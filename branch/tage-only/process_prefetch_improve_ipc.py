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



# tmp_pc = "0x7ffff7fda678"
tmp_pc = "0x7ffff7fce505"
tmp_str = ''


# First Time, record hot PC
# fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0_gh.out"
# fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-13_-_23-41-55-chameleon.trace_detailed_misses.out"
# fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-14_-_00-01-18-videoprocessing.trace_detailed_misses.out"



fnames = []
# bench_labels = ["imageprocessing"]
bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",
                "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
# bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",
#                 "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"

# stop_threshold = [300000, 40000, 60000, 40000, 40000, 30000, 40000, 300000, 30000, 30000]
stop_threshold = [30000000, 40000000, 60000000, 40000000, 40000000, 30000000, 40000000, 30000000, 30000000, 30000000]

for i in range(len(bench_labels)):
    for fn in os.listdir(f_dir):
        # if "detailed_misses_reasons_inv3.out" in fn and bench_labels[i] in fn:
        # if "detailed_misses_reasons_3.out" in fn and bench_labels[i] in fn:
        # if "detailed_misses_reasons_base" in fn and bench_labels[i] in fn:
        if "detailed_misses_reasons_tageonly_base" in fn and bench_labels[i] in fn:
        # if "detailed_misses_reasons_tagesmall_base" in fn and bench_labels[i] in fn:
            fnames.append(f_dir + fn)
            fn_tokens = fn.split(".")
            # bench_tokens = fn_tokens[0].split("-")
            # bench_labels.append(bench_tokens[-1])

insn_threshold = 1000000000

ipc_origin = []
br_mpki_list = []
fn_idx = 0
stop_insn = []
stop_miss = []
for fn in fnames:
    record_stop_data = False
    with open(fn, "r") as f_misses:
        insn_cnt = 0
        for line in f_misses:
            tokens = line.split()
            if "CPU 0 Branch Prediction Accuracy:" in line:
                br_mpki = float(tokens[7])
                miss_num = (insn_cnt * br_mpki / 1000.0)
                if not record_stop_data and miss_num > stop_threshold[fn_idx]:
                    stop_insn.append(insn_cnt)
                    stop_miss.append(miss_num)
                    print
                    record_stop_data = True
                if insn_cnt > insn_threshold:
                    break
            if "Heartbeat CPU 0" in line:
                insn_cnt = int(tokens[4])
                ipc = int(tokens[4]) * 1.0 / int(tokens[6])
                # ipc = float(tokens[12])
        if not record_stop_data:
            stop_insn.append(insn_cnt)
            miss_num = (insn_cnt * br_mpki / 1000.0)
            stop_miss.append(miss_num)
        ipc_origin.append(ipc)
        br_mpki_list.append(br_mpki)
        print(fn)
    fn_idx += 1
print(stop_miss)
print("IPC origin", ipc_origin)
print("Branch MPKI", br_mpki_list)

fnames = []
br_mpki_list_2 = []
for i in range(len(bench_labels)):
    for fn in os.listdir(f_dir):
        # if "_load_states.out" in fn and bench_labels[i] in fn:
        # if "_load_states_every1000atonce.out" in fn and bench_labels[i] in fn:
        # if "load_states_lessmemory_" in fn and bench_labels[i] in fn:
        if "load_states_tageonly_lessmemory" in fn and bench_labels[i] in fn:
        # if "load_states_tagesmall_lessmemory" in fn and bench_labels[i] in fn:
            fnames.append(f_dir + fn)
ipc_idealbranch = []
miss_reduce = []
fn_idx = 0
for fn in fnames:
    prefetch_stop = False
    with open(fn, "r") as f_misses:
        insn_cnt = 0
        for line in f_misses:
            tokens = line.split()
            if "CPU 0 Branch Prediction Accuracy:" in line:
                br_mpki = float(tokens[7])
                if not prefetch_stop and (insn_cnt > stop_insn[fn_idx] - 100 and insn_cnt < stop_insn[fn_idx] + 100):
                    miss_num = (insn_cnt * br_mpki / 1000.0)
                    miss_reduce.append(miss_num - stop_miss[fn_idx])
                    prfetch_stop = True
                if insn_cnt > insn_threshold:
                    break
            if "Heartbeat CPU 0" in line:
                insn_cnt = int(tokens[4])
                # ipc = float(tokens[12])
                ipc = int(tokens[4]) * 1.0 / int(tokens[6])
        br_mpki = br_mpki_list[fn_idx] + miss_reduce[-1] * 1000/ insn_cnt
        ipc_idealbranch.append(ipc)
        br_mpki_list_2.append(br_mpki)
        print(fn)
    fn_idx += 1
print("Miss reduction", miss_reduce)
print("Ideal branch", ipc_idealbranch)
print("Branch MPKI", br_mpki_list_2)
y1 = np.array(ipc_origin)
y2 = np.array(ipc_idealbranch)
print("Average IPC improvement", np.average(y2/y1))
bp1 = np.array(br_mpki_list)
bp2 = np.array(br_mpki_list_2)
print("Average MPKI % reduction", (1 - np.average(bp2/bp1)))

# print("Total Branch:", line_cnt, "Total Miss", total_miss, "Hot Miss", hot_miss)
# print("Use Loop:", use_loop, " Misses:", use_loop_miss)
# print("Use SC:", use_sc, " Misses:", use_sc_miss)
# print("Init Miss", init_miss, "Tage: ", init_miss_t, "Loop: ", init_miss_l, "SC: ", init_miss_s)
# 
# print("Hot Misses: ", hot_miss, "Hit: ", hot_hit)
# print("Second Time Hot Misses: ", hot_miss_2, "Hit: ", hot_hit_2, "Extra Miss:", extra_miss_2)
# print("Third Time Hot Misses: ", hot_miss_3, "Hit: ", hot_hit_3, "Extra Miss:", extra_miss_3)
# 
# print("Total Branch:", line_cnt, "Branch PC Number:", len(br_pc_local))
# print("Unique PC and History", unique_pc_his, "Tuple Matched", same_pc_his, "Diff than prev(Reload won't help):", diff_than_prev, "Same PC and History but misses", same_pc_his_miss)
# print("Branch misses:", total_miss, "Unique Local History", len(br_local_miss))

font = {'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
axs.bar(x_bar_pos, 100*(y2/y1 - 1), width=0.3, color='limegreen', label='IPC Improvement with Prefetch')
# axs.bar(x_bar_pos, y1, width=0.3, color='cornflowerblue', label='512Kbits TAGE-SC-L')
# axs.plot(x_insn_count, unique_pc_his_list, linewidth=2, color = 'purple', label = str(his_len))
axs.set_ylabel('% of IPC Improvement')
# axs.set_xlabel('Instruction Count')
axs.set_xticks(x_bar_pos, bench_labels, fontsize=14, rotation=45, ha='right')
# ax2 = axs.twinx()
# ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
# ax2.set_ylabel('MPKI')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.86, bottom=0.325, left=0.085, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
fig.legend(handles, labels, loc='upper right', ncol=2)
fig.savefig("Prefetch_improve_IPC.eps", format='eps')
plt.show()

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
axs.bar(x_bar_pos, 100*abs((1 - bp2/bp1)), width=0.3, color='coral', label='MPKI Reduction with Prefetch')
axs.set_ylabel('% of MPKI Reduction')
axs.set_xticks(x_bar_pos, bench_labels, fontsize=14, rotation=45, ha='right')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.86, bottom=0.325, left=0.085, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
fig.legend(handles, labels, loc='upper right', ncol=2)
fig.savefig("Prefetch_MPKI_reduction.eps", format='eps')
plt.show()

