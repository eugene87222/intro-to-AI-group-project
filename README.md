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

#
black vs white             		win			score		
-----------------------------

all_3

ref - ref			    	15:80			2418:3582

custom - custom				51:47			3088:2912


ref - custom				15:83			2229:3771

custom - ref				29:64			2753:3247

-----------------------------

all_2

ref - ref				    29:69			2618:3382

custom - custom				28:68			2738:3254


ref - custom				34:62			2761:3237

custom - ref				39:60			2548:3451 (黑色一開始領先，後來被趕上)


----------------------------

all_3 vs all 2
ref - ref				    57:41			3145:2853

ref - custom				60:34			3364:2627


all_2 vs all_3

ref - ref				    8:90			 2065:3933

ref - custom				24：72			2391：3609



# reference
- [1] https://arxiv.org/pdf/1406.1509.pdf
