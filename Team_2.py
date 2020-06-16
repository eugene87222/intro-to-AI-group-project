import pickle
import random
import STcpClient
from copy import deepcopy

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
WHITE = 2
BLACK = 1
EMPTY = 0
CORNER = -1

# 從 pos 開始，把 n 個座標視為一個 tuple
# n 決定 tuple 長度
# d 決定 tuple 衍生方向
# 回傳 list (整個 tuple 的所有座標)
def gen_tuple(pos=[0, 0], n=0, d=SOUTH):
    tup_list = []
    for t in range(n):
        tup_list.append(pos[:])
        pos[0] += d[0]
        pos[1] += d[1]
    return tup_list


# all-3 tuple in reference
def all_3_ref():
    ALL_N_TUPLE = 3

    tup_node = [ [] for i in range(4)] # row 0-3
    tup_node[0] = [[x,0] for x in range(1,3)] # 1 2
    tup_node[1] = [[x,1] for x in range(3)] # 0-2
    tup_node[2] = [[x,2] for x in range(3)]
    tup_node[3] = [[x,3] for x in range(3)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1-5
    tup_node[1] = [[x,1] for x in range(1,5)] # 1-4 
    tup_node[2] = [[x,2] for x in range(2,4)] # 2-3
    del tup_node[3]
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE


# all-3 tuple customize version
def all_3_custom():
    ALL_N_TUPLE = 3
    
    tup_node = [ [] for i in range(4)] # row 0-3
    tup_node[0] = [[x,0] for x in range(1,3)] # 1 2
    tup_node[1] = [[x,1] for x in range(3)] # 0 1 2
    tup_node[2] = [[x,2] for x in range(3)]
    tup_node[3] = [[x,3] for x in range(3)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1-5
    tup_node[1] = [[x,1] for x in range(0,6)] # 0~5 
    tup_node[2] = [[x,2] for x in range(0,6)] # 0~5 
    tup_node[3] = [[x,3] for x in range(0,6)] # 0~5 
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE


# reinforcement learning with n-tuple network
class agent():
    def __init__(self, black_load=None, white_load=None):
        self.black_load = black_load
        self.white_load = white_load

    def load_network(self):
        if self.black_load:
            with open(self.black_load, 'rb') as fp:
                self.black_weight = pickle.load(fp)
        if self.white_load:
            with open(self.white_load, 'rb') as fp:
                self.white_weight = pickle.load(fp)

    def set_tuple(self, tuple_list, tuple_size):
        self.tuple_list = tuple_list
        self.load_network()

    def GetStep(self, board, is_black):
        # n tuple network
        self.board = (board)
        self.is_black = is_black
        
        moves = self.get_valid_moves(is_black)
        if moves:
            (max_val, step) = (None, moves[0])
            for m in moves:
                self.board = deepcopy(board)
                self.board = self.set_and_flip(m, is_black)
                val = self.value(self.board)
                if max_val is None:
                    max_val = val
                    step = m
                elif val > max_val:
                    max_val = val
                    step = m
        else:
            return None
        return step

    def value(self, board):
        val = 0
        tmp = deepcopy(board)

        # 旋轉盤面 4 次的 symmetric tuple
        for loop in range(4):
            # 水平面翻轉
            flip_board = tmp[::-1]
            
            for idx in range(len(self.tuple_list)):
                tup = self.tuple_list[idx]
                key1 = 0
                key2 = 0
                fv = 1
                for node in tup:
                    key1 += (fv * tmp[node[0]][node[1]])
                    key2 += (fv * flip_board[node[0]][node[1]])
                    fv *= 3
                # 通過 key 取得 weight
                if self.is_black:
                    val += self.black_weight[idx][key1]
                    val += self.black_weight[idx][key2]
                else:
                    val += self.white_weight[idx][key1]
                    val += self.white_weight[idx][key2]
            # 旋轉 clockwise 90°
            tmp = [list(r) for r in zip(*tmp[::-1])]
        return val

    # return set of possible moves
    def get_valid_moves(self, is_black):
        moves = []
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.is_legal_move([row, col], is_black):
                    moves.append([row, col])
        return moves

    def is_legal_move(self, step, is_black):
        # determine whether an action is legal
        (row, col) = step
        
        # the position must be empty
        if self.board[row][col] != EMPTY or self.board[row][col] == CORNER:
            return False
        
        # inside 6x6
        if row > 0 and row < 7 \
        and col > 0 and col < 7:
            return True
        
        # out of 8x8
        if row < 0 or col < 0 \
        or row > 7 or col > 7:
            return False
        
        # edge placement: check flip rule is satisfied
        who, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)

        for d in DIRECTIONS:
            (row, col) = step
            flip = False
            for loop in range(7):
                # move one step forward in Direction d
                row += d[0]
                col += d[1]

                # out of bound
                if row < 0 or col < 0 \
                or row > 7 or col > 7:
                    break
                
                # who -> opponent(+) -> who ===> flip
                if self.board[row][col] == EMPTY or self.board[row][col] == CORNER:
                    break
                if self.board[row][col] == who:
                    if flip:
                        return True
                    else:
                        break
                if self.board[row][col] == opponent:
                    fli = [row,col]
                    flip = True
        return False

    def set_and_flip(self, step, is_black):
        test_board = deepcopy(self.board)
        
        test_board[step[0]][step[1]] = BLACK if is_black else WHITE
        
        who, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        for d in DIRECTIONS:
            (row, col) = step
            flip = False
            flip_set = []
            for loop in range(7):
                # move one step foward in Direction d
                row += d[0]
                col += d[1]
                
                # out of bound
                if row < 0 or col < 0 \
                or row > 7 or col > 7:
                    break

                if test_board[row][col] == EMPTY or test_board[row][col] == CORNER:
                    break
                if test_board[row][col] == who:
                    if flip:
                        # this edge placement is legal
                        for s in flip_set:
                            r,c = s
                            test_board[r][c] = who
                        break
                    else:
                        break
                if test_board[row][col] == opponent:
                    flip_set.append([row, col])
                    flip = True
        return test_board


def GetStep(board, is_black):
    if is_black:
        brain = agent(black_load='./Team_2_all_3_custom_black.p')
    else:
        brain = agent(white_load='./Team_2_all_3_custom_white.p')
    tuple_list, tuple_size = all_3_custom()
    brain.set_tuple(tuple_list, tuple_size)
    return brain.GetStep(board, is_black)


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
