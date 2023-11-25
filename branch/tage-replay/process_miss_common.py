from collections import OrderedDict
import random
import numpy as np
import matplotlib.pyplot as plt
import os

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



# bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",
#                 "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
bench_labels = ["chameleon"]# , "floatoperation", "linpack", "rnnserving", "videoprocessing",
for his_len in [128 , 256, 512, 1024]:
    common_miss_all_list = []
    compulsory_miss_list = []
    capacity_miss_list = []
    conflict_miss_list = []
    conflict_miss_low_64_list = []
    conflict_miss_low_128_list = []
    conflict_miss_low_1024_list = []
    for bench_l in bench_labels:
        fnames = []
        # bench_labels = []
        f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"
        
        for fn in os.listdir(f_dir):
            # if "detailed_misses_reasons_2" in fn and bench_l in fn:
            if "detailed_misses_reasons_inv3.out" in fn and bench_l in fn:
                fnames.append(f_dir + fn)
        
        for fn in os.listdir(f_dir):
            if "load_states_every1000atonce.out" in fn and bench_l in fn:
                fnames.append(f_dir + fn)
                break
        print(fnames)
        
        br_pc = {}
        bench_round = 0 
        end_insn = 9900000
        for fn in fnames:
            bench_round += 1
            br_pc_local = {}
            br_local_miss = {}
            with open(fn, "r") as f_misses:
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
                y_bp_conflict_mpki = [0]
                y_bp_compulsory_mpki = [0]
                y_bp_capacity_mpki = [0]
                total_miss_last = 0
                conflict_miss_last = 0
                compulsory_miss_last = 0
                capacity_miss_last = 0
                same_pc_his = 0 # same pc and history again
                same_pc_his_miss = 0 # same pc and history but wrong outcome
                diff_than_prev = 0 # same pc and history but different outcome than last time
                ghist = ""
                # miss reasons
                conflict_miss = 0
                conflict_miss_low_64 = 0
                conflict_miss_low_128 = 0
                conflict_miss_low_1024 = 0
                capacity_miss = 0
                compulsory_miss = 0
                # Common 
                common_miss = 0
                common_miss_last = 0
                common_miss_list = [0]
                for line in f_misses:
                    tokens = line.split()
                    # the first round, record (PC, History) pair
                    if bench_round == 1:
                        if "Heartbeat CPU 0" in line:
                            insn_cnt = int(tokens[4])
                            x_insn_count.append(insn_cnt)
                            print(insn_cnt)
                            if insn_cnt > end_insn:
                                break
                        if len(tokens) < 5:
                            continue
                        pc = 0
                        lhist = ""
                        if tokens[0] == "ip":
                            pc = int(tokens[1], 16)
                        else:
                            continue
                        line_cnt += 1
                        # Init entry or update number
                        phist = ghist
                        if tokens[3] == 'M':
                            if (pc, phist) in br_pc:
                                matched_pc_his = True
                                br_pc[(pc, phist)]["num"] += 1
                                same_pc_his += 1
                                if tokens[3] == 'M':
                                    same_pc_his_miss += 1
                                if tokens[4] != br_pc[(pc, phist)]["last_outcome"]:
                                    diff_than_prev += 1
                            else:
                                matched_pc_his = False
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
                            # decide miss reasons:
                            if int(tokens[5]) != 0:
                                conflict_miss += 1
                                if int(tokens[5]) < 15:
                                    conflict_miss_low_64 += 1
                                if int(tokens[5]) < 19:
                                    conflict_miss_low_128 += 1
                                if int(tokens[5]) < 31:
                                    conflict_miss_low_1024 += 1
                            else:
                                if matched_pc_his:
                                    capacity_miss += 1
                                else:
                                    compulsory_miss += 1
                        # insert local history
                        # update total miss/hit in branch history entries
                        if tokens[3] == 'M':
                            total_miss += 1
                        if len(ghist) < his_len:
                            ghist += tokens[4]
                        else:
                            ghist = ghist[1:] + tokens[4]
                    else:
                        if "Heartbeat CPU 0" in line:
                            insn_cnt = int(tokens[4])
                            x_insn_count.append(insn_cnt)
                            print(insn_cnt)
                            common_miss_list.append((common_miss - common_miss_last) / (total_miss - total_miss_last))
                            common_miss_last = common_miss
                            total_miss_last = total_miss
                            if insn_cnt > end_insn:
                                break
                        if len(tokens) < 5:
                            continue
                        pc = 0
                        if tokens[0] == "ip":
                            pc = int(tokens[1], 16)
                        else:
                            continue
                        phist = ghist
                        if tokens[3] == 'M' and (pc, phist) in br_pc:
                            common_miss += 1
                        if tokens[3] == 'M':
                            total_miss += 1
                        if len(ghist) < his_len:
                            ghist += tokens[4]
                        else:
                            ghist = ghist[1:] + tokens[4]
        
            
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
            
            print("Total Branch:", line_cnt, "Branch PC Number:", len(br_pc_local))
            print("Unique PC and History", unique_pc_his, "Tuple Matched", same_pc_his, "Diff than prev(Reload won't help):", diff_than_prev, "Same PC and History but misses", same_pc_his_miss)
            print("Branch misses:", total_miss, "Unique Local History", len(br_local_miss))
        
            # print("Compulsory:", compulsory_miss, "Conflict: ", conflict_miss, "Capacity: ", capacity_miss)
            # print("Conflict low 64:", conflict_miss_low_64 * 1.0 / conflict_miss)
            # print("Conflict low 128:", conflict_miss_low_128 * 1.0 / conflict_miss)
            # print("Conflict low 1024:", conflict_miss_low_1024 * 1.0 / conflict_miss)
            # compulsory_miss_list.append(compulsory_miss * 100.0 / total_miss)
            # conflict_miss_list.append(conflict_miss * 100.0 / total_miss)
            # capacity_miss_list.append(capacity_miss * 100.0 / total_miss)
            # conflict_miss_low_64_list.append(conflict_miss_low_64 * 100.0 / total_miss)
            # conflict_miss_low_128_list.append(conflict_miss_low_128 * 100.0 / total_miss)
            # conflict_miss_low_1024_list.append(conflict_miss_low_1024 * 100.0 / total_miss)
        
            print(bench_l, "Common misses:", common_miss, common_miss/total_miss)
            if bench_round > 1:
                common_miss_all_list.append(common_miss/total_miss)
            # if his_len == 1024:
            #     axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'navy', label = str(his_len))
            # elif his_len == 512:
            #     axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'green', label = str(his_len))
            # elif his_len == 256:
            #     axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'purple', label = str(his_len))
    
    # Store the results
    # def store_list(fp, li):
    #     fp.write(str(li[0]))
    #     for token in li[1:]:
    #         fp.write(",")
    #         fp.write(str(token))
    #     fp.write("\n")
    #     return
    # 
    # with open("miss_common" + str(his_len) +".csv", "w") as f_output:
    #     print(common_miss_all_list)
    #     store_list(f_output, common_miss_all_list)

exit(0)

font = {'weight' : 'bold',
        'size'   : 14}
plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
# axs.plot(x_insn_count, common_miss_list, linewidth=2, color = 'black', label = 'Common miss percentage')
# axs.plot(x_insn_count, y1, linewidth=2, color = 'cornflowerblue', label = 'Compulsory Misses')
# axs.plot(x_insn_count, y1 + y2, linewidth=2, color = 'coral', label = 'Conflict Misses')
# axs.fill_between(x_insn_count, y0, y1, color = 'cornflowerblue', label = 'Compulsory Misses')
# axs.fill_between(x_insn_count, y1, y1 + y2, color = 'coral', label = 'Conflict Misses')
# axs.fill_between(x_insn_count, y1 + y2, y_bp_mpki, color = 'c', label = 'Capacity Misses')

axs.bar(x_bar_pos, common_miss_all_list, width=0.3, color='deepskyblue', label='Common miss')

# axs.bar(x_bar_pos, compulsory_miss_list, width=0.3, color='deepskyblue', label='Compulsory')
# axs.bar(x_bar_pos, conflict_miss_list, bottom=y1, width=0.3, color='coral', label='Conflict')
# axs.bar(x_bar_pos, y_low, bottom=y1, alpha=1, width=0.285, color='coral', edgecolor='black', hatch='//', label='Conflict at Lower Banks')
# axs.bar(x_bar_pos, capacity_miss_list, bottom=y1+y2, width=0.3, color='c', label='Capacity')
axs.set_ylabel('% of Common Miss')
axs.set_xlabel('Instructions')
# axs.set_xticks(x_bar_pos, bench_labels, rotation=45, ha='right')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.9, bottom=0.130, left=0.095, right=0.985, hspace=0.2, wspace=0.2)
fig.legend(handles, labels, loc='upper right', ncol=4)
# ax2 = axs.twinx()
# ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
# ax2.set_ylabel('MPKI')
fig.savefig("Miss_common.eps", format='eps')
plt.show()
