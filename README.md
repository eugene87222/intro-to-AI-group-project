# About game.py

- 模擬游戲過程
# n tuple network 參考
- TD(0)
- [1] 產生 all-2 tuple
- [2] 產生 all-3 tuple 版本 對抗 all-2
- [3] all_3.p 是目前的結果， all_3_10000 與 all_3_20000 都是訓練 一萬場和兩萬場 暫存的weight

# td agent 參數
- white = agent(load_file, save_file, name, alpha, init_weight)
- load file: 現有 weight.p 的路徑
- save file: 完成訓練時，要存儲 weight.p 的檔案名字， white.save_network() 才會真正儲存
- name: 名字隨意
- alpha: learning rate 0~1之間， 目前 主要用 0.1
- init_weight: True- 無視 load file, 產生一組全新的 的 weight value 隨機分佈在[-1, 1]
# reference
- [1] https://arxiv.org/pdf/1406.1509.pdf
