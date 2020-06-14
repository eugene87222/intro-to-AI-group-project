WIDTH, HEIGHT = 8, 8
NORTH = [-1, 0]
NORTHEAST = [-1, 1]
EAST = [0, 1]
SOUTHEAST = [1, 1]
SOUTH = [1, 0]
SOUTHWEST = [1, -1]
WEST = [0, -1]
NORTHWEST = [-1, -1]
#################################################################################
# 從 pos 開始，把 n 個坐標 視作爲 一個tuple
# n 決定 tuple 長度
# d 決定 tuple 衍生方向
# 回傳 list(整個 tuple 的所有坐標)
def gen_tuple(pos=[0,0], n = 0, d = SOUTH):
    tup_list = []
    for t in range(n):
        tup_list.append(pos[:])
        pos[0] += d[0]
        pos[1] += d[1]
    return tup_list
    
# all-3 tuple in reference
def all_3_ref():
    ALL_N_TUPLE = 3

    tup_node = [ [] for i in range(4)] # row 0-3
    tup_node[0] = [[x,0] for x in range(1,3)] # 1 2
    tup_node[1] = [[x,1] for x in range(3)] # 0-2
    tup_node[2] = [[x,2] for x in range(3)]
    tup_node[3] = [[x,3] for x in range(3)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1-5
    tup_node[1] = [[x,1] for x in range(1,5)] # 1-4 
    tup_node[2] = [[x,2] for x in range(2,4)] # 2-3
    del tup_node[3]
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
# all-3 tuple customize version
def all_3_custom():
    ALL_N_TUPLE = 3
    
    tup_node = [ [] for i in range(4)] # row 0-3
    tup_node[0] = [[x,0] for x in range(1,3)] # 1 2
    tup_node[1] = [[x,1] for x in range(3)] # 0 1 2
    tup_node[2] = [[x,2] for x in range(3)]
    tup_node[3] = [[x,3] for x in range(3)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1-5
    tup_node[1] = [[x,1] for x in range(0,6)] # 0~5 
    tup_node[2] = [[x,2] for x in range(0,6)] # 0~5 
    tup_node[3] = [[x,3] for x in range(0,6)] # 0~5 
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
# all-2 tuple based on all-3 tuple of reference
def all_2_ref():
    ALL_N_TUPLE = 2
    
    tup_node = [ [] for i in range(4)]
    tup_node[0] = [[x,0] for x in range(1,4)] # 1-3
    tup_node[1] = [[x,1] for x in range(4)] # 0-3
    tup_node[2] = [[x,2] for x in range(4)]
    tup_node[3] = [[x,3] for x in range(4)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,6)] # 1-5
    tup_node[1] = [[x,1] for x in range(1,7)] # 1-6
    tup_node[2] = [[x,2] for x in range(2,6)] # 2-5 
    tup_node[3] = [[x,3] for x in range(2,6)]
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
# all-2 tuple customize
def all_2_custom():
    ALL_N_TUPLE = 2
    
    tup_node = [ [] for i in range(5)]
    tup_node[0] = [[x,0] for x in range(1,4)] # 1-3
    tup_node[1] = [[x,1] for x in range(4)] # 0-3
    tup_node[2] = [[x,2] for x in range(4)]
    tup_node[3] = [[x,3] for x in range(4)]
    
    tuple_list = []
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTH))
            
    tup_node[0] = [[x,0] for x in range(1,7)] # 1-6
    tup_node[1] = [[x,1] for x in range(0,7)] # 0-6
    tup_node[2] = [[x,2] for x in range(0,7)]
    tup_node[3] = [[x,3] for x in range(0,7)]
    tup_node[4] = [[x,4] for x in range(0,7)]
    
    for node in tup_node:
        for n in node:
            tuple_list.append(gen_tuple(n, ALL_N_TUPLE, SOUTHEAST))
        
    return tuple_list, ALL_N_TUPLE
