# About game.py

- 模擬游戲過程
# n tuple network 參考
- TD(0)
- [1] 產生 all-2 tuple
- 目前 weight 數值在 backward training 會爆掉， 檢查中
  - 修改 learning rate 折扣方式，大概是 python 小數點 乘法存在bug
    - err *= 1/alpha -> err /= alpha
    - 修改後 weight 成長曲綫比較正常
- [2] 產生 all-3 tuple 版本 對抗 all-2 training 中...
# reference
- [1] https://arxiv.org/pdf/1406.1509.pdf
