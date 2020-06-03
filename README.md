# About Team_2.py

- 一堆 global variable
  - `INF`：隨便定的 infinity，目前設 1e10
  - `MAX_DEPTH`：最大搜尋深度
  - `DURATION`：思考時間，單位為秒
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
    - 權重比較請見[Note](#Note)

- `Max(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 max

- `Min(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 min

- `AlphaBetaPruning(board, is_black, lifetime)`
  - alpha-beta pruning

# Note

> 每組實驗跑 20 次，總共有 40 場對局

```
MAX_DEPTH = 4
DURATION = 4.5
WEIGHT_PIECE = 2.0
WEIGHT_EDGE = 1.5
WEIGHT_MOVE = 1.8
```
- 我方勝場：26
- 平手：1
- 勝率：65.0%

---

```
MAX_DEPTH = 4
DURATION = 4.6
WEIGHT_PIECE = 2.0
WEIGHT_EDGE = 1.5
WEIGHT_MOVE = 1.8
```
- 我方勝場：27
- 平手：3
- 勝率：67.5%
