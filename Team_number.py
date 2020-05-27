import os
import random
import STcpClient

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''

cnt = 0

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
    if new_r%HEIGHT in [0, 7] and new_c%WIDTH in [0, 7]:
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
    player, opponent = (BLACK, WHITE) if is_black else (BLACK, WHITE)
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
    return moves


def GetStep(board, is_black):
    '''
    Example:
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    return (x,y)
    '''
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    moves = GetValidMoves(board, is_black)
    if is_black:
        with open(f'./output_black/{cnt}.log', 'w') as file:
            for row in board:
                file.write(f'{row}\n')
            file.write('\n')
            for move in moves:
                file.write(f'{move}\n')
    else:
        with open(f'./output_white/{cnt}.log', 'w') as file:
            for row in board:
                file.write(f'{row}\n')
            file.write('\n')
            for move in moves:
                file.write(f'{move}\n')
    return (x, y)


os.mkdir('output_black')
os.mkdir('output_white')

while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
    cnt += 1
