from collections import OrderedDict
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import statistics

# bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving","videoprocessing",
#                 "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
bench_labels = ["chameleon"]

common_miss_corr_list = []

def sort_misses(br_pc_his):
    ordered = sorted(br_pc_his.items(), key=lambda i: i[1]["miss"], reverse=True)
    total_cnt = 0
    for k,v in ordered:
        print(k, v)
        total_cnt += 1
        if total_cnt > 10:
            break

f_pc_trace1 = open("pc_trace1.txt", "w")
f_pc_trace2 = open("pc_trace2.txt", "w")

# for his_len in [128, 256, 512, 1024]:
for delta in range(1):
    common_miss_all_list = []
    for his_len in [128]: # , 256, 512, 1024]:
        br_pc_list = [{}] # store all pc,history pairs in each period 
        common_miss_bench_list = [0]
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
                if "store_states_tageonly_pid" in fn and bench_l in fn:
                    fnames.append(f_dir + fn)
            
            for fn in os.listdir(f_dir):
                if "detailed_misses_reasons_tageonly_base" in fn and bench_l in fn:
                    fnames.append(f_dir + fn)
            
            br_pc = br_pc_list[0]
            bench_round = 0 
            period_insn = 1000000000# 1000000 # 30000000
            end_insn = 1000000000# 990000000
            for fn in fnames:
                bench_round += 1
                with open(fn, "r") as f_misses:
                    line_cnt = 0
                    if bench_round > 1:
                        period_idx = delta # initialized to other value if want to do corelation study
                    else:
                        period_idx = 0 # the index of current period
                    tmp_print_cnt = 0 # number of printed PC count
                    max_pc_print_cnt = 10000000 # number of max printed PC count
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
                    common_miss_correct = 0 # originally wrong -> correct
                    common_miss_wrong = 0 # originally correct -> wrong
                    common_miss_last = 0
                    for line in f_misses:
                        tokens = line.split()
                        # the first round, record (PC, History) pair
                        if bench_round == 1:
                            if "Heartbeat CPU 0" in line:
                                insn_cnt = int(tokens[4])
                                x_insn_count.append(insn_cnt)
                                y_bp_mpki.append((total_miss - total_miss_last) * 1000.0 / 10000000)
                                y_bp_conflict_mpki.append((conflict_miss - conflict_miss_last) * 1000.0 / 10000000)
                                y_bp_compulsory_mpki.append((compulsory_miss - compulsory_miss_last) * 1000.0 / 10000000)
                                y_bp_capacity_mpki.append((capacity_miss - capacity_miss_last) * 1000.0 / 10000000)
                                total_miss_last = total_miss
                                conflict_miss_last = conflict_miss
                                compulsory_miss_last = compulsory_miss
                                capacity_miss_last = capacity_miss
                                unique_pc_his_list.append(unique_pc_his - unique_pc_his_last)
                                if insn_cnt % 10000000 < 10:
                                    print(insn_cnt)
                                if insn_cnt >= period_insn * (period_idx + 1):
                                    br_pc_list.append({})
                                    period_idx += 1
                                if insn_cnt >= end_insn:
                                    break
                                unique_pc_his_last = unique_pc_his
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
                            if (pc, phist) in br_pc_list[period_idx]:
                                matched_pc_his = True
                                br_pc_list[period_idx][(pc, phist)]["num"] += 1
                                same_pc_his += 1
                                if tokens[3] == 'M':
                                    br_pc_list[period_idx][(pc, phist)]["miss"] += 1
                                    same_pc_his_miss += 1
                                else:
                                    br_pc_list[period_idx][(pc, phist)]["hit"] += 1
                                if tokens[4] != br_pc_list[period_idx][(pc, phist)]["last_outcome"]:
                                    diff_than_prev += 1
                            else:
                                matched_pc_his = False
                                unique_pc_his += 1
                                br_pc_list[period_idx][(pc, phist)] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0, 
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
                            if tokens[3] == 'M':
                                if tmp_print_cnt < max_pc_print_cnt:
                                    # print(hex(pc))
                                    tmp_print_cnt += 1
                                    f_pc_trace1.write(hex(pc))
                                    f_pc_trace1.write(' ' + phist + ' ' + tokens[4] + '\n')
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
                            # update total miss/hit in branch history entries
                            if tokens[3] == 'M':
                                total_miss += 1
                            if len(ghist) < his_len:
                                ghist += tokens[4]
                            else:
                                ghist = ghist[1:] + tokens[4]
                        else:
                            if insn_cnt == 0:
                                br_pc = br_pc_list[0]
                            if "Heartbeat CPU 0" in line:
                                insn_cnt = int(tokens[4])
                                if insn_cnt % 10000000 < 10:
                                    print(insn_cnt)
                                # if insn_cnt > end_insn:
                                if insn_cnt >= period_insn * (period_idx + 1):
                                    common_miss_bench_list.append((common_miss - common_miss_last)/(total_miss - total_miss_last))
                                    common_miss_last = common_miss
                                    total_miss_last = total_miss
                                    x_insn_count.append(insn_cnt)
                                    # print(common_miss, total_miss)
                                    period_idx += 1
                                    if period_idx >= len(br_pc_list):
                                        break
                                    br_pc = br_pc_list[period_idx]
                                if insn_cnt >= end_insn:
                                    break
                            if len(tokens) < 5:
                                continue
                            pc = 0
                            if tokens[0] == "ip":
                                pc = int(tokens[1], 16)
                            else:
                                continue
                            phist = ghist
                            if (pc, phist) in br_pc:
                                # Check if using last result is correct
                                if tokens[4] == br_pc[(pc, phist)]["last_outcome"]:
                                    if tokens[3] == 'M':
                                        common_miss_correct += 1
                                else:
                                    if tokens[3] == 'H':
                                        common_miss_wrong += 1
                                if tokens[3] == 'M':
                                    common_miss += 1
                            if tokens[3] == 'M':
                                total_miss += 1
                                if tmp_print_cnt < max_pc_print_cnt:
                                    # print(hex(pc))
                                    tmp_print_cnt += 1
                                    f_pc_trace2.write(hex(pc))
                                    f_pc_trace2.write(' ' + phist + ' ' + tokens[4] + '\n')
                            if len(ghist) < his_len:
                                ghist += tokens[4]
                            else:
                                ghist = ghist[1:] + tokens[4]
            
                
                print("Total Branch:", line_cnt)
                print("Unique PC and History", unique_pc_his, "Tuple Matched", same_pc_his, "Diff than prev(Reload won't help):", diff_than_prev, "Same PC and History but misses", same_pc_his_miss)
                print("Branch misses:", total_miss)
            
                print(bench_l, "Common misses:", common_miss, common_miss/total_miss)
                print(bench_l, "Originally wrong -> correct:", common_miss_correct, common_miss_correct/total_miss)
                print(bench_l, "Originally correct -> wrong:", common_miss_wrong)
                print(bench_l, "Common misses reduction,", common_miss_correct - common_miss_wrong)
                # sort_misses(br_pc_list[0])
                if bench_round > 1:
                    common_miss_all_list.append(common_miss_bench_list)
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
        # with open("miss_common_progress" + str(his_len) +".csv", "w") as f_output:
        #     store_list(f_output, common_miss_all_list)

    print("Progressive Results", common_miss_all_list)
    common_miss_corr_list.append(statistics.mean(common_miss_all_list[0]))
    print("Average 128: ", statistics.mean(common_miss_all_list[0]))
    # print("Average 256: ", statistics.mean(common_miss_all_list[1]))
    # print("Average 512: ", statistics.mean(common_miss_all_list[2]))
    # print("Average 1024: ", statistics.mean(common_miss_all_list[3]))


f_pc_trace1.close()
f_pc_trace2.close()


# Store the results
def store_list(fp, li):
    fp.write(str(li[0]))
    for token in li[1:]:
        fp.write(",")
        fp.write(str(token))
    fp.write("\n")
    return

# with open("miss_common_progressive_corr.csv", "w") as f_output:
#     store_list(f_output, common_miss_corr_list)
# print(common_miss_corr_list)

# font = {'weight' : 'bold',
#         'size'   : 14}
# 
# plt.rc('font', **font)
# fig, axs = plt.subplots(1, 1, figsize=(10, 6))
# axs.plot(x_insn_count, common_miss_all_list[0],  linewidth=2, label = 'History Length 128')
# # axs.plot(x_insn_count, common_miss_all_list[1],  linewidth=2, label = 'History Length 256')
# # axs.plot(x_insn_count, common_miss_all_list[2],  linewidth=2, label = 'History Length 512')
# # axs.plot(x_insn_count, common_miss_all_list[3],  linewidth=2, label = 'History Length 1024')
# axs.set_ylabel('% of Common Miss')
# axs.set_xlabel('Insn Count')
# axs.set_title(bench_labels[0])
# handles, labels = axs.get_legend_handles_labels()
# plt.subplots_adjust(top=0.80, bottom=0.1, left=0.095, right=0.985, hspace=0.2, wspace=0.2)
# fig.legend(handles, labels, loc='upper right', ncol=2)
# 
# fig.savefig("Miss_common_progress_conv" + str(corr_delta) + "_" + bench_labels[0] + ".png")
# plt.show()

#    x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
#    # colors = ['cornflowerblue', 'coral', 'limegreen', 'darkviolet']
#    colors = ['darkviolet', 'cornflowerblue', 'cadetblue', 'paleturquoise']
#    
#    color_id = 0
#    for his_len in [128, 256, 512, 1024]:
#        common_miss_all_list = []
#        with open("miss_common_insn990000000_his" + str(his_len) + ".csv", "r") as f_r:
#            for line in f_r:
#                tokens = line.split(",")
#                for token in tokens:
#                    common_miss_all_list.append(float(token))
#            print(np.average(np.array(common_miss_all_list)))
#        axs.bar(x_bar_pos + color_id * 0.1, np.array(common_miss_all_list) * 100, width=0.1, color=colors[color_id], label='History Length ' + str(his_len) + 'bits')
#        color_id += 1
#    
#    # axs.plot(x_insn_count, common_miss_list, linewidth=2, color = 'black', label = 'Common miss percentage')
#    # axs.plot(x_insn_count, y1, linewidth=2, color = 'cornflowerblue', label = 'Compulsory Misses')
#    # axs.plot(x_insn_count, y1 + y2, linewidth=2, color = 'coral', label = 'Conflict Misses')
#    # axs.fill_between(x_insn_count, y0, y1, color = 'cornflowerblue', label = 'Compulsory Misses')
#    # axs.fill_between(x_insn_count, y1, y1 + y2, color = 'coral', label = 'Conflict Misses')
#    # axs.fill_between(x_insn_count, y1 + y2, y_bp_mpki, color = 'c', label = 'Capacity Misses')
#    
#    
#    # axs.bar(x_bar_pos, compulsory_miss_list, width=0.3, color='deepskyblue', label='Compulsory')
#    # axs.bar(x_bar_pos, conflict_miss_list, bottom=y1, width=0.3, color='coral', label='Conflict')
#    # axs.bar(x_bar_pos, y_low, bottom=y1, alpha=1, width=0.285, color='coral', edgecolor='black', hatch='//', label='Conflict at Lower Banks')
#    # axs.bar(x_bar_pos, capacity_miss_list, bottom=y1+y2, width=0.3, color='c', label='Capacity')
#    axs.set_ylabel('% of Common Miss')
#    # axs.set_xlabel('Instructions')
#    axs.set_xticks(x_bar_pos + 0.15, bench_labels, rotation=45, ha='right')
#    axs.set_ylim([0,100])
#    handles, labels = axs.get_legend_handles_labels()
#    plt.subplots_adjust(top=0.87, bottom=0.280, left=0.095, right=0.985, hspace=0.2, wspace=0.2)
#    fig.legend(handles, labels, loc='upper right', ncol=2)
#    plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
#    # ax2 = axs.twinx()
#    # ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
#    # ax2.set_ylabel('MPKI')
#    fig.savefig("Miss_common_progress.eps", format='eps')
#    plt.show()
