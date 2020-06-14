import timeit
from copy import deepcopy

from td_agent import *
from othello import *
from Team_2 import *
from tuple_generator import *

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

def diff_weight():
    print('w:b')
    for idx in range(len(white.weight)):
        w = white.white_weight[idx]
        b = black.black_weight[idx]
        print('----------------------',idx,'--------------------')
        for idx_2 in range(len(w)):
            print(w[idx_2], b[idx_2])

###############################################################
# to simulate game and do training
###############################################################
alpha = 0.1
init_weight = False
black_tset, black_n_size = all_3_ref()
white_tset, white_n_size = all_3_ref()
black_fn = 'all_3_ref_black.p'
white_fn = 'all_3_ref_white.p'
__BLACK_TRAIN__ = True
__WHITE_TRAIN__ = True
# num of games to be played
NUM_GAMES = 1#0**10
###############################################################
# =========================BLACK==================================
black = agent(black_load = black_fn,
              black_save = black_fn,
              white_load = None,
              white_save = None,
              alpha = alpha,
              init_weight = init_weight)
black.set_tuple(black_tset, black_n_size)

# =========================WHITE==================================
white = agent(black_load = None,
              black_save = None,
              white_load = white_fn,
              white_save = white_fn,
              alpha = alpha,
              init_weight = init_weight)
# tuple set 
white.set_tuple(white_tset, white_n_size)
# ===============================================================
##############################################################################

# False: 取消時間限制設定
Time_Limit_On = False
Time_Limit_Seconds = 5

# True: write every end game state to 'game_report.txt'
__GAME_RECORD__ = False
# True: write any TLE or illegal move to 'err_report.txt'
__ERR_RECORD__ = True

##############################################################################

# init game variable
judger = Game()
error_encounter = 0
blackwin = 0 
whitewin = 0
draw = 0
total_bscore = 0
total_wscore = 0

#############################################################################
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
        print('in total score, B:W', total_bscore, '-',total_wscore)
        #judger.show()

end = timeit.default_timer()
#############################################################################
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
if __BLACK_TRAIN__:
    black.save_network()
if __WHITE_TRAIN__:
    white.save_network()
print('DONE!')


