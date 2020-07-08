import curses
import copy


BOARD_LEN = 8

TILE_CH = '#'
MAN_CH = 'o'
QUEEN_CH = 'Q'
MAN_HUMAN_CH = 'h'
MAN_PC_CH = 'p'
QUEEN_HUMAN_CH = 'H'
QUEEN_PC_CH = 'P'
MOVE_CH = '?'
START_MAN_CH = 's'
START_QUEEN_CH = 'S'


MOVE_PC = []
DEPTH = 0


def new_board():
    """
     return: 2d list: new board with a starting configuration
    """

    board = []
    row = [TILE_CH] * BOARD_LEN

    for i in range(BOARD_LEN):
        if i in range(3, BOARD_LEN - 3):
            board.append(list(row))
        else:
            board.append(list())

            if i in range(3):
                piece = MAN_PC_CH
            else:  # i in range(BOARD_LEN - 3, BOARD_LEN)
                piece = MAN_HUMAN_CH

            for j in range(BOARD_LEN):
                if (i + j) % 2 == 1:
                    board[i].append(piece)
                else:
                    board[i].append(TILE_CH)

    return board


def possible_moves(board, pos, player, capture):
    """
    moves = possible_captures(board, pos, player, 1)

    if len(moves) == 0:
        moves = possible_shifts(board, pos, player)

    return moves
    """

    if capture:
        return possible_captures(board, pos, player, 1)
    else:
        return possible_shifts(board, pos, player)


def possible_shifts(board, pos, player):
    """
     board: 2d list: tiles
     pos: pair of ints: coordinates to move from
     player: bool: true represents a human, false represents a pc

     return: list of pairs of ints: coordinates of possible shift movements
    """

    moves = []

    if player:
        man_char = MAN_HUMAN_CH
        queen_char = QUEEN_HUMAN_CH
        shift = -1
    else:
        man_char = MAN_PC_CH
        queen_char = QUEEN_PC_CH
        shift = 1

    if board[pos[0]][pos[1]] != man_char and board[pos[0]][pos[1]] != queen_char:
        return moves

    if (pos[0] + shift >= 0 and player) or (pos[0] + shift < BOARD_LEN and not player):
        if pos[1] - 1 >= 0 and board[pos[0] + shift][pos[1] - 1] == TILE_CH:
            moves.append([pos, (pos[0] + shift, pos[1] - 1)])
        if pos[1] + 1 < BOARD_LEN and board[pos[0] + shift][pos[1] + 1] == TILE_CH:
            moves.append([pos, (pos[0] + shift, pos[1] + 1)])

    if board[pos[0]][pos[1]] == queen_char:
        if (pos[0] - shift >= 0 and not player) or (pos[0] - shift < BOARD_LEN and player):
            if pos[1] - 1 >= 0 and board[pos[0] - shift][pos[1] - 1] == TILE_CH:
                moves.append([pos, (pos[0] - shift, pos[1] - 1)])
            if pos[1] + 1 < BOARD_LEN and board[pos[0] - shift][pos[1] + 1] == TILE_CH:
                moves.append([pos, (pos[0] - shift, pos[1] + 1)])

    return moves


def possible_captures(board, pos, player, fly):
    """
     board: 2d list: tiles
     pos: pair of ints: coordinates to move from
     player: bool: true represents a human, false represents a pc

     return: list of pairs of ints: coordinates of possible capture movements
    """

    moves = []

    if player:
        man_char = MAN_HUMAN_CH
        queen_char = QUEEN_HUMAN_CH
        man_enemy_char = MAN_PC_CH
        queen_enemy_char = QUEEN_PC_CH
        shift = -2
    else:
        man_char = MAN_PC_CH
        queen_char = QUEEN_PC_CH
        man_enemy_char = MAN_HUMAN_CH
        queen_enemy_char = QUEEN_HUMAN_CH
        shift = 2

    if board[pos[0]][pos[1]] != man_char and board[pos[0]][pos[1]] != queen_char:
        return moves

    if (pos[0] + shift >= 0 and player) or (pos[0] + shift < BOARD_LEN and not player):
        if (pos[1] - 2 >= 0 and board[pos[0] + shift][pos[1] - 2] == TILE_CH
           and (board[int(pos[0] + shift / 2)][pos[1] - 1] == man_enemy_char
                or board[int(pos[0] + shift / 2)][pos[1] - 1] == queen_enemy_char)):
            moves.append([pos, (pos[0] + shift, pos[1] - 2)])
            move = [pos, (pos[0] + shift, pos[1] - 2)]
            if fly:
                capture_fly(board, player, moves, move)
        if (pos[1] + 2 < BOARD_LEN and board[pos[0] + shift][pos[1] + 2] == TILE_CH
           and (board[int(pos[0] + shift / 2)][pos[1] + 1] == man_enemy_char
                or board[int(pos[0] + shift / 2)][pos[1] + 1] == queen_enemy_char)):
            moves.append([pos, (pos[0] + shift, pos[1] + 2)])
            move = [pos, (pos[0] + shift, pos[1] + 2)]
            if fly:
                capture_fly(board, player, moves, move)

    if board[pos[0]][pos[1]] == queen_char:
        if (pos[0] - shift >= 0 and not player) or (pos[0] - shift < BOARD_LEN and player):
            if (pos[1] - 2 >= 0 and board[pos[0] - shift][pos[1] - 2] == TILE_CH
                    and (board[int(pos[0] - shift / 2)][pos[1] - 1] == man_enemy_char
                         or board[int(pos[0] - shift / 2)][pos[1] - 1] == queen_enemy_char)):
                moves.append([pos, (pos[0] - shift, pos[1] - 2)])
                move = [pos, (pos[0] - shift, pos[1] - 2)]
                if fly:
                    capture_fly(board, player, moves, move)
            if (pos[1] + 2 < BOARD_LEN and board[pos[0] - shift][pos[1] + 2] == TILE_CH
                    and (board[int(pos[0] - shift / 2)][pos[1] + 1] == man_enemy_char
                         or board[int(pos[0] - shift / 2)][pos[1] + 1] == queen_enemy_char)):
                moves.append([pos, (pos[0] - shift, pos[1] + 2)])
                move = [pos, (pos[0] - shift, pos[1] + 2)]
                if fly:
                    capture_fly(board, player, moves, move)

    return moves


def capture_fly(board, player, moves, move):
    """
     board: 2d list of tiles
     player: bool: true represents a human, false represents a pc
     moves: list of lists of pairs of ints: list of sequences of movement actions
     move: list of pairs of ints: upcoming move

     return void
    """
    board_step = copy.deepcopy(board)
    if step(board_step, [move[-2], move[-1]]):  # crowned
        return

    captures = possible_captures(board_step, move[-1], player, 0)

    if len(captures) != 0:
        for capture in captures:
            move_step = copy.deepcopy(move)
            move_step.append((capture[1][0], capture[1][1]))
            moves.insert(0, move_step)

            capture_fly(board_step, player, moves, move_step)


def show_board(board):
    """
     board: 2d list of tiles

     return void
    """
    print("---board---")
    for row in board:
        for symbol in row:
            print(symbol + " ", end='')
        print('\n', end='')


def step(board, move):
    """
     board: 2d list of tiles
     move: list of pairs of ints: sequence of movement actions

     return: void
    """

    for i in range(len(move) - 1):
        if abs(move[i][0] - move[i + 1][0]) == 2:  # and abs(move[i][1] - move[i + 1][1]) == 2
            board[int((move[i][0] + move[i + 1][0]) / 2)][int((move[i][1] + move[i + 1][1]) / 2)] = TILE_CH

    figure = board[move[0][0]][move[0][1]]
    board[move[0][0]][move[0][1]] = TILE_CH

    if figure == MAN_HUMAN_CH and move[-1][0] == 0:
        board[move[-1][0]][move[-1][1]] = QUEEN_HUMAN_CH
        return 1
    elif figure == MAN_PC_CH and move[-1][0] == BOARD_LEN - 1:
        board[move[-1][0]][move[-1][1]] = QUEEN_PC_CH
        return 1
    else:
        board[move[-1][0]][move[-1][1]] = figure


def check_captures(board, player):
    """
     board: 2d list of tiles
     player: bool: true represents a human, false represents a pc

     return bool: true if at least one capture movement is possible, false otherwise
    """
    if player:
        man = MAN_HUMAN_CH
        queen = QUEEN_HUMAN_CH
    else:
        man = MAN_PC_CH
        queen = QUEEN_PC_CH

    captures = []

    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if board[i][j] == man or board[i][j] == queen:
                capture = possible_captures(board, (i, j), player, 0)
                if len(capture) != 0:
                    captures.append(capture)

    return bool(len(captures))


def game_over(board):
    """
     board: 2d list of tiles

     return: int: 0 means, that game is not over yet
                  1 means, that human lost,
                  2 means, that pc lost
    """
    stop = 0

    for row in board:
        for tile in row:
            if tile == MAN_HUMAN_CH or tile == QUEEN_HUMAN_CH or tile == START_MAN_CH or tile == START_QUEEN_CH:
                stop = 1
        if stop:
            break
    else:
        return 1

    stop = 0

    for row in board:
        for tile in row:
            if tile == MAN_PC_CH or tile == QUEEN_PC_CH:
                stop = 1
        if stop:
            break
    else:
        return 2

    return 0


def eval_minimax(board, player, depth):
    """
     board: 2d list of tiles
     player: bool: true represents a maximizing player,
                   false represents a minimizing player
     depth: int >= 0: depth of the game tree

     return float: value of the terminal node for the concrete player
    """
    value_human = 0
    value_pc = 0

    for row in board:
        for tile in row:
            if tile == MAN_HUMAN_CH:
                value_human += 1
            elif tile == QUEEN_HUMAN_CH:
                value_human += 2
            elif tile == MAN_PC_CH:
                value_pc += 1
            elif tile == QUEEN_PC_CH:
                value_pc += 2

    value = value_human - value_pc + depth * 3

    if player:
        return value
    else:
        return (-1.0) * value


def minimax_choice_heuristic(moves):
    """
     moves: lost of lists of pairs of ints: sequence of movement actions

     return: moves sorted by the complexity of movements(length of the sequence)
    """
    return sorted(moves, key=len, reverse=True)


def minimax(board, depth, alpha, beta, player):
    """
     board: 2d list of tiles
     depth: int >= 0: depth of the game tree
     alpha: float
     beta: float
     player: bool: true represents a maximizing player, false represents a minimizing player

     return: best value achieved from the particular board configuration to the current player
    """
    global MOVE_PC

    if depth == 0 or bool(game_over(board)):
        return eval_minimax(board, player, depth)

    if player:
        extr_eval = float("-inf")
    else:
        extr_eval = float("+inf")

    moves = []

    capture = check_captures(board, player)

    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            moves_to_append = possible_moves(board, (i, j), player, capture)
            if len(moves_to_append) != 0:
                for move in moves_to_append:
                    moves.append(move)

    moves = minimax_choice_heuristic(moves)

    for move in moves:
        board_step = copy.deepcopy(board)
        step(board_step, move)

        value = minimax(board_step, depth - 1, alpha, beta, not player)
        if player:
            # extr_eval = max(extr_eval, value)
            if value > extr_eval:
                extr_eval = value
                if depth == DEPTH:
                    MOVE_PC = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        else:
            # extr_eval = min(extr_eval, value)
            if value < extr_eval:
                extr_eval = value
                if depth == DEPTH:
                    MOVE_PC = move
            beta = min(beta, value)
            if alpha >= beta:
                break

    return extr_eval


def print_board(board, screen):
    """
     board: 2d list of tiles
     screen: curses screen

     return: void
    """

    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if (i + j) % 2 == 0:
                screen.addstr(i, 2 * j, board[i][j], curses.color_pair(1))
            else:
                if board[i][j] == MAN_PC_CH:
                    screen.addstr(i, 2 * j, MAN_CH, curses.color_pair(3) | curses.A_BOLD)
                elif board[i][j] == MAN_HUMAN_CH:
                    screen.addstr(i, 2 * j, MAN_CH, curses.color_pair(4) | curses.A_BOLD)
                elif board[i][j] == QUEEN_PC_CH:
                    screen.addstr(i, 2 * j, QUEEN_CH, curses.color_pair(3) | curses.A_BOLD)
                elif board[i][j] == QUEEN_HUMAN_CH:
                    screen.addstr(i, 2 * j, QUEEN_CH, curses.color_pair(4) | curses.A_BOLD)
                elif board[i][j] == MOVE_CH:
                    screen.addstr(i, 2 * j, MOVE_CH, curses.color_pair(5) | curses.A_BOLD)
                elif board[i][j] == START_MAN_CH:
                    screen.addstr(i, 2 * j, MAN_CH, curses.color_pair(6) | curses.A_BOLD)
                elif board[i][j] == START_QUEEN_CH:
                    screen.addstr(i, 2 * j, QUEEN_CH, curses.color_pair(6) | curses.A_BOLD)
                else:
                    screen.addstr(i, 2 * j, board[i][j], curses.color_pair(2))


def print_game_over(board, screen, who):
    """
     board: 2d list of tiles
     screen: curses screen
     who: int >= 0: looser, 1 represents a human, 2 represents a pc

     return: void
    """
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if (i + j) % 2 == 0:
                screen.addstr(i, 2 * j, board[i][j], curses.color_pair(1))
            else:
                screen.addstr(i, 2 * j, board[i][j], curses.color_pair(2))

    if who == 1:
        screen.addstr(3, 2, "You", curses.color_pair(9) | curses.A_BOLD)
        screen.addstr(4, 4, "lost ", curses.color_pair(9) | curses.A_BOLD)
    else:  # who == 2
        screen.addstr(3, 2, "You", curses.color_pair(8) | curses.A_BOLD)
        screen.addstr(4, 4, "won", curses.color_pair(8) | curses.A_BOLD)

    screen.addstr(BOARD_LEN, 0, "Press ESC to exit.", curses.color_pair(7) | curses.A_BOLD)


def add_moves(board, moves):
    """
     board: 2d list of tiles
     moves: list of lists of pairs of ints: list of sequences of movement actions

     return: void
    """
    for move in moves:
        for action_num in range(len(move)):
            if action_num == 0:
                if board[move[action_num][0]][move[action_num][1]] == MAN_HUMAN_CH:
                    board[move[action_num][0]][move[action_num][1]] = START_MAN_CH
                elif board[move[action_num][0]][move[action_num][1]] == QUEEN_HUMAN_CH:
                    board[move[action_num][0]][move[action_num][1]] = START_QUEEN_CH
            else:
                board[move[action_num][0]][move[action_num][1]] = MOVE_CH


def clear_moves(board):
    """
     board: 2d list of tiles

     return: void
    """
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if board[i][j] == MOVE_CH:
                board[i][j] = TILE_CH
            elif board[i][j] == START_MAN_CH:
                board[i][j] = MAN_HUMAN_CH
            elif board[i][j] == START_QUEEN_CH:
                board[i][j] = QUEEN_HUMAN_CH


def set_depth():
    global DEPTH

    difficulty = int(input("Select difficulty(type the number according to your choice):\n"
                           "1) Easy\n"
                           "2) Medium\n"
                           "3) Hard\n"))

    if difficulty == 1:
        DEPTH = 1
    elif difficulty == 2:
        DEPTH = 3
    elif difficulty == 3:
        DEPTH = 7
    else:
        print("The difficulty level must be an integer a, such that 1 <= a <= 3")
        exit(1)


def main(stdscr):
    global DEPTH

    curses.curs_set(0)
    curses.mousemask(1)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)  # tiles 1
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)  # tiles 2
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLUE)  # pieces 1
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # pieces 2
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)  # moves
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)  # first action of the movement
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)  # borders
    curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)  # you won
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)  # you lost

    board = new_board()
    capture = check_captures(board, 1)
    moves = []

    while 1:
        stdscr.refresh()
        moved = 0

        go = game_over(board)
        if bool(go):
            print_game_over(board, stdscr, go)
        else:
            print_board(board, stdscr)

        key = stdscr.getch()

        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()

            clear_moves(board)

            if not go:

                if x < BOARD_LEN * 2 and y < BOARD_LEN and x % 2 == 0:
                    x = int(x / 2)

                    for move in moves:
                        if move[-1] == (y, x):
                            step(board, move)
                            moves.clear()
                            moved = 1

                    if not moved:
                        capture = check_captures(board, 1)
                        moves = possible_moves(board, (y, x), 1, capture)
                        add_moves(board, moves)

                    if moved:
                        minimax(board, DEPTH, float("-inf"), float("+inf"), 0)
                        step(board, MOVE_PC)

        elif key == 27:  # Esc
            break


if __name__ == "__main__":
    set_depth()
    curses.wrapper(main)
