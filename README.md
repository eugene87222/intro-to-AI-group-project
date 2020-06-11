- Content
  - [About Team_2.py](#About_Team_2.py)
  - [Note](#Note)
  - [TODO](#TODO)

# About Team_2.py

- 用 minimax 實作 AI
- 一堆 global variable
  - `INF`：隨便定的 infinity，目前設 1e10
  - `MAX_DEPTH`：最大搜尋深度，目前設定為 round(sqrt(72/目前可放置的位置總數) + 0.5)
  - `DURATION`：思考時間，目前給 4.9 秒
  - `WEIGHT_PIECE, WEIGHT_EDGE, WEIGHT_MOVE`：各種權重
  - `CORNER, EMPTY, BLACK, WHITE`：隨便給數字，增加 code readability 而已
  - `WIDTH, HEIGHT`：盤面大小，8x8
  - `NORTH, NORTHEAST, ..., DIRECTIONS`：各種移動方向，第一個與第二個值分別為 row 與 col 的移動方向

- `OutOfBoard(pos, direction)`
  - 檢查 `pos` 沿 `direction` 方向移動一步後是否超出棋盤

- `IsValidMove(board, pos, direction, is_black)`
  - 如果把棋子下在 `pos`，並檢查沿 `direction` 方向是否能把敵方的棋子 flip

- `GetValidMoves(board, is_black)`
  - central 6x6 的位置只要是 `EMPTY` 就是 valid move
  - 檢查四條邊有沒有 valid move，原本可以用 for-loop 就好，但為了減少搜尋時間所以把所有情況展開個別處理

- `CheckFlip(board, pos, direction, is_black)`
  - 檢查目前的 `board` 以 `pos` 為出發點，沿 `direction` 方向前進，是否有 opponent 的 piece 可以 flip
  - return 是否有東西可 flip, 所有可 flip 的座標

- `PlaceAndFlip(board, pos, is_black)`
  - place a piece at `pos`, then call `CheckFlip`

- `Evaluate(board, is_black)`
  - calculate the score of current board
  - things being taken into account
    - number of pieces on the edge
    - number of available moves
    - number of total pieces
    - 權重比較請見 [Note](#Note)

- `Max(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 max

- `Min(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 min

- `AlphaBetaPruning(board, is_black, lifetime)`
  - alpha-beta pruning

# Note

> 每組跑 20 遍，共 40 場對局
|參數|結果|
|-|-|
|ALGO = negamax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 1.5|我方勝場：31<br/>平手：3<br/>我方勝率：77.5%<br/>對方勝率：15.0%|
|ALGO = negamax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.8|我方勝場：29<br/>平手：1<br/>我方勝率：72.5%<br/>對方勝率：25.0%|
|ALGO = negamax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.5<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.0|我方勝場：27<br/>平手：2<br/>我方勝率：67.5%<br/>對方勝率：27.5%|
|ALGO = negamax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.8<br/>WEIGHT_EDGE = 1.6<br/>WEIGHT_MOVE = 1.2|我方勝場：27<br/>平手：2<br/>我方勝率：67.5%<br/>對方勝率：27.5%|
|ALGO = pvs<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 1.5|我方勝場：25<br/>平手：1<br/>我方勝率：62.5%<br/>對方勝率：35.0%|
|ALGO = pvs<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.8|我方勝場：30<br/>平手：1<br/>我方勝率：75.0%<br/>對方勝率：22.5%|
|ALGO = pvs<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.5<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.0|我方勝場：36<br/>平手：0<br/>我方勝率：90.0%<br/>對方勝率：10.0%|
|ALGO = pvs<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.8<br/>WEIGHT_EDGE = 1.6<br/>WEIGHT_MOVE = 1.2|我方勝場：28<br/>平手：4<br/>我方勝率：70.0%<br/>對方勝率：20.0%|
|ALGO = minimax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 1.5|我方勝場：28<br/>平手：3<br/>我方勝率：70.0%<br/>對方勝率：22.5%|
|ALGO = minimax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 2.0<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.8|我方勝場：25<br/>平手：3<br/>我方勝率：62.5%<br/>對方勝率：30.0%|
|ALGO = minimax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.5<br/>WEIGHT_EDGE = 1.5<br/>WEIGHT_MOVE = 1.0|我方勝場：33<br/>平手：1<br/>我方勝率：82.5%<br/>對方勝率：15.0%|
|ALGO = minimax<br/>DURATION = 4.96<br/>WEIGHT_PIECE = 1.8<br/>WEIGHT_EDGE = 1.6<br/>WEIGHT_MOVE = 1.2|我方勝場：32<br/>平手：2<br/>我方勝率：80.0%<br/>對方勝率：15.0%|

# TODO

- [x] GetValidMove
- [ ] 想 evaluate function
  - 考慮的東西
    - 四條邊上棋子的數量
    - 棋子總數
    - valid moves 的數量
  - 權重比較請見 [Note](#Note)
  - [ ] 權重可能還要修改
  - [ ] 想想還有沒有什麼東西可以加入 evaluation function
- [x] minimax algorithm
- [x] alpha-beta pruning
- [ ] 有沒有其他加速方式，讓搜尋深度可以加大
