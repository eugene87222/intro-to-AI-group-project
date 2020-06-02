# About Team_2.py

- 一堆 global variable
  - `INF`：隨便定的 infinity，目前設 1e10
  - `MAX_DEPTH`：最大搜尋深度，目前是 100 層
  - `CORNER, EMPTY, BLACK, WHITE`：隨便給數字，增加 code readability 而已
  - `WIDTH, HEIGHT`：盤面大小，8x8
  - `NORTH, NORTHEAST, ..., DIRECTIONS`：各種移動方向，第一個與第二個值分別為 row 與 col 的移動方向

- `OutOfBoard(pos, direction)`
  - 檢查 `pos` 沿 `direction` 方向移動一步後是否超出棋盤

- `GetValidMove(board, pos, direction, is_black)`
  - 檢查 `pos` 沿 `direction` 方向移動是否能找到 valid move

- `GetValidMoves(board, is_black)`
  - check the whole board
  - if the cell is corner of opponent's piece -> 忽略該 cell
  - if the cell is empty and inside the central 6x6 area -> a valid move
  - if the cell is player's piece -> `GetValidMove`

- `CheckFlip(board, pos, direction, is_black)`
  - 檢查目前的 `board` 以 `pos` 為出發點，沿 `direction` 方向前進，是否有 opponent 的 piece 可以翻面
  - return [是否有東西可翻面, 可翻面的座標(list)]

- `PlaceAndFlip(board, pos, is_black)`
  - place a piece at `pos`, then call `CheckFlip`

- `Evaluate(board, is_black)`
  - calculate the score of current board
  - things being taken into account
    - number of pieces on the edge (weight 1.5)
    - number of available moves (weight 0)
    - number of total pieces (weight 2)

- `Max(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 max

- `Min(board, is_black, depth, lifetime, alpha, beta)`
  - minimax 的 min

- `AlphaBetaPruning(board, is_black, lifetime)`
  - alpha-beta pruning
  - lifetime 目前給 4.4 秒

# Note

~~Team_2.py 會開兩個目錄，output_black 跟 output_white，只是用來把對局過程中的盤面 output 成文字檔，debug 用的而已~~ 暫時關掉