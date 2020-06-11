from copy import deepcopy
import pickle
import random
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

def reward(board, is_black):
    r = 0
    who, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
    for row in range(8):
        for col in range(8):
            if board[row][col] == who:
                r += 1
            elif board[row][col] == opponent:
                r -= 1
    return r/60 # reward at [-1, 1]
# reinforcement learning with n-tuple network
class agent():
    def __init__(self, load_file = None, save_file = None, name = 'Player', alpha = 0.5, init_weight = False):
        self.load_file = load_file
        self.save_file = save_file
        self.name = name
        self.alpha = alpha
        self.init_weight = init_weight
        
    def save_network(self):
        if self.save_file:
            with open(self.save_file, 'wb') as fp:
                pickle.dump(self.weight, fp, protocol=pickle.HIGHEST_PROTOCOL)
    def load_network(self):
        with open(self.load_file, 'rb') as fp:
            self.weight = pickle.load(fp)
    def set_tuple(self, tuple_list, tuple_size):
        self.tuple_list = tuple_list
        
        # init weight if need, else load weight from file
        if self.init_weight:
            self.weight = []
            # every tuple has its own set of weight
            for i in range(len(tuple_list)):
                # combination of single tuple at size = 3**size 
                # init value at (-1, 1)
                self.weight.append([random.uniform(-1, 1) for x in range(3**tuple_size)])
        elif load_file:
            self.load_network()
           
    # 旋轉盤面 順時針90度
    def rotate(self, board):
        return [list(r) for r in zip(*board[::-1])]
    ##################################################################################
    def open_episode(self):
        self.epi = []
    def close_episode(self):
        self.epi = self.epi[::-1]
        err = self.alpha * (reward(self.epi[0], self.is_black))# self.value(self.epi[0]))
        self.update(self.epi[0], err)
        #print('endgame:', err)
        for e in range(1, len(self.epi)):
            self.training(self.epi[e], self.epi[e-1])
    def training(self, before, after):
        # TD(0)
        # err += a*( (r+after) - before )
        err = self.alpha * ((reward(after, self.is_black)+self.value(after) - self.value(before)))
        self.update(before, err)
    # update weight
    def update(self, board, err):
        tmp = deepcopy(board)
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
                self.weight[idx][key1] += err
                self.weight[idx][key2] += err
            tmp = [list(r) for r in zip(*tmp[::-1])]
    ##################################################################################
    def GetStep(self, board, is_black):
        # n tuple network
        self.board = deepcopy(board)
        choose_epi = None
        self.is_black = is_black
        
        moves = self.Get_Valid_Moves(is_black)
        if moves:
            (max_val, step) = (None, moves[0])
            for m in moves:
                self.board = deepcopy(board)
                self.board = self.set_and_flip(m, is_black)
                val = self.value(self.board)
                val += reward(self.board, is_black)
                if max_val is None:
                    max_val = val
                    step = m
                    choose_epi = self.board
                elif val > max_val:
                    max_val = val
                    step = m
                choose_epi = self.board
        else:
            return None
        self.epi.append(deepcopy(self.board))
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
                val += self.weight[idx][key1]
                val += self.weight[idx][key2]
            # 旋轉clockwise 90°
            tmp = [list(r) for r in zip(*tmp[::-1])]
        return val
    ##################################################################################
    # return set of possible moves
    def Get_Valid_Moves(self, is_black):
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
        if row > 0 and row < 7\
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
                        # this edge placement is legal
                        return True
                    else:
                        break
                if self.board[row][col] == opponent:
                    fli = [row,col]
                    flip = True
        return False
    ##################################################################################
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