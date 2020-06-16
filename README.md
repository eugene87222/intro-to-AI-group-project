- Content
  - [SA.py](#SA.py)
  - [Team_2.py](#Team_2.py)
  - [Note](#Note)
  - [TODO](#TODO)

# SA.py

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

# Team_2.py

- 詳細 code 請參考 reinforcement 與 td_agent_dev 兩個 branch
- 將訓練好的 weights 用於對局

# weight folder

- 利用 reinforcement learning - TD learning 學習出來的 weights
- 有四個本版：訓練 10 萬、15 萬、20 萬、25 萬場的 weights
- `.p` 檔名開頭的 `all_{數字}`
  - `all_2`：使用 2-tuple 訓練
  - `all_3`：使用 3-tuple 訓練
- `.p` 檔名中間的 `ref`、`custom`
  - `ref`：參考 paper 所實作的 networks
  - `custom`：基於 `ref` 上另外添加一些資訊的 networks
- `.p` 檔名末端的 `black`、`white`
  - `black`：針對先手的 weights（黑棋先下）
  - `white`：針對後手的 weights

# Note

> SA.py 跟助教提供的 AI 對局的結果  
> 對局 100 場對
> 對於相同 score 的 move -> 選擇第一個走訪的

|參數|結果|
|-|-|
|DURATION = 4.98<br/>WEIGHT_PIECE = 1.0<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 10.0|我方勝場：61<br/>平手：6<br/>我方勝率：61.0%<br/>對方勝率：33.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 0.1<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 10.0|我方勝場：74<br/>平手：6<br/>我方勝率：74.0%<br/>對方勝率：20.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 10.0<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 50.0|我方勝場：69<br/>平手：4<br/>我方勝率：69.0%<br/>對方勝率：27.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 50.0<br/>WEIGHT_MOVE = 1.0|我方勝場：54<br/>平手：11<br/>我方勝率：54.0%<br/>對方勝率：35.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 50.0|我方勝場：58<br/>平手：8<br/>我方勝率：58.0%<br/>對方勝率：34.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 10.0|我方勝場：49<br/>平手：5<br/>我方勝率：49.0%<br/>對方勝率：46.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 10.0<br/>WEIGHT_MOVE = 1.0|我方勝場：60<br/>平手：3<br/>我方勝率：60.0%<br/>對方勝率：37.0%|

---

> SA.py 跟助教提供的 AI 對局的結果  
> 對局 100 場對
> 對於相同 score 的 move -> 隨機挑一個  
> 看起來沒有比較好

|參數|結果|
|-|-|
|DURATION = 4.98<br/>WEIGHT_PIECE = 0.1<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 10.0|我方勝場：57<br/>平手：3<br/>我方勝率：57.0%<br/>對方勝率：40.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 50.0<br/>WEIGHT_MOVE = 1.0|我方勝場：46<br/>平手：8<br/>我方勝率：46.0%<br/>對方勝率：46.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 50.0|我方勝場：51<br/>平手：6<br/>我方勝率：51.0%<br/>對方勝率：43.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 1.0<br/>WEIGHT_MOVE = 10.0|我方勝場：55<br/>平手：7<br/>我方勝率：55.0%<br/>對方勝率：38.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 100.0<br/>WEIGHT_EDGE = 10.0<br/>WEIGHT_MOVE = 1.0|我方勝場：47<br/>平手：6<br/>我方勝率：47.0%<br/>對方勝率：47.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 1.0<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 10.0|我方勝場：49<br/>平手：7<br/>我方勝率：49.0%<br/>對方勝率：44.0%|
|DURATION = 4.98<br/>WEIGHT_PIECE = 10.0<br/>WEIGHT_EDGE = 100.0<br/>WEIGHT_MOVE = 50.0|我方勝場：54<br/>平手：4<br/>我方勝率：54.0%<br/>對方勝率：42.0%|

<style>
table {
    width:100%;
}
</style>

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
