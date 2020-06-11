#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# params
WHITE = 2
BLACK = 1
EMPTY = 0
CORNER = -1
# agent params
alpha = 0.5


# In[ ]:





# In[3]:


ALL_N_TUPLE = 2
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
    return tuple_list, ALL_N_TUPLE

# all-3 tuple in reference
def tuple_set_two():
    # all-3 tuple
    ALL_N_TUPLE = 3
    
    # 30 個 tuple 
    tup_node = [[0,0] for i in range(3)]
    tup_node[0] = [[x,0] for x in range(1,3)] # 1 2
    tup_node[1] = [[x,1] for x in range(3)] # 0 1 2
    tup_node[2] = [[x,2] for x in range(3)]
    
    
    # SOUTH(下), SOUTHEAST（右下）
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1 2 3 4 5
    tup_node[1] = [[x,1] for x in range(1,5)] # 1 2 3 4 
    tup_node[1] = [[x,1] for x in range(2,4)] # 2 3
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE


# In[4]:



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


# In[5]:


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
    white.open_episode()
    
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
    if NO_ERROR:
        black.close_episode()
        white.close_episode()
    judger.ep += 1


# In[9]:


# to simulate game and do training

from IPython.display import display, clear_output

from td_agent import *
from othello import *


alpha = 1/(30*8*2)

# black agent = 
black = agent('black.p', 'black.p', 'black_tuple_agent', alpha, True) # load and save on 'black.p'
# tuple set
tuple_list, tuple_size = tuple_set_one()
black.set_tuple(tuple_list, tuple_size)

# white agent = 
white = agent('white.p', 'white.p', 'white_tuple_agent', alpha, True)
# tuple set 
tuple_list, tuple_size = tuple_set_two()
white.set_tuple(tuple_list, tuple_size)

# Params
# num of games to be played
NUM_GAMES = 1000

# True: write every end game state to 'game_report.txt'
__GAME_RECORD__ = False
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


# In[ ]:




