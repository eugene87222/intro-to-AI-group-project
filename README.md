- Content
  - [About Team_2.py](#About_Team_2.py)
  - [Note](#Note)
  - [TODO](#TODO)

# About Team_2.py

- 用 [PVS](https://en.wikipedia.org/wiki/Principal_variation_search) 實作
- global variables
  - `INF`：隨便定的 infinity，目前設 1e10
  - `CORNER, EMPTY, BLACK, WHITE`：隨便給數字，增加 code readability 而已
  - `WIDTH, HEIGHT`：盤面大小，8x8
  - `NORTH, NORTHEAST, ..., DIRECTIONS`：各種移動方向，第一個與第二個值分別為 row 與 col 的移動方向

- `SearchAgent()`
  - attribute
    - `PLAYER`：agent 的身分（黑棋 or 白棋）
    - `MAX_DEPTH`：最大搜尋深度
    - `DURATION`：最大思考時間
    - `WEIGHT_PIECE`：權重
    - `WEIGHT_EDGE`：權重
    - `WEIGHT_MOVE`：權重
    - `LIFETIME`：now + `DURATION`
  - method
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
    - `PVS(board, is_black, depth, alpha, beta)`
      - https://en.wikipedia.org/wiki/Principal_variation_search

# Note

> 每組跑 50 遍，共 100 場對局

|參數|結果|
|-|-|

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
  - [x] [PVS](https://en.wikipedia.org/wiki/Principal_variation_search)
