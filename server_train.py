#!/usr/bin/env python
# coding: utf-8

# In[1]:


import timeit
from copy import deepcopy

from td_agent import *
from othello import *
from Team_2 import *

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


# In[2]:


# 從 pos 開始，把 n 個坐標 視作爲 一個tuple
# n 決定 tuple 長度
# d 決定 tuple 衍生方向
# 回傳 list(整個 tuple 的所有坐標)
def gen_tuple(pos=[0,0], n = 0, d = SOUTH):
    tup_list = []
    for t in range(n):
        tup_list.append(pos[:])
        pos[0] += d[0]
        pos[1] += d[1]
    return tup_list

def diff_weight():
    for idx in range(len(white.weight)):
        w = white.weight[idx]
        b = black.weight[idx]
        print('----------------------',idx,'--------------------')
        for idx_2 in range(len(w)):
            print(w[idx_2], b[idx_2])

# all-3 tuple in reference
def tuple_set_two():
    # all-3 tuple of reference
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
    tup_node[2] = [[x,1] for x in range(2,4)] # 2 3
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
def tuple_set_three():
    # all-2 tuple based on all-3 tuple of reference
    ALL_N_TUPLE = 2
    
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
    tup_node[2] = [[x,1] for x in range(2,4)] # 2 3
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
def tuple_set_four():
    ALL_N_TUPLE = 15
    
    tuple_list = []
    for row in range(4):
        for col in range(4):
            if row == 0 and col == 0:
                continue
            tuple_list.append([row, col])
    return [tuple_list], ALL_N_TUPLE


# In[3]:


def play_game():
    # 棋盤與玩家
    global judger
    global black
    global white
    
    global __SWITCH_SIDE__
    global first_hand
    
    global error_encounter
    
    # 記錄輸贏
    global blackwin
    global whitewin
    global draw
    
    global total_bscore
    global total_wscore
    
    # black go first
    is_black = True
    pass_turn = False
    NO_ERROR = True
    
    if __SWITCH_SIDE__:
        if not first_hand:
            is_black = False
        first_hand = not first_hand
        
    if __BLACK_TRAIN__:
        black.open_episode()
    if __WHITE_TRAIN__:
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
        if Time_Limit_On and end-start > Time_Limit_Seconds:
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
        if __BLACK_TRAIN__:
            black.close_episode()
        if __WHITE_TRAIN__:
            white.close_episode()
    judger.ep += 1


# In[4]:


# to simulate game and do training
alpha = 0.1
init_weight = False

# =========================BLACK==================================
black = SearchingAgent(True, 10, 1, 100, 25, random_pick=True)

#black = agent('black_all_3.p', 'black_all_3.p', 'black_all_3', alpha, init_weight) # load and save on 'black.p'
# tuple set
#tuple_list, tuple_size = tuple_set_two()
#black.set_tuple(tuple_list, tuple_size)

# =========================WHITE==================================
white = agent('all_3_SA.p', 'all_3_SA_DEPTH=3.p', 'name', alpha, init_weight)
# tuple set 
tuple_list, tuple_size = tuple_set_two()
white.set_tuple(tuple_list, tuple_size)

__BLACK_TRAIN__ = False
__WHITE_TRAIN__ = True
__SAVE_NET__ = __WHITE_TRAIN__ or __BLACK_TRAIN__

# num of games to be played
NUM_GAMES = 100000

# True: 黑白棋手 先後手交替
__SWITCH_SIDE__ = True
first_hand = True
# False: 取消時間限制設定
Time_Limit_On = False
Time_Limit_Seconds = 5

# True: write every end game state to 'game_report.txt'
__GAME_RECORD__ = False
# True: write any TLE or illegal move to 'err_report.txt'
__ERR_RECORD__ = True


# In[5]:


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
    
    play_game()

    if __GAME_RECORD__:
        judger.save_match()
    
    # brief summary
    if True or match%50 == 0:
        print('black', ' wins:', blackwin )
        print('white', ' wins:', whitewin)
        print('A Tie:', draw)
        print('B:W', total_bscore, '-',total_wscore)
        #judger.show()

end = timeit.default_timer()

print('========== END ==========')
print('Total Game Played:', NUM_GAMES)
print('black', ' wins:', blackwin )
print('white', ' wins:', whitewin)
print('A Tie:', draw)
print('Time Taken:', end-start)

if __GAME_RECORD__:
    print('Game Summary...', end='')
    judger.summary()
    print('OK!')
if error_encounter:
    print('Error(s) encounter:', error_encounter)
    if __ERR_RECORD__:
        print('Error Summary...', end='')
        judger.err_summary()
        print('OK!')
if __SAVE_NET__:
    print('Saving Weight...', end='')
    if __BLACK_TRAIN__:
        black.save_network()
    if __WHITE_TRAIN__:
        white.save_network()
    print('OK!')
print('DONE!')

