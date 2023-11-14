from collections import OrderedDict
import random
import numpy as np

# For 4th implementation
size_table = 64
lg2_size_table = 6

hash_size = 20
feature_dimension = 100
np.random.seed(11414)
random_projection_matrix = np.random.randn(hash_size, feature_dimension)
hash_bits = (random_projection_matrix >= 0).astype(int)

def dot_projection(vec_base, vec_history):
    # vec_base is the base projection vector
    # vec_history is the branch history
    assert(len(vec_base) == len(vec_history))
    sum_tmp = 0
    for i in range(len(vec_base)):
        sum_tmp += 1 if ((vec_base[i] - 0.5) * (int(vec_history[i]) - 0.5)) > 0 else 0
    return 1 if sum_tmp > len(vec_base) / 2 else 0

def lsh_hash(projection_matrix, vec_history):
    lht_addr = 0
    for i in range(len(projection_matrix)):
        bit_i = dot_projection(projection_matrix[i], vec_history)
        lht_addr = (lht_addr << 1) + bit_i
    return lht_addr

# generate a fake history for testing
# history_fake = '0101110011101011110100001011110001110000110111101100110111101000001111011100001110111000000010100101'
# for i in range(feature_dimension):
#     history_fake += str(random.randint(0, 1))

# print(history_fake, lsh_hash(random_projection_matrix, history_fake))

def hamming(his1, his2):
    assert(len(his1) == len(his2))
    sum_h = 0
    for i in range(len(his1)):
        if his1[i] != his2[i]:
            sum_h += 1
    return sum_h

hot_miss = 0
hot_hit = 0
pc_history = []
max_pc_num = 100 # how many hot pcs to record for each period
real_num_his = [] # record how many pcs are really recorded, because sometimes only 1~2 pcs show up in that period
def preprocess_branch_misses(br_pc, insn_cnt):
    global hot_miss
    global hot_hit
    ordered = sorted(br_pc.items(), key=lambda i: i[1]["miss"], reverse=True)

    tmp_str = ''
    total_cnt = 0
    for k,v in ordered:
        # store first max_pc_num pcs into pc history
        if total_cnt < max_pc_num:
            hot_miss += v['miss']
            hot_hit += v['hit']
            print(hex(k), v)
            pc_history.append({'pc': k, 'local_his': '', 'table': {}, 'local_his_long': ''})
            total_cnt += 1
    real_num_his.append(total_cnt)
    # print(total_cnt)
    # assert(total_cnt == pc_num)

# only use local history
hot_miss_2 = 0
hot_hit_2 = 0
extra_miss_2 = 0
def process_hot_misses(pc_history_index, br_pc, taken, miss_hit, table_index):
    global hot_miss_2
    global hot_hit_2
    global extra_miss_2
    length_local = 64
    length_long = 1024
    ####### 7th Implementation:
    # Using global history
    if br_pc == pc_history[pc_history_index]['pc'] and len(global_his) == global_his_len:
        pattern = global_his
        pattern = br_pc ^ (int(global_his[64:])) ^ (int(global_his[0:63]))
        if pattern in pc_history[table_index]['table'] and len(global_his) == global_his_len:
            if pc_history[table_index]['table'][pattern] != taken:
                hot_miss_2 += 1
                pc_history[table_index]['table'][pattern] = taken
                if miss_hit == 'H':
                    extra_miss_2 += 1
            else:
                hot_hit_2 += 1
                if miss_hit == 'M':
                    extra_miss_2 += -1
        else:
            if miss_hit == 'M':
                hot_miss_2 += 1
                # Only update local history table if original BP is a miss
                # if (len(pc_history[table_index]['table']) < 1000) and len(global_his) == global_his_len:
                if len(global_his) == global_his_len:
                    pc_history[table_index]['table'][pattern] = taken
            else:
                hot_hit_2 += 1
    ####### End of 7th implementation
    ####### Sixth Implementation:
    # Combine all pc_history into one table
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if len(pattern) == length_local:
    #         x = int(pattern, 2)
    #         pattern = x ^ (br_pc >> 2)
    #         # pattern = (x ^ (x >> 16) ^ (x >> 32) ^ (x >> 48)) & 0xffff
    #         # pattern = (x ^ (x >> 10) ^ (x >> 20) ^ (x >> 30) ^ (x >> 40) ^ (x >> 50)) & 0x3ff
    #         # pattern = (x ^ (x >> 10) ^ (x >> 20) ^ (x >> 30) ^ (x >> 40) ^ (x >> 50) ^ (x >> 60) ^ (x >> 70) ^ (x >> 80) ^ (x >> 90)) & 0x3ff
    #         # print(pattern)
    #     if pattern in pc_history[table_index]['table'] and len(pc_history[pc_history_index]['local_his']) == length_local:
    #         if pc_history[table_index]['table'][pattern] != taken:
    #             hot_miss_2 += 1
    #             pc_history[table_index]['table'][pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #             # Only update local history table if original BP is a miss
    #             if (len(pc_history[table_index]['table']) < 1000 and len(pc_history[pc_history_index]['local_his']) == length_local):
    #                 pc_history[table_index]['table'][pattern] = taken
    #         else:
    #             hot_hit_2 += 1
    ####### End of Sixth implementation
    ####### Fifth Implementation:
    # # first check if this is in the hot miss addresses
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if len(pc_history[pc_history_index]['local_his']) < length_local:
    #         # generate 0s to have total 100 bits 
    #         zeros_tmp = ''
    #         for i in range(length_local - len(pc_history[pc_history_index]['local_his'])):
    #             zeros_tmp += '0'
    #         pattern = zeros_tmp + pattern
    #     hash_pattern = lsh_hash(random_projection_matrix, pattern)
    #     if hash_pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][hash_pattern] != taken:
    #             hot_miss_2 += 1
    #             pc_history[pc_history_index]['table'][hash_pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #             # Only update local history table if original BP is a miss
    #             if (len(pc_history[pc_history_index]['table']) < 500):
    #                 pc_history[pc_history_index]['table'][hash_pattern] = taken
    #         else:
    #             hot_hit_2 += 1
    ####### End of Fifth implementation
    ####### Forth Implementation:
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his'][0:lg2_size_table]
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['local_his'] == pc_history[pc_history_index]['table'][pattern]['tag']:
    #             if pc_history[pc_history_index]['table'][pattern]['t'] != taken:
    #                 hot_miss_2 += 1
    #                 pc_history[pc_history_index]['table'][pattern]['t'] = taken
    #                 if miss_hit == 'H':
    #                     extra_miss_2 += 1
    #             else:
    #                 hot_hit_2 += 1
    #                 if miss_hit == 'M':
    #                     extra_miss_2 += -1
    #         else:
    #             if miss_hit == 'M':
    #                 hot_miss_2 += 1
    #                 # Only update local history table if original BP is a miss
    #                 pc_history[pc_history_index]['table'][pattern] = {'tag': pc_history[pc_history_index]['local_his'], 't': taken}
    #             else:
    #                 hot_hit_2 += 1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #             # Only update local history table if original BP is a miss
    #             pc_history[pc_history_index]['table'][pattern] = {'tag': pc_history[pc_history_index]['local_his'], 't': taken}
    #         else:
    #             hot_hit_2 += 1
    ####### End of Forth Implementation
    ####### Third Implementation:
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if len(pc_history[pc_history_index]['local_his']) < length_local:
    #         # generate 0s to have total 100 bits 
    #         zeros_tmp = ''
    #         for i in range(length_local - len(pc_history[pc_history_index]['local_his'])):
    #             zeros_tmp += '0'
    #         pattern = zeros_tmp + pattern
    #     hash_pattern = lsh_hash(random_projection_matrix, pattern)
    #     if hash_pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][hash_pattern] != taken:
    #             hot_miss_2 += 1
    #             pc_history[pc_history_index]['table'][hash_pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #             # Only update local history table if original BP is a miss
    #             pc_history[pc_history_index]['table'][hash_pattern] = taken
    #         else:
    #             hot_hit_2 += 1
    ####### End of Third Implementation
    ####### Second implementation
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     pattern_idx = pc_history[pc_history_index]['local_his_long'][:-1].rfind(pattern)
    #     if len(pc_history[pc_history_index]['local_his']) >= length_local and pattern_idx > 0 and pattern_idx + length_local < len(pc_history[pc_history_index]['local_his_long']):
    #         if pc_history[pc_history_index]['local_his_long'][pattern_idx + length_local] != taken:
    #             hot_miss_2 += 1
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #         pc_history[pc_history_index]['table'][pattern] = taken
    ####### End of Second Implementation
    ####### Original Implementation:
    # first check if this is in the hot miss addresses
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     # try to find hamming distance < 1:
    #     # if bool(pc_history[pc_history_index]['table']):
    #     #     for key in pc_history[pc_history_index]['table']:
    #     #         if hamming(pattern, key) < 2:
    #     #             pattern = key
    #     #             break
    #     # end of hamming distance
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][pattern] != taken:
    #             hot_miss_2 += 1
    #             pc_history[pc_history_index]['table'][pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_2 += 1
    #             # Only update local history table if original BP is a miss
    #             if (len(pc_history[pc_history_index]['table']) < 1000 and len(pattern) == length_local):
    #                 pc_history[pc_history_index]['table'][pattern] = taken
    #         else:
    #             hot_hit_2 += 1
    ####### End of Original implementation
        # else:
        #     pattern = pc_history[pc_history_index]['local_his']
        #     if pattern in pc_history[pc_history_index]['table']:
        #         if pc_history[pc_history_index]['table'][pattern] != taken:
        #             hot_miss_2 += 1
        #             pc_history[pc_history_index]['table'][pattern] = taken
        #         else:
        #             hot_hit_2 += 1
        if len(pc_history[pc_history_index]['local_his_long']) < length_long:
            pc_history[pc_history_index]['local_his_long'] += taken
        else:
            pc_history[pc_history_index]['local_his_long'] = pc_history[pc_history_index]['local_his_long'][1:] + taken
        if len(pc_history[pc_history_index]['local_his']) < length_local:
            pc_history[pc_history_index]['local_his'] += taken
        else:
            pc_history[pc_history_index]['local_his'] = pc_history[pc_history_index]['local_his'][1:] + taken


# Reload
hot_miss_3 = 0
hot_hit_3 = 0
extra_miss_3 = 0 # More misses due to this implementation, possibly negative
def reload_hot_misses(pc_history_index, br_pc, taken, miss_hit, table_index):
    global hot_miss_3
    global hot_hit_3
    global extra_miss_3
    length_local = 64
    ####### 7th Implementation:
    # Using global history
    if br_pc == pc_history[pc_history_index]['pc'] and len(global_his) == global_his_len:
        pattern = global_his
        pattern = br_pc ^ (int(global_his[64:])) ^ (int(global_his[0:63]))
        if pattern in pc_history[table_index]['table'] and len(global_his) == global_his_len:
            if pc_history[table_index]['table'][pattern] != taken:
                hot_miss_3 += 1
                pc_history[table_index]['table'][pattern] = taken
                if miss_hit == 'H':
                    extra_miss_3 += 1
            else:
                hot_hit_3 += 1
                if miss_hit == 'M':
                    extra_miss_3 += -1
        else:
            if miss_hit == 'M':
                hot_miss_3 += 1
                # Only update local history table if original BP is a miss
                # if (len(pc_history[table_index]['table']) < 1000 and len(pc_history[pc_history_index]['local_his']) == length_local):
                # if (len(global_his) == length_local):
                #     pc_history[table_index]['table'][pattern] = taken
            else:
                hot_hit_3 += 1
    ####### End of 7th implementation
    ####### Sixth Implementation:
    # Combine all pc_history into one table
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if len(pattern) == length_local:
    #         x = int(pattern, 2)
    #         pattern = x ^ (br_pc >> 2)
    #         # pattern = (x ^ (x >> 16) ^ (x >> 32) ^ (x >> 48)) & 0xffff
    #         # pattern = (x ^ (x >> 10) ^ (x >> 20) ^ (x >> 30) ^ (x >> 40) ^ (x >> 50)) & 0x3ff
    #         # pattern = (x ^ (x >> 10) ^ (x >> 20) ^ (x >> 30) ^ (x >> 40) ^ (x >> 50) ^ (x >> 60) ^ (x >> 70) ^ (x >> 80) ^ (x >> 90)) & 0x3ff
    #     if pattern in pc_history[table_index]['table'] and len(pc_history[pc_history_index]['local_his']) == length_local:
    #         if pc_history[table_index]['table'][pattern] != taken:
    #             hot_miss_3 += 1
    #             pc_history[table_index]['table'][pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_3 += 1
    #         else:
    #             hot_hit_3 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_3 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_3 += 1
    #             # Only update local history table if original BP is a miss
    #             # if (len(pc_history[table_index]['table']) < 1000 and len(pattern) == length_local):
    #             #     pc_history[table_index]['table'][pattern] = taken
    #         else:
    #             hot_hit_3 += 1
    ####### End of Sixth implementation
    ####### Forth Implementation:
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his'][0:lg2_size_table]
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['local_his'] == pc_history[pc_history_index]['table'][pattern]['tag']:
    #             if pc_history[pc_history_index]['table'][pattern]['t'] != taken:
    #                 hot_miss_3 += 1
    #                 pc_history[pc_history_index]['table'][pattern]['t'] = taken
    #                 if miss_hit == 'H':
    #                     extra_miss_3 += 1
    #             else:
    #                 hot_hit_3 += 1
    #                 if miss_hit == 'M':
    #                     extra_miss_3 += -1
    #         else:
    #             if miss_hit == 'M':
    #                 hot_miss_3 += 1
    #                 # Only update local history table if original BP is a miss
    #                 # pc_history[pc_history_index]['table'][pattern] = {'tag': pc_history[pc_history_index]['local_his'], 't': taken}
    #             else:
    #                 hot_hit_3 += 1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_3 += 1
    #             # Only update local history table if original BP is a miss
    #             # pc_history[pc_history_index]['table'][pattern] = {'tag': pc_history[pc_history_index]['local_his'], 't': taken}
    #         else:
    #             hot_hit_3 += 1
    ####### End of Forth Implementation
    ####### Third / Fifth Implementation
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if len(pc_history[pc_history_index]['local_his']) < length_local:
    #         # generate 0s to have total 100 bits 
    #         zeros_tmp = ''
    #         for i in range(length_local - len(pc_history[pc_history_index]['local_his'])):
    #             zeros_tmp += '0'
    #         pattern = zeros_tmp + pattern
    #     hash_pattern = lsh_hash(random_projection_matrix, pattern)
    #     if hash_pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][hash_pattern] != taken:
    #             hot_miss_3 += 1
    #             pc_history[pc_history_index]['table'][hash_pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_3 += 1
    #         else:
    #             hot_hit_3 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_3 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_3 += 1
    #         else:
    #             hot_hit_3 += 1
    ####### End of Third / Fifth Implementation
    ####### Second Implementation
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     pattern_idx = pc_history[pc_history_index]['local_his_long'][:-1].rfind(pattern)
    #     if len(pc_history[pc_history_index]['local_his']) >= length_local and pattern_idx > 0 and pattern_idx + length_local < len(pc_history[pc_history_index]['local_his_long']):
    #         if pc_history[pc_history_index]['local_his_long'][pattern_idx + length_local] != taken:
    #             hot_miss_3 += 1
    #             if miss_hit == 'H':
    #                 extra_miss_3 += 1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_3 += 1
    #         else:
    #             hot_hit_3 += 1
    ####### End of Second Implementation
    ####### First Implementation
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     # if pattern in pc_history[pc_history_index]['table']:
    #     # try to find hamming distance < 1:
    #     # if bool(pc_history[pc_history_index]['table']):
    #     #     for key in pc_history[pc_history_index]['table']:
    #     #         if hamming(pattern, key) < 2:
    #     #             pattern = key
    #     #             break
    #     # end of hamming distance
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][pattern] != taken:
    #             hot_miss_3 += 1
    #             if miss_hit == 'H':
    #                 extra_miss_3 += 1
    #             pc_history[pc_history_index]['table'][pattern] = taken
    #         else:
    #             hot_hit_3 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_3 += -1
    #     else:
    #         if miss_hit == 'M':
    #             hot_miss_3 += 1
    #         else:
    #             hot_hit_3 += 1
    ####### End of First Implementation
    if br_pc == pc_history[pc_history_index]['pc']:
        # if len(pc_history[pc_history_index]['local_his_long']) < length_local:
        #     pc_history[pc_history_index]['local_his_long'] += taken
        # else:
        #     pc_history[pc_history_index]['local_his_long'] = pc_history[pc_history_index]['local_his_long'][1:] + taken
        if len(pc_history[pc_history_index]['local_his']) < length_local:
            pc_history[pc_history_index]['local_his'] += taken
        else:
            pc_history[pc_history_index]['local_his'] = pc_history[pc_history_index]['local_his'][1:] + taken

br_pc = {}

# tmp_pc = "0x7ffff7fda678"
tmp_pc = "0x7ffff7fce505"
tmp_str = ''

global_his = ""
global_his_len = 128

# First Time, record hot PC
# fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out"
fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_v0.out"
insn_period = 200000 # 1810000
end_insn = 1820000 # 1820000

# Store insn number idx * insn_period
def store_states(path, idx_insn, pc_his_idx):
    global insn_period
    file_name = path + "insn" + str(idx_insn * insn_period) + ".out" # insn number is the insn that trigger the load
    with open(file_name, "w") as f_out:
        for i in range(real_num_his[idx_insn]):
            f_out.write(hex(pc_history[pc_his_idx + i]['pc']))
            f_out.write("\n")
        # Store history
        for key in pc_history[pc_his_idx]['table']:
            f_out.write(str(key) + " " + str(pc_history[pc_his_idx]['table'][key]))
            f_out.write("\n")


for iteration in range(3):
    if iteration == 2:
        # fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out"
        fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_2_v0.out"
        # initialize the local histories
        for i in range(len(pc_history)):
            pc_history[i]['local_his'] = ''
    with open(fn, "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v1.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v10.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out", "r") as f_misses:
        global_his = ""
        line_cnt = 0
        init_miss = 0
        init_miss_t = 0
        init_miss_l = 0
        init_miss_s = 0
        total_miss = 0
        use_loop = 0
        use_loop_miss = 0
        use_sc = 0
        use_sc_miss = 0
        real_num_his_idx = 0
        pc_history_index = 0
        hot_miss_2_prev = 0
        hot_hit_2_prev = 0
        for line in f_misses:
            tokens = line.split()
            if len(tokens) < 4:
                continue
            pc = 0
            if tokens[0] == "ip":
                pc = int(tokens[1], 16)
            else:
                continue
            line_cnt += 1
            # if line_cnt % 10000000 == 0:
            # if line_cnt % 1822781 == 0:
            # if line_cnt % 2738 == 0:
            # if line_cnt % 20000 == 0:
            if iteration == 0:
                if line_cnt % insn_period == 0:
                    # if line_cnt % 40000 == 0:
                    #     break
                    # print(line_cnt)
                    preprocess_branch_misses(br_pc, line_cnt)
                    br_pc = {}
            elif iteration > 0:
                if real_num_his_idx < len(real_num_his):
                    for tmp_idx in range(real_num_his[real_num_his_idx]):
                        # print(len(pc_history), pc_history_index + tmp_idx)
                        if pc == pc_history[pc_history_index + tmp_idx]['pc']:
                            if iteration == 1:
                                process_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3], pc_history_index)
                            elif iteration == 2:
                                reload_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3], pc_history_index)
                            break
                if line_cnt > 0 and line_cnt % insn_period == 0 and pc_history_index < len(pc_history)-1:# - real_num_his[-1]:
                    if iteration == 1:
                        for tmp_idx in range(real_num_his[real_num_his_idx]):
                            print(hex(pc_history[pc_history_index + tmp_idx]['pc']), "Total hot miss:", hot_miss_2 - hot_miss_2_prev, "Total hot hit:", hot_hit_2 - hot_hit_2_prev)
                        hot_miss_2_prev = hot_miss_2
                        hot_hit_2_prev = hot_hit_2
                        pc_history_index += real_num_his[real_num_his_idx]
                        real_num_his_idx += 1
                    if iteration == 2:
                        for tmp_idx in range(real_num_his[real_num_his_idx]):
                            print(hex(pc_history[pc_history_index + tmp_idx]['pc']), "Table Length:", len(pc_history[pc_history_index + tmp_idx]['table']), "Total hot miss:", hot_miss_3 - hot_miss_2_prev, "Total hot hit:", hot_hit_3 - hot_hit_2_prev)
                        hot_miss_2_prev = hot_miss_3
                        hot_hit_2_prev = hot_hit_3
                        pc_history_index += real_num_his[real_num_his_idx]
                        real_num_his_idx += 1

            if line_cnt % end_insn == 0:
            # if line_cnt % 1822781 == 0:
                break
            # Init entry or update number
            if pc in br_pc:
                br_pc[pc]["num"] += 1
            else:
                br_pc[pc] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0, 
                             "h_t": 0, "m_t": 0, "h_l": 0, "m_l": 0, "h_s": 0, "m_s": 0}
                if tokens[3] == 'M':
                    init_miss += 1
                    if tokens[2] == 'L':
                        init_miss_l += 1
                    elif tokens[2] == 'S':
                        init_miss_s += 1
                    else:
                        init_miss_t += 1
            # update total miss/hit in branch history entries
            if tokens[3] == 'M':
                total_miss += 1
                br_pc[pc]["miss"] += 1
            else:
                br_pc[pc]["hit"] += 1
            # update num
            if tokens[2] == 'L':
                use_loop += 1
                if tokens[3] == 'M':
                    use_loop_miss += 1 
                    br_pc[pc]["m_l"] += 1
                else:
                    br_pc[pc]["h_l"] += 1
            elif tokens[2] == 'S':
                use_sc += 1
                if tokens[3] == 'M':
                    use_sc_miss += 1 
                    br_pc[pc]["m_s"] += 1
                else:
                    br_pc[pc]["h_s"] += 1
            else:
                if tokens[3] == 'M':
                    br_pc[pc]["m_t"] += 1
                else:
                    br_pc[pc]["h_t"] += 1
            # update miss/hit by Tage or Bimodal
            if tokens[4] == '0':
                br_pc[pc]["NT"] += 1
            else:
                br_pc[pc]["T"] += 1
            if pc == int(tmp_pc, 16):
                tmp_str += tokens[4]
            # update global history
            if len(global_his) < 128:
                global_his += tokens[4]
            else:
                global_his = global_his[1:] + tokens[4]
    # Add table store here after the preprocessing
    # if iteration == 1:
    #     pc_his_idx = 0
    #     for idx_insn in range(len(real_num_his)):
    #         store_states("./states/", idx_insn, pc_his_idx)
    #         pc_his_idx += real_num_his[idx_insn]



# ordered = OrderedDict(sorted(br_pc.items(), key=lambda i: i[1]["num"]))

print("Total Branch:", 1820000, "Total Miss", total_miss, "Hot Miss", hot_miss)
print("Use Loop:", use_loop, " Misses:", use_loop_miss)
print("Use SC:", use_sc, " Misses:", use_sc_miss)
print("Init Miss", init_miss, "Tage: ", init_miss_t, "Loop: ", init_miss_l, "SC: ", init_miss_s)

# only_1_cnt = 0
# total_cnt = 0
# for k,v in ordered:
#     total_cnt += 1
#     if v['num'] == 1:
#         only_1_cnt += 1
#     if total_cnt < 20:
#         print(hex(k), v)
# print("Total branch PCs: ", total_cnt, "Branch PC only occurs once: ", only_1_cnt)

# print(tmp_pc, tmp_str)
# 
# table = {}
# local_miss = 0
# len_localtable = 10
# for i in range(len(tmp_str)):
#     if i < len_localtable + 1:
#         continue
#     table[tmp_str[i-1-len_localtable:i-1]] = tmp_str[i]
# 
# for i in range(len(tmp_str)):
#     if i < len_localtable + 1:
#         continue
#     if tmp_str[i] != table[tmp_str[i-1-len_localtable:i-1]]:
#         local_miss += 1 
# print(local_miss)

print("Hot Misses: ", hot_miss, "Hit: ", hot_hit)
print("Second Time Hot Misses: ", hot_miss_2, "Hit: ", hot_hit_2, "Extra Miss:", extra_miss_2)
print("Third Time Hot Misses: ", hot_miss_3, "Hit: ", hot_hit_3, "Extra Miss:", extra_miss_3)
