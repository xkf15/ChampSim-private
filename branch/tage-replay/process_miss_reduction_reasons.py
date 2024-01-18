from collections import OrderedDict
import random
import numpy as np
import matplotlib.pyplot as plt
import os

font = {'weight' : 'bold',
        'size'   : 14}

compulsory_miss_list = [[],[]]
capacity_miss_list = [[],[]]
conflict_miss_list = [[],[]]
conflict_miss_low_64_list = [[],[]]
conflict_miss_low_128_list = [[],[]]
conflict_miss_low_1024_list = [[],[]]

# First Time, record hot PC
# fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0.out"
# fn = "/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_v0_gh.out"
# fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-13_-_23-41-55-chameleon.trace_detailed_misses.out"
fnames = []
# bench_labels = []
bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing", 
                "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"

# for i in range(10):
#     for fn in os.listdir(f_dir):
#         # if "detailed_misses_reasons_2" in fn and bench_labels[i] in fn:
#         if "detailed_misses_reasons_base" in fn and bench_labels[i] in fn:
#             fnames.append(f_dir + fn)
#     for fn in os.listdir(f_dir):
#         if "load_states_lessmemory_" in fn and bench_labels[i] in fn:
#             fnames.append(f_dir + fn)
# 
# bench_type = 0 # 0 base, 1 improve
# for fn in fnames:
#     his_len = 256
#     br_pc = {}
#     br_pc_local = {}
#     br_local_miss = {}
#     with open(fn, "r") as f_misses:
#         line_cnt = 0
#         init_miss = 0
#         init_miss_t = 0
#         init_miss_l = 0
#         init_miss_s = 0
#         total_miss = 0
#         use_loop = 0
#         use_loop_miss = 0
#         use_sc = 0
#         use_sc_miss = 0
#         real_num_his_idx = 0
#         pc_history_index = 0
#         hot_miss_2_prev = 0
#         hot_hit_2_prev = 0
#         unique_pc_his = 0 # unique pc and history
#         unique_pc_his_last = 0 # tmp unique pc and history
#         unique_pc_his_list = [0]
#         x_insn_count = [0]
#         y_bp_mpki = [0]
#         total_miss_last = 0
#         same_pc_his = 0 # same pc and history again
#         same_pc_his_miss = 0 # same pc and history but wrong outcome
#         diff_than_prev = 0 # same pc and history but different outcome than last time
#         ghist = ""
#         # miss reasons
#         conflict_miss = 0
#         conflict_miss_low_64 = 0
#         conflict_miss_low_128 = 0
#         conflict_miss_low_1024 = 0
#         capacity_miss = 0
#         compulsory_miss = 0
#         for line in f_misses:
#             tokens = line.split()
#             if "Heartbeat CPU 0" in line:
#                 insn_cnt = int(tokens[4])
#                 x_insn_count.append(insn_cnt)
#                 # y_bp_mpki.append((total_miss - total_miss_last) * 1000.0 / 10000000)
#                 total_miss_last = total_miss
#                 unique_pc_his_list.append(unique_pc_his - unique_pc_his_last)
#                 if insn_cnt % 10000000 < 100:
#                     print(insn_cnt)
#                 if insn_cnt > 10000000:
#                     break
#                 unique_pc_his_last = unique_pc_his
#             if len(tokens) < 5:
#                 continue
#             pc = 0
#             lhist = ""
#             if tokens[0] == "ip":
#                 pc = int(tokens[1], 16)
#                 # begin_idx = int(32-his_len/4)
#                 # ghist = tokens[5][begin_idx:]
#             else:
#                 continue
#             line_cnt += 1
#             # Init entry or update number
#             # if pc in br_pc_local:
#             #     lhist = br_pc_local[pc]
#             phist = ghist
#             if (pc, phist) in br_pc:
#                 matched_pc_his = True
#                 br_pc[(pc, phist)]["num"] += 1
#                 same_pc_his += 1
#                 if tokens[3] == 'M':
#                     same_pc_his_miss += 1
#                 if tokens[4] != br_pc[(pc, phist)]["last_outcome"]:
#                     diff_than_prev += 1
#                     # print(pc, phist, "Prev:", br_pc[(pc, phist)]["last_outcome"], "Current:", tokens[4])
#             else:
#                 matched_pc_his = False
#                 unique_pc_his += 1
#                 br_pc[(pc, phist)] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0, 
#                         "h_t": 0, "m_t": 0, "h_l": 0, "m_l": 0, "h_s": 0, "m_s": 0, "last_outcome": tokens[4]}
#                 if tokens[3] == 'M':
#                     init_miss += 1
#                     if tokens[2] == 'L':
#                         init_miss_l += 1
#                     elif tokens[2] == 'S':
#                         init_miss_s += 1
#                     else:
#                         init_miss_t += 1
#             # if miss add local history into miss table
#             if tokens[3] == 'M':
#                 if phist in br_local_miss:
#                     br_local_miss[phist] += 1
#                 else:
#                     br_local_miss[phist] = 0
#                 # decide miss reasons:
#                 if int(tokens[5]) != 0:
#                     conflict_miss += 1
#                     if int(tokens[5]) < 15:
#                         conflict_miss_low_64 += 1
#                     if int(tokens[5]) < 19:
#                         conflict_miss_low_128 += 1
#                     if int(tokens[5]) < 31:
#                         conflict_miss_low_1024 += 1
#                 else:
#                     if matched_pc_his:
#                         capacity_miss += 1
#                     else:
#                         compulsory_miss += 1
#             # insert local history
#             # if pc in br_pc_local:
#             #     if len(br_pc_local[pc]) < his_len:
#             #         br_pc_local[pc] = br_pc_local[pc] + tokens[4]
#             #     else:
#             #         br_pc_local[pc] = br_pc_local[pc][1:] + tokens[4]
#             # else:
#             #     br_pc_local[pc] = tokens[4]
#             # update total miss/hit in branch history entries
#             if tokens[3] == 'M':
#                 total_miss += 1
#             if len(ghist) < his_len:
#                 ghist += tokens[4]
#             else:
#                 ghist = ghist[1:] + tokens[4]
#     
#     print("Total Branch:", line_cnt, "Branch PC Number:", len(br_pc_local))
#     print("Unique PC and History", unique_pc_his, "Tuple Matched", same_pc_his, "Diff than prev(Reload won't help):", diff_than_prev, "Same PC and History but misses", same_pc_his_miss)
#     print("Branch misses:", total_miss, "Unique Local History", len(br_local_miss))
# 
#     print("Compulsory:", compulsory_miss, "Conflict: ", conflict_miss, "Capacity: ", capacity_miss)
#     print("Conflict low 64:", conflict_miss_low_64 * 1.0 / conflict_miss)
#     print("Conflict low 128:", conflict_miss_low_128 * 1.0 / conflict_miss)
#     print("Conflict low 1024:", conflict_miss_low_1024 * 1.0 / conflict_miss)
#     # compulsory_miss_list[bench_type].append(compulsory_miss * 100.0 / total_miss)
#     # conflict_miss_list[bench_type].append(conflict_miss * 100.0 / total_miss)
#     # capacity_miss_list[bench_type].append(capacity_miss * 100.0 / total_miss)
#     compulsory_miss_list[bench_type].append(compulsory_miss)
#     conflict_miss_list[bench_type].append(conflict_miss)
#     capacity_miss_list[bench_type].append(capacity_miss)
#     conflict_miss_low_64_list[bench_type].append(conflict_miss_low_64)
#     conflict_miss_low_128_list[bench_type].append(conflict_miss_low_128)
#     conflict_miss_low_1024_list[bench_type].append(conflict_miss_low_1024)
# 
#     bench_type = bench_type ^ 1
# 
# def store_list(fp, li):
#     fp.write(str(li[0]))
#     for token in li[1:]:
#         fp.write(",")
#         fp.write(str(token))
#     fp.write("\n")
#     return
# 
# with open("miss_reasons_reduction_prefetch.csv", "w") as f_output:
#     store_list(f_output, compulsory_miss_list[0])
#     store_list(f_output, compulsory_miss_list[1])
#     store_list(f_output, conflict_miss_list[0])
#     store_list(f_output, conflict_miss_list[1])
#     store_list(f_output, conflict_miss_low_128_list[0])
#     store_list(f_output, conflict_miss_low_128_list[1])
#     store_list(f_output, capacity_miss_list[0])
#     store_list(f_output, capacity_miss_list[1])

compulsory_miss_list = [[],[]]
capacity_miss_list = [[],[]]
conflict_miss_list = [[],[]]
conflict_miss_low_64_list = [[],[]]
conflict_miss_low_128_list = [[],[]]
conflict_miss_low_1024_list = [[],[]]
with open("miss_reasons_reduction_prefetch.csv", "r") as f_in:
    line_cnt = 0
    for line in f_in:
        tokens = line.split(",")
        if line_cnt == 0:
            for token in tokens:
                compulsory_miss_list[0].append(int(token))
        elif line_cnt == 1:
            for token in tokens:
                compulsory_miss_list[1].append(int(token))
        elif line_cnt == 2:
            for token in tokens:
                conflict_miss_list[0].append(int(token))
        elif line_cnt == 3:
            for token in tokens:
                conflict_miss_list[1].append(int(token))
        elif line_cnt == 4:
            for token in tokens:
                conflict_miss_low_128_list[0].append(int(token))
        elif line_cnt == 5:
            for token in tokens:
                conflict_miss_low_128_list[1].append(int(token))
        elif line_cnt == 6:
            for token in tokens:
                capacity_miss_list[0].append(int(token))
        elif line_cnt == 7:
            for token in tokens:
                capacity_miss_list[1].append(int(token))
        line_cnt += 1


plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 6))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
y1 = np.array(compulsory_miss_list[0])
y2 = np.array(conflict_miss_list[0])
y3 = np.array(capacity_miss_list[0])
y_low_1 = np.array(conflict_miss_low_128_list[0])
y11 = np.array(compulsory_miss_list[1])
y22 = np.array(conflict_miss_list[1])
y33 = np.array(capacity_miss_list[1])
y_low_2 = np.array(conflict_miss_low_128_list[1])
print("miss reduction: Compulsory", (1-np.average(y11/y1)), "conflict", (1-np.average(y22/y2)), "Lower", (1-np.average(y_low_2/y_low_1)), "Capacity", (1-np.average(y33/y3)))
# axs.bar(x_bar_pos, 1-y11/y1, width=0.1, color='deepskyblue', label='Compulsory')
# axs.bar(x_bar_pos + 0.1, 1-y22/y2, width=0.1, color='coral', label='Hit in TAGE but wrong')
# # axs.bar(x_bar_pos + 0.2, 1-y_low_2/y_low_1, alpha=1, width=0.1, color='coral', edgecolor='black', hatch='//', label='Hit in TAGE at Lower Banks')
# axs.bar(x_bar_pos + 0.2, 1-y33/y3, width=0.1, color='seagreen', label='Capacity')
axs.bar(x_bar_pos, y1-y11, width=0.1, color='deepskyblue', label='Compulsory')
axs.bar(x_bar_pos + 0.1, y2-y22, width=0.1, color='coral', label='TAGE Hit Misprediction')
# axs.bar(x_bar_pos + 0.2, y_low_1-y_low_2, alpha=1, width=0.1, color='coral', edgecolor='black', hatch='//', label='Hit in TAGE at Lower Banks')
axs.bar(x_bar_pos + 0.2, y3-y33, width=0.1, color='seagreen', label='Capacity')
axs.set_ylabel('Misprediction Reduction Number')
# axs.set_xlabel('Benchmarks')
axs.set_xticks(x_bar_pos + 0.1, bench_labels, rotation=45, ha='right')
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.910, bottom=0.270, left=0.120, right=0.985, hspace=0.2, wspace=0.2)
fig.legend(handles, labels, loc='upper right', ncol=3)
# ax2 = axs.twinx()
# ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
# ax2.set_ylabel('MPKI')
fig.savefig("Miss_reasons_reduction_pefetch.eps", format='eps')
plt.show()

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 6))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
y_conflict = y2-y22
y_low = y_low_1 - y_low_2
axs.bar(x_bar_pos, y2-y22, width=0.15, color='coral', label='TAGE Hit Misprediction')
axs.bar(x_bar_pos + 0.15, y_low_1-y_low_2, alpha=1, width=0.15, color='brown', edgecolor='black', hatch='//', label='Lower Banks')
bottom_high = []
y_high = y_conflict - y_low
for i in range(10):
    if y_high[i] > 0 :
        if y_low[i] > 0:
            bottom_high.append(y_low[i])
        else:
            bottom_high.append(0)
    else:
        if y_low[i] < 0:
            bottom_high.append(y_low[i])
        else:
            bottom_high.append(0)
axs.bar(x_bar_pos + 0.15, (y2 - y22) - (y_low_1-y_low_2), bottom=bottom_high, alpha=1, width=0.15, color='lemonchiffon', edgecolor='black', hatch='\\\\', label='Higher Banks')
axs.set_ylabel('Misprediction Reduction Number')
axs.set_xticks(x_bar_pos + 0.075, bench_labels, rotation=45, ha='right')
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.910, bottom=0.270, left=0.120, right=0.985, hspace=0.2, wspace=0.2)
fig.legend(handles, labels, loc='upper right', ncol=3)
fig.savefig("Miss_reasons_reduction_conflict.eps", format='eps')
plt.show()

