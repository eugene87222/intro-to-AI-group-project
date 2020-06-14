from copy import deepcopy
import time
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
                if row < 0 or col < 0 \
                or row > 7 or col > 7:
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
                # move one step foward in Direction d
                row += d[0]
                col += d[1]
                
                # out of bound
                if row < 0 or col < 0 \
                or row > 7 or col > 7:
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
                header = '============ episode ' + str(e+1) + ' ============ B:W-' + \
                         str(score[0]) + ':' + str(score[1]) + '\n'
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
        err_summary += str(step) + '\n' + \
                        'time:' + current_time + '\n'
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