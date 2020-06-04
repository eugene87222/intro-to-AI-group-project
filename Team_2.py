import os
import random
import STcpClient
from copy import deepcopy
from datetime import datetime, timedelta

'''
ID : 2
隊名 : 我拿交大畢業證書
組長 : 0516034 楊翔鈞
組員 : 0516118 黃泳繁
'''

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''

INF = 1e10
MAX_DEPTH = 40
DURATION = 4.9
WEIGHT_PIECE = 2.0
WEIGHT_EDGE = 1.5
WEIGHT_MOVE = 1.8

CORNER = -1
EMPTY = 0
BLACK = 1
WHITE = 2

WIDTH, HEIGHT = 8, 8
NORTH = [-1, 0]
NORTHEAST = [-1, 1]
EAST = [0, 1]
SOUTHEAST = [1, 1]
SOUTH = [1, 0]
SOUTHWEST = [1, -1]
WEST = [0, -1]
NORTHWEST = [-1, -1]
DIRECTIONS = (NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST)

ROUND = -1
HISTORY = {}


def OutOfBoard(pos, direction):
    '''first element indicates whether this move is out of board or not
    
    second element indicates the position after this move
    '''
    new_r = pos[0] + direction[0]
    new_c = pos[1] + direction[1]
    if new_r<0 or new_r>=HEIGHT:
        return True, (new_r, new_c)
    if new_c<0 or new_c>=WIDTH:
        return True, (new_r, new_c)
    if new_r in [0, HEIGHT-1] and new_c in [0, WIDTH-1]:
        return True, (new_r, new_c)
    return False, (new_r, new_c)


def IsValidMove(board, pos, direction, is_black):
    res = OutOfBoard(pos, direction)
    if not res[0]:
        next_pos = res[1]
    else:
        return False
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    if board[next_pos[0]][next_pos[1]] == opponent:
        while board[next_pos[0]][next_pos[1]] == opponent:
            res = OutOfBoard(next_pos, direction)
            if res[0]:
                return False
            else:
                next_pos = res[1]
        if board[next_pos[0]][next_pos[1]] == player:
            return True
    return False


def GetValidMoves(board, is_black):
    moves = []
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    # upper edge ==============================================================
    if board[0][1] == EMPTY:
        for d in [SOUTH, SOUTHEAST, EAST]:
            if IsValidMove(board, (0, 1), d, is_black):
                moves.append((0, 1))
                break
    if board[0][2] == EMPTY:
        for d in [SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
            if IsValidMove(board, (0, 2), d, is_black):
                moves.append((0, 2))
                break
    if board[0][3] == EMPTY:
        for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
            if IsValidMove(board, (0, 3), d, is_black):
                moves.append((0, 3))
                break
    if board[0][4] == EMPTY:
        for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
            if IsValidMove(board, (0, 4), d, is_black):
                moves.append((0, 4))
                break
    if board[0][5] == EMPTY:
        for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST]:
            if IsValidMove(board, (0, 5), d, is_black):
                moves.append((0, 5))
                break
    if board[0][6] == EMPTY:
        for d in [WEST, SOUTHWEST, SOUTH]:
            if IsValidMove(board, (0, 6), d, is_black):
                moves.append((0, 6))
                break
    # left edge ==============================================================
    if board[1][0] == EMPTY:
        for d in [EAST, SOUTHEAST, SOUTH]:
            if IsValidMove(board, (1, 0), d, is_black):
                moves.append((1, 0))
                break
    if board[2][0] == EMPTY:
        for d in [NORTHEAST, EAST, SOUTHEAST, SOUTH]:
            if IsValidMove(board, (2, 0), d, is_black):
                moves.append((2, 0))
                break
    if board[3][0] == EMPTY:
        for d in [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH]:
            if IsValidMove(board, (3, 0), d, is_black):
                moves.append((3, 0))
                break
    if board[4][0] == EMPTY:
        for d in [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH]:
            if IsValidMove(board, (4, 0), d, is_black):
                moves.append((4, 0))
                break
    if board[5][0] == EMPTY:
        for d in [NORTH, NORTHEAST, EAST, SOUTHEAST]:
            if IsValidMove(board, (5, 0), d, is_black):
                moves.append((5, 0))
                break
    if board[6][0] == EMPTY:
        for d in [NORTH, NORTHEAST, EAST]:
            if IsValidMove(board, (6, 0), d, is_black):
                moves.append((6, 0))
                break
    # lower edge ==============================================================
    if board[7][1] == EMPTY:
        for d in [NORTH, NORTHEAST, EAST]:
            if IsValidMove(board, (7, 1), d, is_black):
                moves.append((7, 1))
                break
    if board[7][2] == EMPTY:
        for d in [NORTHWEST, NORTH, NORTHEAST, EAST]:
            if IsValidMove(board, (7, 2), d, is_black):
                moves.append((7, 2))
                break
    if board[7][3] == EMPTY:
        for d in [WEST, NORTHWEST, NORTH, NORTHEAST, EAST]:
            if IsValidMove(board, (7, 3), d, is_black):
                moves.append((7, 3))
                break
    if board[7][4] == EMPTY:
        for d in [WEST, NORTHWEST, NORTH, NORTHEAST, EAST]:
            if IsValidMove(board, (7, 4), d, is_black):
                moves.append((7, 4))
                break
    if board[7][5] == EMPTY:
        for d in [WEST, NORTHWEST, NORTH, NORTHEAST]:
            if IsValidMove(board, (7, 5), d, is_black):
                moves.append((7, 5))
                break
    if board[7][6] == EMPTY:
        for d in [WEST, NORTHWEST, NORTH]:
            if IsValidMove(board, (7, 6), d, is_black):
                moves.append((7, 6))
                break
    # right edge ==============================================================
    if board[1][7] == EMPTY:
        for d in [WEST, SOUTHWEST, SOUTH]:
            if IsValidMove(board, (1, 7), d, is_black):
                moves.append((1, 7))
                break
    if board[2][7] == EMPTY:
        for d in [NORTHWEST, WEST, SOUTHWEST, SOUTH]:
            if IsValidMove(board, (2, 7), d, is_black):
                moves.append((2, 7))
                break
    if board[3][7] == EMPTY:
        for d in [NORTH, NORTHWEST, WEST, SOUTHWEST, SOUTH]:
            if IsValidMove(board, (3, 7), d, is_black):
                moves.append((3, 7))
                break
    if board[4][7] == EMPTY:
        for d in [NORTH, NORTHWEST, WEST, SOUTHWEST, SOUTH]:
            if IsValidMove(board, (4, 7), d, is_black):
                moves.append((4, 7))
                break
    if board[5][7] == EMPTY:
        for d in [NORTH, NORTHWEST, WEST, SOUTHWEST]:
            if IsValidMove(board, (5, 7), d, is_black):
                moves.append((5, 7))
                break
    if board[6][7] == EMPTY:
        for d in [NORTH, NORTHWEST, WEST]:
            if IsValidMove(board, (6, 7), d, is_black):
                moves.append((6, 7))
                break
    # central 6x6 =============================================================
    for r in range(1, HEIGHT-1):
        for c in range(1, WIDTH-1):
            if board[r][c] == EMPTY:
                moves.append((r, c))
    # random.shuffle(moves)
    return moves


def CheckFlip(board, pos, direction, is_black):
    res = OutOfBoard(pos, direction)
    flip = []
    if not res[0]:
        pos = res[1]
    else:
        return False, []
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    if board[pos[0]][pos[1]] == opponent:
        while board[pos[0]][pos[1]] == opponent:
            flip.append(pos)
            res = OutOfBoard(pos, direction)
            if res[0]:
                break
            else:
                pos = res[1]
        if board[pos[0]][pos[1]] == player:
            return True, flip
    return False, []


def PlaceAndFlip(board, pos, is_black):
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    new_board = deepcopy(board)
    new_board[pos[0]][pos[1]] = player
    for d in DIRECTIONS:
        res = CheckFlip(new_board, pos, d, is_black)
        if res[0]:
            for t in res[1]:
                new_board[t[0]][t[1]] = player
    return new_board


def Evaluate(board, is_black):
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    moves = GetValidMoves(board, is_black)
    player_edge = 0
    player_piece = 0
    opponent_edge = 0
    opponent_piece = 0
    opponent_moves = GetValidMoves(board, not is_black)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if board[r][c]==EMPTY or board[r][c]==CORNER:
                continue
            elif board[r][c] == player:
                player_piece += 1
                if r in [0, HEIGHT-1] or c in [0, WIDTH-1]:
                    player_edge += 1
            elif board[r][c] == opponent:
                opponent_piece += 1
                if r in [0, HEIGHT-1] or c in [0, WIDTH-1]:
                    opponent_edge += 1
            else:
                # print(f'ERROR, unknown value at {board[r][c]}')
                pass
    piece_score = 1 if player_piece>opponent_piece else 0 if player_piece==opponent_piece else -1
    edge_score = player_edge - opponent_edge
    return piece_score*WEIGHT_PIECE + edge_score*WEIGHT_EDGE + len(moves)*WEIGHT_MOVE


def Stringify(board, is_black):
    board_str = ''.join([''.join(map(str, row)) for row in board])
    if is_black:
        return f'B{board_str}'
    else:
        return f'W{board_str}'


def Max(board, is_black, depth, lifetime, alpha, beta):
    global HISTORY
    board_str = Stringify(board, is_black)
    if board_str in HISTORY:
        return HISTORY[board_str]
    if depth>MAX_DEPTH or datetime.now()>lifetime:
        score = Evaluate(board, is_black)
        HISTORY[board_str] = score
        return score
    v = -INF
    next_steps = GetValidMoves(board, is_black)
    if len(next_steps) == 0:
        score = Evaluate(board, is_black)
        HISTORY[board_str] = score
        return score
    for step in next_steps:
        v = max(v, Min(board, not is_black, depth+1, lifetime, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def Min(board, is_black, depth, lifetime, alpha, beta):
    global HISTORY
    board_str = Stringify(board, is_black)
    if board_str in HISTORY:
        return HISTORY[board_str]
    if depth>MAX_DEPTH or datetime.now()>lifetime:
        score = Evaluate(board, is_black)
        HISTORY[board_str] = score
        return score
    v = INF
    next_steps = GetValidMoves(board, is_black)
    if len(next_steps) == 0:
        score = Evaluate(board, is_black)
        HISTORY[board_str] = score
        return score
    for step in next_steps:
        v = min(v, Max(board, not is_black, depth+1, lifetime, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def AlphaBetaPruning(board, is_black, lifetime):
    depth = 0
    best_move = None
    max_score = -INF
    score = -INF
    moves = GetValidMoves(board, is_black)
    for move in moves:
        new_board = PlaceAndFlip(board, move, is_black)
        score = Min(new_board, not is_black, depth, lifetime, max_score ,INF)
        if score >= max_score:
            max_score = score
            best_move = move
        if datetime.now() > lifetime:
            # print('moves 跑到一半')
            break
    return move


def GetStep(board, is_black):
    global ROUND, HISTORY
    if ROUND == -1:
        ROUND = is_black
        HISTORY = {}
    elif ROUND != is_black:
        ROUND = is_black
        HISTORY = {}
    lifetime = datetime.now() + timedelta(seconds=DURATION)
    move = AlphaBetaPruning(board, is_black, lifetime)
    return move


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
