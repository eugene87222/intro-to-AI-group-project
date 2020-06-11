#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
from copy import deepcopy
#import operator
#import numpy as np
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# In[376]:


# params
WHITE = 2
BLACK = 1
EMPTY = 0
CORNER = -1
# agent params
alpha = 0.5


# In[377]:


class Game:
    def __init__(self):
        # var to record game
        self.all_games = []
        self.whosturn = []
        self.err = ''
        self.ep = 0
        self.game_score = []
    def reset(self):
        self.board = [[EMPTY for col in range(8)] for row in range(8)]
        self.board[0][0] = CORNER
        self.board[7][7] = CORNER
        self.board[0][7] = CORNER
        self.board[7][0] = CORNER
        self.prev_step = (-1,-1)
        self.is_black = None
    
    def place(self, step, is_black):
        self.prev_step = step
        self.is_black = is_black
        
        if self.is_legal_move(step, is_black):
            # legal placement, just do it!
            self.set_and_flip(step, is_black)
            return True
        else:
            return False
    def set_and_flip(self, step, is_black):
        self.board[step[0]][step[1]] = BLACK if is_black else WHITE
        
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
                if row < 0 or col < 0                 or row > 7 or col > 7:
                    break

                if self.board[row][col] == EMPTY or self.board[row][col] == CORNER:
                    break
                if self.board[row][col] == who:
                    if flip:
                        # this edge placement is legal
                        for s in flip_set:
                            r,c = s
                            self.board[r][c] = who
                        break
                    else:
                        break
                if self.board[row][col] == opponent:
                    flip_set.append([row, col])
                    flip = True
    def is_legal_move(self, step, is_black):
        # determine whether an action from player is legal
        (row, col) = step
        # the position must be empty
        if self.board[row][col] != EMPTY or self.board[row][col] == CORNER:
            return False
        
        # inside 6x6
        if row > 0 and row < 7        and col > 0 and col < 7:
            return True
        
        # out of 8x8
        if row < 0 or col < 0         or row > 7 or col > 7:
            return False
        
        # edge placement: check flip rule is satisfied
        who, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        for d in DIRECTIONS:
            (row, col) = step
            flip = False
            
            for loop in range(7):
                # move one step foward in Direction d
                row += d[0]
                col += d[1]
                
                # out of bound
                if row < 0 or col < 0                 or row > 7 or col > 7:
                    break

                if self.board[row][col] == EMPTY or self.board[row][col] == CORNER:
                    break
                if self.board[row][col] == who:
                    if flip:
                        # this edge placement is legal
                        return True
                    else:
                        break
                if self.board[row][col] == opponent:
                    flip = True
        return False
    
    # print board in prompt
    def show(self):
        print('============ episode:' ,self.ep+1 , '============', 
              '# {}{}'.format(
                              'B' if self.is_black else 'W',
                              self.prev_step)
                             )
        for row in range(HEIGHT):
            for col in range(WIDTH):
                print('{:>4}'.format(self.board[row][col]), end='')
            print('')
            
    # write every end game state into file 'game_report.txt'
    def summary(self):
        with open('game_report.txt', 'w') as fp:
            for e in range(self.ep):
                game = self.all_games[e]
                score = self.game_score[e]
                header = '============ episode ' + str(e+1) + ' ============ B:W-' +                          str(score[0]) + ':' + str(score[1]) + '\n'
                fp.write(header)
                for row in range(8):
                    for col in range(8):
                        fp.write('{:4}'.format(game[row][col]))
                    fp.write('\n')
    # store end game state
    def save_match(self):
        self.all_games.append(self.board)
        #self.whosturn.append(is_black)
    
    # store error encounter in string 
    def track_err(self, err='TLE', is_black=True, step=(-1,-1)):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        err_summary = 'Error: ' + err + ' on '
        if is_black:
            err_summary += 'black turns #'
        else:
            err_summary += 'white turns #'
        err_summary += str(step) + '\n' +                         'time:' + current_time + '\n'
        err_summary += '============ episode ' + str(self.ep+1) + ' ============\n'
        for row in range(WIDTH):
            for col in range(8):
                err_summary += '{:4}'.format(self.board[row][col])
            err_summary += '\n'
        self.err += err_summary
    
    # write error encounter to file 'err_report.txt'
    def err_summary(self):
        with open('err_report.txt', 'w') as fp:
            fp.write(self.err)
    # Return True if determine there is at least one legal move for next player 
    def Get_Valid_Moves(self, is_black):
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.is_legal_move([row, col], is_black):
                    return True
        return False
    # agent's final score = #(belonging color stones)
    def compute_score(self):
        (bscore, wscore) = (0,0)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.board[row][col] == BLACK:
                    bscore += 1
                elif self.board[row][col] == WHITE:
                    wscore += 1
        self.game_score.append([bscore, wscore])
        return bscore, wscore


# In[275]:


# 從 pos 開始，把 n 個坐標 視作爲 一個tuple
# n 決定 tuple 長度
# d 決定 tuple 衍生方向
# 回傳 list(整個 tuple 的所有坐標)
def gen_tuple(pos=[0,0], n = ALL_N_TUPLE, d = SOUTH):
    tup_list = []
    for t in range(n):
        tup_list.append(pos[:])
        pos[0] += d[0]
        pos[1] += d[1]
    return tup_list


# 30 of all-2 tuple
def tuple_set_one():
    # 2 tuple
    ALL_N_TUPLE = 2
    
    # 30 個 tuple
    tup_node = [[0,0] for i in range(4)]
    tup_node[0] = [[x,0] for x in range(1,4)] # 1 2 3
    tup_node[1] = [[x,1] for x in range(4)] # 0 1 2 3
    tup_node[2] = [[x,2] for x in range(4)]
    tup_node[3] = [[x,3] for x in range(4)]

    # SOUTH(下), SOUTHEAST（右下）
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
    return tuple_list


# In[472]:


import pickle
import random
# 隨機亂玩
class dummy():
    def __init__(self):
        pass
    def GetStep(self, board, is_black):
        self.board = board
        moves = self.Get_Valid_Moves(is_black)
        if moves:
            choice = random.randrange(len(moves))
            return moves[choice]
        else:
            return None
    # return set of possible moves
    def Get_Valid_Moves(self, is_black):
        moves = []
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.is_legal_move([row, col], is_black):
                    moves.append([row, col])
        return moves

    def is_legal_move(self, step, is_black):
        # determine whether an action from player is legal
        (row, col) = step
        # the position must be empty
        if self.board[row][col] != EMPTY or self.board[row][col] == CORNER:
            return False
        
        # inside 6x6
        if row > 0 and row < 7        and col > 0 and col < 7:
            return True
        
        # out of 8x8
        if row < 0 or col < 0         or row > 7 or col > 7:
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
                if row < 0 or col < 0                 or row > 7 or col > 7:
                    break

                if self.board[row][col] == EMPTY or self.board[row][col] == CORNER:
                    break
                if self.board[row][col] == who:
                    if flip:
                        # this edge placement is legal
                        return True
                    else:
                        break
                if self.board[row][col] == opponent:
                    flip = True
        return False
def show(board):

        for row in range(HEIGHT):
            for col in range(WIDTH):
                print('{:>4}'.format(board[row][col]), end='')
            print('')
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
    def __init__(self, load_file = None, save_file = None, name = 'Player', alpha = 0.5):
        self.load_file = load_file
        self.save_file = save_file
        self.name = name
        self.alpha = alpha
        if load_file:
            self.load_network()
    def save_network(self):
        if self.save_file:
            with open(self.save_file, 'wb') as fp:
                pickle.dump(self.weight, fp, protocol=pickle.HIGHEST_PROTOCOL)
    def load_network(self):
        with open(self.load_file, 'rb') as fp:
            self.weight = pickle.load(fp)
    def set_tuple(self, tuple_list, tuple_size):
        self.tuple_list = tuple_list
        
        # no init for weight if weight is loaded
        if self.load_file:
            return 0
        
        self.weight = []
        # every tuple has its own set of weight
        for i in range(len(tuple_list)):
            # combination of single tuple at size = 3**size 
            # init value at (-1, 1)
            self.weight.append([random.uniform(-1, 1) for x in range(3**tuple_size)])
    
    # 旋轉盤面 順時針90度
    def rotate(self, board):
        return [list(r) for r in zip(*board[::-1])]
    ##################################################################################
    def open_episode(self):
        self.epi = []
    def close_episode(self):
        self.epi = self.epi[::-1]
        err = self.alpha * (- self.value(self.epi[0]))
        self.update(self.epi[0], err)
        print('endgame:', err)
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
        self.epi.append(deepcopy(board))
        self.is_black = is_black
        
        moves = self.Get_Valid_Moves(is_black)
        (max_val, step) = (-9999, moves[0])
        if moves:
            for m in moves:
                self.board = deepcopy(board)
                self.board = self.set_and_flip(m, is_black)
                val = self.value(self.board)
                val += reward(self.board, is_black)
                if val > max_val:
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
        if row > 0 and row < 7        and col > 0 and col < 7:
            return True
        
        # out of 8x8
        if row < 0 or col < 0         or row > 7 or col > 7:
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
                if row < 0 or col < 0                 or row > 7 or col > 7:
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
                if row < 0 or col < 0                 or row > 7 or col > 7:
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


# In[475]:


import timeit
def play_game():
    # 棋盤與玩家
    global judger
    global black
    global white
    
    global error_encounter
    global NO_ERROR
    
    # 記錄輸贏
    global blackwin
    global whitewin
    global draw
    
    global total_bscore
    global total_wscore
    # black go first
    is_black = True
    pass_turn = False
    
    black.open_episode()
    #white.open_episode()
    
    while True:
        board = deepcopy(judger.board)
        
        start = timeit.default_timer()
        if is_black:
            # black player turn
            step = black.GetStep(board, is_black)
        else:
            # white player turn
            step = white.GetStep(board, is_black)
        end = timeit.default_timer()

        # no legal move at agent's perspective
        if step is None:
            who = 'BLACK' if is_black else 'WHITE'
            if is_black:
                print(black.Get_Valid_Moves(is_black))
            else:
                print(white.Get_Valid_Moves(is_black))
            print("Agent can't find a legal move ", who , ' turn')
            break

        # 出手大於 5 秒  
        if end-start > 5:
            judger.track_err('TLE', is_black, step)
            error_encounter += 1
            NO_ERROR = False
            print('TLE')
            break

        status = judger.place(step, is_black)
        
        # illegal placement
        if not status:
            judger.track_err('Illegal Move', is_black, step)
            error_encounter += 1
            NO_ERROR = False
            print('illegal move')
            break

        # switch player's turn
        is_black = not is_black
        
        # 判斷 next player 沒有 棋下 
        if not judger.Get_Valid_Moves(is_black):
            # 自動 pass turn
            is_black = not is_black
            
            # 兩位 players 同時沒有旗下才結束
            if not judger.Get_Valid_Moves(is_black):
                bscore, wscore = judger.compute_score()
                if bscore > wscore:
                    blackwin += 1
                elif wscore > bscore:
                    whitewin += 1
                else:
                    draw += 1
                total_bscore += bscore
                total_wscore += wscore
                break
                
    black.close_episode()
    #white.close_episode()
    judger.ep += 1


# In[479]:


# to simulate game and do training

from IPython.display import display, clear_output

alpha = 1/(30*8*2)
# black agent = 
black = agent('black.p', 'black.p', 'black_tuple_agent', alpha) # load and save on 'black.p'
# tuple set for black agent
tuple_list = tuple_set_one()
black.set_tuple(tuple_list, 2)

# white agent = 
white = dummy()#agent(None, 'white.p', 'white_tuple_agent', alpha)
# tuple set for white agent
tuple_list = tuple_set_one()
#white.set_tuple(tuple_list, 2)

# Params
# num of games to be played
NUM_GAMES = 100

# True: write every end game state to 'game_report.txt'
__GAME_RECORD__ = True
# True: write any TLE or illegal move to 'err_report.txt'
__ERR_RECORD__ = True

__SAVE_NET__ = True
__BLACK_TRAIN__ = True
__WHITE_TRAIN__ = False


# True: 黑白棋手每局對換身份, False：黑棋手永遠持黑棋
__SWITCH_SIDE__ = False

# init game variable
judger = Game()
error_encounter = 0
blackwin = 0 
whitewin = 0
draw = 0
total_bscore = 0
total_wscore = 0
start = timeit.default_timer()
for match in range(NUM_GAMES):
    judger.reset()
    NO_ERROR = True
    
    play_game()

    if NO_ERROR:
        # do backward training
        pass

    if __GAME_RECORD__:
        judger.save_match()
    
    # brief summary
    if True or match%50 == 0:
        clear_output(wait=True)
        print(black.name, ' wins:', blackwin )
        print('white', ' wins:', whitewin)
        print('A Tie:', draw)
        judger.show()
        
    # 黑白手互換
    if __SWITCH_SIDE__:
        tmp = black
        black = white
        white = tmp

        tmp = blackwin
        blackwin = whitewin
        whitewin = tmp
        
        tmp = __BLACK_TRAIN__
        __BLACK_TRAIN__ = __WHITE_TRAIN__
        __WHITE_TRAIN__ = tmp
end = timeit.default_timer()

print(bcolors.OKGREEN)
print('========== END ==========')
print('Total Game Played:', NUM_GAMES)
print(black.name, ' wins:', blackwin )
print('white', ' wins:', whitewin)
print('A Tie:', draw)
print('B:W', total_bscore, '-',total_wscore)
print('Time Taken:', end-start)

if __GAME_RECORD__:
    print('Game Summary...', end='')
    judger.summary()
    print('OK!')
if error_encounter:
    print(bcolors.WARNING, end='')
    print('Error(s) encounter:', error_encounter)
    if __ERR_RECORD__:
        print('Error Summary...', end='')
        judger.err_summary()
        print('OK!', bcolors.ENDC)
if __SAVE_NET__:
    print(bcolors.OKGREEN, end='')
    print('Saving Weight...', end='')
    if __BLACK_TRAIN__:
        black.save_network()
    if __WHITE_TRAIN__:
        white.save_network()
    print('OK!')
print('DONE!', bcolors.ENDC)

