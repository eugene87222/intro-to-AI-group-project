# About game.py

- 模擬游戲過程
# n tuple network 參考
- TD(0)
- [1] 產生 all-2 tuple
- use CS department server to train
    - python 
    - exec(open("server_train.py").read())
    - Ctrl+c ( Stop program at any time )
    - white.save_network() ( due to interrupt of program, has to manually save )
# td_agent param
- black = agent(black_load = None, 
                 black_save = None,
                 white_load = None,
                 white_save = None,
                 alpha = 0.1, 
                 init_weight = False
- black_load/black_save: 先手 的 weight 路徑
- white_load..: 後手的 weight 路徑
# reference
- [1] https://arxiv.org/pdf/1406.1509.pdf
