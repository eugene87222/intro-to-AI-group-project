import os
import random
import STcpClient
from copy import deepcopy
from datetime import datetime, timedelta

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''

# cnt = 0

INF = 1e10
MAX_DEPTH = 100

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


def OutOfBoard(pos, direction):
    new_r = pos[0] + direction[0]
    new_c = pos[1] + direction[1]
    if new_r<0 or new_r>=HEIGHT:
        return True, (new_r, new_c)
    if new_c<0 or new_c>=WIDTH:
        return True, (new_r, new_c)
    if new_r in [0, HEIGHT-1] and new_c in [0, WIDTH-1]:
        return True, (new_r, new_c)
    return False, (new_r, new_c)


def GetValidMove(board, pos, direction, is_black):
    res = OutOfBoard(pos, direction)
    # first element indicates whether this move is out of board or not
    # second element indicates the position after this move
    if not res[0]:
        pos = res[1]
    else:
        return False, pos
    opponent = WHITE if is_black else BLACK
    if board[pos[0]][pos[1]] == opponent:
        while board[pos[0]][pos[1]] == opponent:
            res = OutOfBoard(pos, direction)
            if res[0]:
                break
            else:
                pos = res[1]
        if board[pos[0]][pos[1]] == EMPTY:
            return True, pos
    return False, pos


def GetValidMoves(board, is_black):
    moves = set()
    player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if board[r][c] == CORNER:
                continue
            elif board[r][c] == opponent:
                continue
            elif board[r][c] == player:
                for d in DIRECTIONS:
                    # first element indicates whether returned position is valid after this move
                    # second element is the position after this move
                    res = GetValidMove(board, (r, c), d, is_black)
                    if res[0]:
                        moves.add(res[1])
            elif board[r][c] == EMPTY:
                if r>0 and r<HEIGHT-1 and c>0 and c<WIDTH-1:
                    moves.add((r, c))
            else:
                print(f'ERROR, unknown value at {board[r][c]}')
    return list(moves)


def CheckFlip(board, pos, direction, is_black):
    res = OutOfBoard(pos, direction)
    # first element indicates whether this move is out of board or not
    # second element indicates the position after this move
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
                print(f'ERROR, unknown value at {board[r][c]}')
    if player_piece > opponent_piece:
        piece_score = 1
    elif player_piece == opponent_piece:
        piece_score = 0
    else:
        piece_score = -1
    edge_score = player_edge - opponent_edge
    return piece_score * 2 + edge_score * 1.5


def Max(board, is_black, depth, lifetime, alpha, beta):
    if depth>MAX_DEPTH or datetime.now()>lifetime:
        # time exceeded or too deep -> evaluate and return score
        return Evaluate(board, is_black)
    v = -1e10
    # list every valid move
    next_steps = GetValidMoves(board, is_black)
    for step in next_steps:
        v = max(v, Min(board, not is_black, depth+1, lifetime, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def Min(board, is_black, depth, lifetime, alpha, beta):
    if depth>MAX_DEPTH or datetime.now()>lifetime:
        # time exceeded or too deep -> evaluate and return score
        return Evaluate(board, is_black)
    v = 1e10
    # list every valid move
    next_steps = GetValidMoves(board, is_black)
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
        if score > max_score:
            max_score = score
            best_move = move
        if datetime.now() > lifetime:
            print('moves 跑到一半')
            break
    return move


def GetStep(board, is_black):
    '''
    Example:
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    return (x, y)
    '''
    # moves = GetValidMoves(board, is_black)
    # if is_black:
    #     with open(f'./output_black/{cnt}.log', 'w') as file:
    #         for row in board:
    #             for col in row:
    #                 file.write(f'{col:>2} ')
    #             file.write('\n')
    #         file.write('\n')
    #         for move in moves:
    #             new_board = PlaceAndFlip(board, move, is_black)
    #             file.write(f'{move}\n')
    #             for row in new_board:
    #                 for col in row:
    #                     file.write(f'{col:>2} ')
    #                 file.write('\n')
    #             file.write('\n')
    # else:
    #     with open(f'./output_white/{cnt}.log', 'w') as file:
    #         for row in board:
    #             for col in row:
    #                 file.write(f'{col:>2} ')
    #             file.write('\n')
    #         file.write('\n')
    #         for move in moves:
    #             new_board = PlaceAndFlip(board, move, is_black)
    #             file.write(f'{move}\n')
    #             for row in new_board:
    #                 for col in row:
    #                     file.write(f'{col:>2} ')
    #                 file.write('\n')
    #             file.write('\n')
    # return random.choice(moves)

    lifetime = datetime.now() + timedelta(seconds=4.4)
    move = AlphaBetaPruning(board, is_black, lifetime)
    return move


# os.mkdir('output_black')
# os.mkdir('output_white')

while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
    # cnt += 1
