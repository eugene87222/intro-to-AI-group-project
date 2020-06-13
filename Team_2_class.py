import os
import random
import STcpClient
from copy import deepcopy
from math import sqrt
from datetime import datetime, timedelta

INF = 1e10

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

class SearchingAgent():
    def __init__(self, is_black, duration, weight_piece, weight_edge, weight_move, algo='pvs'):
        self.is_black = is_black
        self.MAX_DEPTH = -1
        self.DURATION = duration
        self.WEIGHT_PIECE = weight_piece
        self.WEIGHT_EDGE = weight_edge
        self.WEIGHT_MOVE = weight_move
        self.ALGO = algo
        self.lifetime = None

    def OutOfBoard(self, pos, direction):
        new_r = pos[0] + direction[0]
        new_c = pos[1] + direction[1]
        if new_r<0 or new_r>=HEIGHT:
            return True, (new_r, new_c)
        if new_c<0 or new_c>=WIDTH:
            return True, (new_r, new_c)
        if new_r in [0, HEIGHT-1] and new_c in [0, WIDTH-1]:
            return True, (new_r, new_c)
        return False, (new_r, new_c)

    def IsValidMove(self, board, pos, direction, is_black):
        res = self.OutOfBoard(pos, direction)
        if not res[0]:
            next_pos = res[1]
        else:
            return False
        player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        if board[next_pos[0]][next_pos[1]] == opponent:
            while board[next_pos[0]][next_pos[1]] == opponent:
                res = self.OutOfBoard(next_pos, direction)
                if res[0]:
                    return False
                else:
                    next_pos = res[1]
            if board[next_pos[0]][next_pos[1]] == player:
                return True
        return False

    def GetValidMoves(self, board, is_black):
        moves = []
        player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        # upper edge ==============================================================
        if board[0][1] == EMPTY:
            for d in [SOUTH, SOUTHEAST, EAST]:
                if self.IsValidMove(board, (0, 1), d, is_black):
                    moves.append((0, 1))
                    break
        if board[0][2] == EMPTY:
            for d in [SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
                if self.IsValidMove(board, (0, 2), d, is_black):
                    moves.append((0, 2))
                    break
        if board[0][3] == EMPTY:
            for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
                if self.IsValidMove(board, (0, 3), d, is_black):
                    moves.append((0, 3))
                    break
        if board[0][4] == EMPTY:
            for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST, EAST]:
                if self.IsValidMove(board, (0, 4), d, is_black):
                    moves.append((0, 4))
                    break
        if board[0][5] == EMPTY:
            for d in [WEST, SOUTHWEST, SOUTH, SOUTHEAST]:
                if self.IsValidMove(board, (0, 5), d, is_black):
                    moves.append((0, 5))
                    break
        if board[0][6] == EMPTY:
            for d in [WEST, SOUTHWEST, SOUTH]:
                if self.IsValidMove(board, (0, 6), d, is_black):
                    moves.append((0, 6))
                    break
        # left edge ==============================================================
        if board[1][0] == EMPTY:
            for d in [EAST, SOUTHEAST, SOUTH]:
                if self.IsValidMove(board, (1, 0), d, is_black):
                    moves.append((1, 0))
                    break
        if board[2][0] == EMPTY:
            for d in [NORTHEAST, EAST, SOUTHEAST, SOUTH]:
                if self.IsValidMove(board, (2, 0), d, is_black):
                    moves.append((2, 0))
                    break
        if board[3][0] == EMPTY:
            for d in [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH]:
                if self.IsValidMove(board, (3, 0), d, is_black):
                    moves.append((3, 0))
                    break
        if board[4][0] == EMPTY:
            for d in [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH]:
                if self.IsValidMove(board, (4, 0), d, is_black):
                    moves.append((4, 0))
                    break
        if board[5][0] == EMPTY:
            for d in [NORTH, NORTHEAST, EAST, SOUTHEAST]:
                if self.IsValidMove(board, (5, 0), d, is_black):
                    moves.append((5, 0))
                    break
        if board[6][0] == EMPTY:
            for d in [NORTH, NORTHEAST, EAST]:
                if self.IsValidMove(board, (6, 0), d, is_black):
                    moves.append((6, 0))
                    break
        # lower edge ==============================================================
        if board[7][1] == EMPTY:
            for d in [NORTH, NORTHEAST, EAST]:
                if self.IsValidMove(board, (7, 1), d, is_black):
                    moves.append((7, 1))
                    break
        if board[7][2] == EMPTY:
            for d in [NORTHWEST, NORTH, NORTHEAST, EAST]:
                if self.IsValidMove(board, (7, 2), d, is_black):
                    moves.append((7, 2))
                    break
        if board[7][3] == EMPTY:
            for d in [WEST, NORTHWEST, NORTH, NORTHEAST, EAST]:
                if self.IsValidMove(board, (7, 3), d, is_black):
                    moves.append((7, 3))
                    break
        if board[7][4] == EMPTY:
            for d in [WEST, NORTHWEST, NORTH, NORTHEAST, EAST]:
                if self.IsValidMove(board, (7, 4), d, is_black):
                    moves.append((7, 4))
                    break
        if board[7][5] == EMPTY:
            for d in [WEST, NORTHWEST, NORTH, NORTHEAST]:
                if self.IsValidMove(board, (7, 5), d, is_black):
                    moves.append((7, 5))
                    break
        if board[7][6] == EMPTY:
            for d in [WEST, NORTHWEST, NORTH]:
                if self.IsValidMove(board, (7, 6), d, is_black):
                    moves.append((7, 6))
                    break
        # right edge ==============================================================
        if board[1][7] == EMPTY:
            for d in [WEST, SOUTHWEST, SOUTH]:
                if self.IsValidMove(board, (1, 7), d, is_black):
                    moves.append((1, 7))
                    break
        if board[2][7] == EMPTY:
            for d in [NORTHWEST, WEST, SOUTHWEST, SOUTH]:
                if self.IsValidMove(board, (2, 7), d, is_black):
                    moves.append((2, 7))
                    break
        if board[3][7] == EMPTY:
            for d in [NORTH, NORTHWEST, WEST, SOUTHWEST, SOUTH]:
                if self.IsValidMove(board, (3, 7), d, is_black):
                    moves.append((3, 7))
                    break
        if board[4][7] == EMPTY:
            for d in [NORTH, NORTHWEST, WEST, SOUTHWEST, SOUTH]:
                if self.IsValidMove(board, (4, 7), d, is_black):
                    moves.append((4, 7))
                    break
        if board[5][7] == EMPTY:
            for d in [NORTH, NORTHWEST, WEST, SOUTHWEST]:
                if self.IsValidMove(board, (5, 7), d, is_black):
                    moves.append((5, 7))
                    break
        if board[6][7] == EMPTY:
            for d in [NORTH, NORTHWEST, WEST]:
                if self.IsValidMove(board, (6, 7), d, is_black):
                    moves.append((6, 7))
                    break
        # central 6x6 =============================================================
        for r in range(1, HEIGHT-1):
            for c in range(1, WIDTH-1):
                if board[r][c] == EMPTY:
                    moves.append((r, c))
        return moves

    def CheckFlip(self, board, pos, direction, is_black):
        res = self.OutOfBoard(pos, direction)
        flip = []
        if not res[0]:
            pos = res[1]
        else:
            return False, []
        player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        if board[pos[0]][pos[1]] == opponent:
            while board[pos[0]][pos[1]] == opponent:
                flip.append(pos)
                res = self.OutOfBoard(pos, direction)
                if res[0]:
                    break
                else:
                    pos = res[1]
            if board[pos[0]][pos[1]] == player:
                return True, flip
        return False, []

    def PlaceAndFlip(self, board, pos, is_black):
        player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        new_board = deepcopy(board)
        new_board[pos[0]][pos[1]] = player
        for d in DIRECTIONS:
            res = self.CheckFlip(new_board, pos, d, is_black)
            if res[0]:
                for t in res[1]:
                    new_board[t[0]][t[1]] = player
        return new_board

    def Evaluate(self, board, is_black):
        player, opponent = (BLACK, WHITE) if is_black else (WHITE, BLACK)
        moves = self.GetValidMoves(board, is_black)
        player_edge = 0
        player_piece = 0
        opponent_edge = 0
        opponent_piece = 0
        opponent_moves = self.GetValidMoves(board, not is_black)
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
        score = piece_score*self.WEIGHT_PIECE + edge_score*self.WEIGHT_EDGE + len(moves)*self.WEIGHT_MOVE
        if self.is_black != is_black:
            score *= -1
        return score

    def Max(self, board, is_black, depth, lifetime, alpha, beta):
        if depth>self.MAX_DEPTH or datetime.now()>self.lifetime:
            score = self.Evaluate(board, is_black)
            return score
        next_moves = self.GetValidMoves(board, is_black)
        if len(next_moves) == 0:
            score = self.Evaluate(board, is_black)
            return score
        v = -INF
        for move in next_moves:
            new_board = self.PlaceAndFlip(board, move, is_black)
            v = max(v, self.Min(new_board, not is_black, depth+1, lifetime, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def Min(self, board, is_black, depth, lifetime, alpha, beta):
        if depth>self.MAX_DEPTH or datetime.now()>self.lifetime:
            score = self.Evaluate(board, is_black)
            return score
        next_moves = self.GetValidMoves(board, is_black)
        if len(next_moves) == 0:
            score = self.Evaluate(board, is_black)
            return score
        v = INF
        for move in next_moves:
            new_board = self.PlaceAndFlip(board, move, is_black)
            v = min(v, self.Max(new_board, not is_black, depth+1, lifetime, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def AlphaBetaPruning(self, board, is_black):
        depth = 0
        best_move = None
        max_score = -INF
        score = -INF
        moves = self.GetValidMoves(board, is_black)
        self.MAX_DEPTH = round(sqrt(72//len(moves))+0.5)
        for move in moves:
            new_board = self.PlaceAndFlip(board, move, is_black)
            score = self.Min(new_board, not is_black, depth, max_score ,INF)
            if score > max_score:
                max_score = score
                best_move = move
            if datetime.now() > self.lifetime:
                # print('moves 跑到一半')
                break
        return move

    def Negamax(self, board, is_black, depth, alpha, beta):
        if depth>self.MAX_DEPTH or datetime.now()>self.lifetime:
            score = self.Evaluate(board, is_black)
            return score
        next_moves = self.GetValidMoves(board, is_black)
        if len(next_moves) == 0:
            score = self.Evaluate(board, is_black)
            return score
        v = -INF
        best_move = None
        for move in next_moves:
            new_board = self.PlaceAndFlip(board, move, is_black)
            score = -self.Negamax(new_board, not is_black, depth+1, -beta, -alpha)
            if score > v:
                v = score
                best_move = move
            alpha = max(alpha, v)
            if alpha >= beta:
                break
            if datetime.now() > self.lifetime:
                # print('moves 跑到一半')
                break
        if depth == 0:
            return best_move
        else:
            return v

    def PVS(self, board, is_black, depth, alpha, beta):
        if depth>self.MAX_DEPTH or datetime.now()>self.lifetime:
            score = self.Evaluate(board, is_black)
            return score
        next_moves = self.GetValidMoves(board, is_black)
        if len(next_moves) == 0:
            score = self.Evaluate(board, is_black)
            return score
        best_move = None
        for i, move in enumerate(next_moves):
            new_board = self.PlaceAndFlip(board, move, is_black)
            if i == 0:
                score = -self.PVS(new_board, not is_black, depth+1, -beta, -alpha)
            else:
                score = -self.PVS(new_board, not is_black, depth+1, -alpha-1, -alpha)
                if alpha<score and score<beta:
                    score = -self.PVS(new_board, not is_black, depth+1, -beta, -score)
            if score > alpha:
                best_move = move
                alpha = score
            if alpha >= beta:
                break
            if datetime.now() > self.lifetime:
                # print('moves 跑到一半')
                break
        if depth == 0:
            return best_move
        else:
            return alpha

    def GetStep(self, board, is_black):
        self.lifetime = datetime.now() + timedelta(seconds=self.DURATION)
        if self.ALGO == 'minimax':
            move = self.AlphaBetaPruning(board, is_black)
        elif self.ALGO == 'negamax':
            moves = self.GetValidMoves(board, is_black)
            self.MAX_DEPTH = round(sqrt(72//len(moves))+0.5)
            move = self.Negamax(board, is_black, 0, -INF, INF)
        else:
            moves = self.GetValidMoves(board, is_black)
            self.MAX_DEPTH = round(sqrt(72//len(moves))+0.5)
            move = self.PVS(board, is_black, 0, -INF, INF)
        return move
