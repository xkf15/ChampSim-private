from collections import OrderedDict
import random
import numpy as np
import matplotlib.pyplot as plt

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
max_pc_num = 10 # how many hot pcs to record for each period
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
    ####### Sixth Implementation:
    # Combine all pc_history into one table
    if br_pc == pc_history[pc_history_index]['pc']:
        pattern = pc_history[pc_history_index]['local_his']
        if pattern in pc_history[table_index]['table']:
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
                if (len(pc_history[table_index]['table']) < 1000 and len(pattern) == length_local):
                    pc_history[table_index]['table'][pattern] = taken
            else:
                hot_hit_2 += 1
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
    ####### Sixth Implementation:
    # Combine all pc_history into one table
    if br_pc == pc_history[pc_history_index]['pc']:
        pattern = pc_history[pc_history_index]['local_his']
        if pattern in pc_history[table_index]['table']:
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
                # if (len(pc_history[table_index]['table']) < 1000 and len(pattern) == length_local):
                #     pc_history[table_index]['table'][pattern] = taken
            else:
                hot_hit_3 += 1
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



# tmp_pc = "0x7ffff7fda678"
tmp_pc = "0x7ffff7fce505"
tmp_str = ''

font = {'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(12, 10))

# First Time, record hot PC
# fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0_gh.out"
# fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-13_-_23-41-55-chameleon.trace_detailed_misses.out"
fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-14_-_00-01-18-videoprocessing.trace_detailed_misses.out"
# for iteration in range(1):
#     if iteration == 2:
#         # fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out"
#         fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_2_v0.out"
for his_len in [1024, 512, 256]:
    br_pc = {}
    br_pc_local = {}
    br_local_miss = {}
    with open(fn, "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v1.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v10.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out", "r") as f_misses:
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
        unique_pc_his = 0 # unique pc and history
        unique_pc_his_last = 0 # tmp unique pc and history
        unique_pc_his_list = [0]
        x_insn_count = [0]
        y_bp_mpki = [0]
        total_miss_last = 0
        same_pc_his = 0 # same pc and history again
        same_pc_his_miss = 0 # same pc and history but wrong outcome
        diff_than_prev = 0 # same pc and history but different outcome than last time
        ghist = ""
        for line in f_misses:
            tokens = line.split()
            if "Heartbeat CPU 0" in line:
                insn_cnt = int(tokens[4])
                print(insn_cnt)
                if insn_cnt > 99000000:
                    break
                x_insn_count.append(insn_cnt)
                y_bp_mpki.append((total_miss - total_miss_last) * 1000.0 / 10000000)
                total_miss_last = total_miss
                unique_pc_his_list.append(unique_pc_his - unique_pc_his_last)
                unique_pc_his_last = unique_pc_his
            if len(tokens) < 5:
                continue
            pc = 0
            lhist = ""
            if tokens[0] == "ip":
                pc = int(tokens[1], 16)
                # begin_idx = int(32-his_len/4)
                # ghist = tokens[5][begin_idx:]
            else:
                continue
            line_cnt += 1
            # if line_cnt % 10000000 == 0:
            # if line_cnt % 1822781 == 0:
            # if line_cnt % 2738 == 0:
            # if line_cnt % 20000 == 0:

            # if iteration == 0:
            #     if line_cnt % 100000 == 0:
            #         # if line_cnt % 40000 == 0:
            #         #     break
            #         # print(line_cnt)
            #         preprocess_branch_misses(br_pc, line_cnt)
            #         br_pc = {}
            # elif iteration > 0:
            #     for tmp_idx in range(real_num_his[real_num_his_idx]):
            #         # print(len(pc_history), pc_history_index + tmp_idx)
            #         if pc == pc_history[pc_history_index + tmp_idx]['pc']:
            #             if iteration == 1:
            #                 process_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3], pc_history_index)
            #             elif iteration == 2:
            #                 reload_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3], pc_history_index)
            #             break
            #     if line_cnt % 100000 == 0 and pc_history_index < len(pc_history) - real_num_his[-1]:
            #         if iteration == 1:
            #             for tmp_idx in range(real_num_his[real_num_his_idx]):
            #                 print(hex(pc_history[pc_history_index + tmp_idx]['pc']), hot_miss_2 - hot_miss_2_prev, hot_hit_2 - hot_hit_2_prev)
            #             hot_miss_2_prev = hot_miss_2
            #             hot_hit_2_prev = hot_hit_2
            #             pc_history_index += real_num_his[real_num_his_idx]
            #             real_num_his_idx += 1
            #         if iteration == 2:
            #             for tmp_idx in range(real_num_his[real_num_his_idx]):
            #                 print(hex(pc_history[pc_history_index + tmp_idx]['pc']), len(pc_history[pc_history_index + tmp_idx]['table']), hot_miss_3 - hot_miss_2_prev, hot_hit_3 - hot_hit_2_prev)
            #             hot_miss_2_prev = hot_miss_3
            #             hot_hit_2_prev = hot_hit_3
            #             pc_history_index += real_num_his[real_num_his_idx]
            #             real_num_his_idx += 1

            # if line_cnt % 10000000 == 0:
            # if line_cnt % 1820000 == 0:
            # if line_cnt % 1822781 == 0:
            #     break
            # Init entry or update number
            if pc in br_pc_local:
                lhist = br_pc_local[pc]
            phist = ghist
            if (pc, phist) in br_pc:
                br_pc[(pc, phist)]["num"] += 1
                same_pc_his += 1
                if tokens[3] == 'M':
                    same_pc_his_miss += 1
                if tokens[4] != br_pc[(pc, phist)]["last_outcome"]:
                    diff_than_prev += 1
                    # print(pc, phist, "Prev:", br_pc[(pc, phist)]["last_outcome"], "Current:", tokens[4])
            else:
                unique_pc_his += 1
                br_pc[(pc, phist)] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0, 
                        "h_t": 0, "m_t": 0, "h_l": 0, "m_l": 0, "h_s": 0, "m_s": 0, "last_outcome": tokens[4]}
                if tokens[3] == 'M':
                    init_miss += 1
                    if tokens[2] == 'L':
                        init_miss_l += 1
                    elif tokens[2] == 'S':
                        init_miss_s += 1
                    else:
                        init_miss_t += 1
            # if miss add local history into miss table
            if tokens[3] == 'M':
                if phist in br_local_miss:
                    br_local_miss[phist] += 1
                else:
                    br_local_miss[phist] = 0
            # insert local history
            if pc in br_pc_local:
                if len(br_pc_local[pc]) < his_len:
                    br_pc_local[pc] = br_pc_local[pc] + tokens[4]
                else:
                    br_pc_local[pc] = br_pc_local[pc][1:] + tokens[4]
            else:
                br_pc_local[pc] = tokens[4]
            # update total miss/hit in branch history entries
            if tokens[3] == 'M':
                total_miss += 1
            if len(ghist) < his_len:
                ghist += tokens[4]
            else:
                ghist = ghist[1:] + tokens[4]
            #     br_pc[pc]["miss"] += 1
            # else:
            #     br_pc[pc]["hit"] += 1
            # # update num
            # if tokens[2] == 'L':
            #     use_loop += 1
            #     if tokens[3] == 'M':
            #         use_loop_miss += 1 
            #         br_pc[pc]["m_l"] += 1
            #     else:
            #         br_pc[pc]["h_l"] += 1
            # elif tokens[2] == 'S':
            #     use_sc += 1
            #     if tokens[3] == 'M':
            #         use_sc_miss += 1 
            #         br_pc[pc]["m_s"] += 1
            #     else:
            #         br_pc[pc]["h_s"] += 1
            # else:
            #     if tokens[3] == 'M':
            #         br_pc[pc]["m_t"] += 1
            #     else:
            #         br_pc[pc]["h_t"] += 1
            # # update miss/hit by Tage or Bimodal
            # if tokens[4] == '0':
            #     br_pc[pc]["NT"] += 1
            # else:
            #     br_pc[pc]["T"] += 1
            # if pc == int(tmp_pc, 16):
            #     tmp_str += tokens[4]

    # ordered = OrderedDict(sorted(br_pc.items(), key=lambda i: i[1]["num"]))
    
    print("Total Branch:", line_cnt, "Total Miss", total_miss, "Hot Miss", hot_miss)
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
    
    print("Total Branch:", line_cnt, "Branch PC Number:", len(br_pc_local))
    print("Unique PC and History", unique_pc_his, "Tuple Matched", same_pc_his, "Diff than prev(Reload won't help):", diff_than_prev, "Same PC and History but misses", same_pc_his_miss)
    print("Branch misses:", total_miss, "Unique Local History", len(br_local_miss))

    if his_len == 1024:
        axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'navy', label = str(his_len))
    elif his_len == 512:
        axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'green', label = str(his_len))
    elif his_len == 256:
        axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'purple', label = str(his_len))
axs.set_ylabel('Unique (PC, History) Tuple')
axs.set_xlabel('Instruction Count')
ax2 = axs.twinx()
ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
ax2.set_ylabel('MPKI')
fig.savefig("Unique_PC_History.eps", format='eps')
plt.show()
