# About Team_2.py

- `OutOfBoard(pos, direction)`
  - 檢查 `pos` 沿 `direction` 方向移動一步後是否超出棋盤

- `GetValidMove(board, pos, direction, is_black)`
  - 檢查 `pos` 沿 `direction` 方向移動是否能找到 valid move

- `GetValidMoves(board, is_black)`
  - check the whole board
  - if the cell is corner of opponent's piece -> 忽略該 cell
  - if the cell is empty and inside the central 6x6 area -> a valid move
  - if the cell is player's piece -> `GetValidMove`

- `Max(depth, lifetime, alpha, beta)`
  - 只有雛形

- `Min(depth, lifetime, alpha, beta)`
  - 只有雛形

- `AlphaBetaPruning()`
  - 還沒實作

# Note

Team_2.py 會開兩個目錄，output_black 跟 output_white，只是用來把對局過程中的盤面 output 成文字檔，debug 用的而已