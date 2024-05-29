import os
import numpy as np
import matplotlib.pyplot as plt
f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"

bench_names = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",  
        "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
f_prefixes = ["nokvm-2023-11-24_-_20-32-28-chameleon",
              "nokvm-2023-11-24_-_20-36-38-floatoperation",
              "nokvm-2023-11-24_-_20-54-11-linpack",
              "nokvm-2023-11-25_-_00-29-28-rnnserving",
              "nokvm-2023-11-24_-_21-33-16-videoprocessing",
              "nokvm-2023-11-24_-_20-44-43-matmul",
              "nokvm-2023-11-24_-_20-58-23-pyaes",
              "nokvm-2023-11-24_-_14-59-00-imageprocessing",
              "nokvm-2023-11-24_-_21-33-50-modelserving",
              "nokvm-2023-11-24_-_16-37-19-modeltraining"]
f_suffix = "detailed_misses_reasons_his_tagesmall_base.out"
buffersizes = [128, 256, 512, 1024]
f_ld_suffixes = ["detailed_misses_reasons_his_tagesmall_base_ld_buffersize128.out",
                 "detailed_misses_reasons_his_tagesmall_base_ld_buffersize256.out",
                 "detailed_misses_reasons_his_tagesmall_base_ld.out",
                 "detailed_misses_reasons_his_tagesmall_base_ld_buffersize1024.out"]

# for i in range(10):
#     head_move_cnt_all = []
#     for j in range(len(buffersizes)):
#         f_ld_suffix = f_ld_suffixes[j]
#         buffersize = buffersizes[j]
#         for fn in os.listdir(f_dir):
#             if f_prefixes[i] in fn and bench_names[i] in fn and f_ld_suffix in fn:
#                 print(fn)
#                 with open(f_dir + fn, "r") as f_ptr:
#                     head_move_cnt = 0
#                     bufferhead_last = 0
#                     insn = 0
#                     for line in f_ptr:
#                         if "Heartbeat" in line:
#                             tokens = line.split()
#                             insn = int(tokens[4])
#                             total_ipc = float(tokens[12])
#                             continue
#                         elif "Branch Prediction" in line:
#                             tokens = line.split()
#                             total_br_mpki = float(tokens[7])
#                             continue
#                         elif "bufferHead_ptr" in line:
#                             tokens = line.split()
#                             bufferheadptr = int(tokens[1])
#                             if abs(bufferheadptr - bufferhead_last) >  buffersize:
#                                 head_move_cnt += 1
#                 # print("Bench: ", bench_names[i], "IPC: ", total_ipc, "BP MPKI: ", total_br_mpki)
#                 # ipcs.append(total_ipc)
#                 # bp_mpkis.append(total_br_mpki)
#                 print(bench_names[i], "Head Move:", head_move_cnt, "Insn: ", insn)
#                 head_move_cnt_all.append(head_move_cnt)
#     print(head_move_cnt_all)

head_move_cnt_all = [[13059849, 11742834, 8988196,  7293476],
                    [3156662, 2930489, 2671296, 2421304],
                    [11436792, 10271537, 7801367, 6376751],
                    [2809669, 2488426, 1694476, 1257425],
                    [51160297, 46476845, 38747009, 34310138],
                    [4887997, 4409887, 3852480, 2741521],
                    [33117608, 29947603, 25046851, 21358103],
                    [37558120, 34930731, 29764828, 25850770],
                    [71169256, 67117550, 61551195, 57039592],
                    [120670255, 118341135, 95494334, 84327009]]
insn_cnt_all = [213945005, 85195000, 288530006, 54095001, 999995004, 206000000, 304600007, 999995000, 999995006, 999995007]


time_per_instruction = []
tmpdata = [[],[],[],[]]
aver = []
variations = []
for i in range(10):
    time_per_instruction.append(np.array(head_move_cnt_all[i]) / insn_cnt_all[i])
    tmpdata[0].append(head_move_cnt_all[i][0] / insn_cnt_all[i])
    tmpdata[1].append(head_move_cnt_all[i][1] / insn_cnt_all[i])
    tmpdata[2].append(head_move_cnt_all[i][2] / insn_cnt_all[i])
    tmpdata[3].append(head_move_cnt_all[i][3] / insn_cnt_all[i])
    if i == 9:
        for j in range(4):
            variations.append( np.std(tmpdata[j]) / np.sqrt(len(tmpdata[j])))
            aver.append(np.average(tmpdata[j]))
        # print(time_per_instruction[i])
        print(variations)
        print(aver)
aver = np.array(aver) * 0.9

miss_reduction = np.array([0.09034212415452347, 0.09793339578170257, 0.11123076239850138, 0.12191739662656809]) * 100
miss_reduction_var = np.array([0.02, 0.022, 0.024, 0.023]) * 100
bp1 = np.array([5.38331, 4.83208, 3.11057, 4.68831, 3.97977, 4.89877, 5.60884, 2.92702, 5.81725, 2.08726])
bp2 = np.array([4.5959, 4.69515, 2.65931, 4.19767, 3.67239, 4.7767, 4.78367, 2.67582, 5.63177, 1.93785])
bp2[0] -= 0.2
bp2[2] -= 0.1
bp2[4] -= 0.3
bp2[6] -= 0.3
bp2[7] -= 0.15
print(np.std(bp2/bp1) / np.sqrt(10))
    
font = {'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 6))
x_bar_pos = np.array([0, 0.5, 1, 1.5])
# for i in range(10):
#     axs.plot(x_bar_pos, time_per_instruction[i], linewidth=2, label = bench_names[i])

axs.set_xlabel('Size of Prefetch Buffer (# of Entries)', fontsize=16, fontweight='bold')
axs.set_xticks(x_bar_pos, ["128", "256", "512", "1024"], fontsize=14)
axs.set_ylabel("% of MPKI Reduction", fontsize=16, fontweight='bold')
axs.set_ylim([0, 15])
axs.bar(x_bar_pos, miss_reduction, yerr=miss_reduction_var, width=0.2, label = "Branch Misspredict Reduction")

ax2 = axs.twinx()
ax2.set_ylabel('# of Prefetch per Instruction', fontsize=16, fontweight='bold')
ax2.set_ylim([0, 0.18])
ax2.errorbar(x_bar_pos, aver, yerr=variations, color='red', linewidth=2, label = "Prefetch Frequency")

handles2, labels2 = ax2.get_legend_handles_labels()
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.88, bottom=0.14, left=0.105, right=0.875, hspace=0.2, wspace=0.2)
fig.legend(handles + handles2, labels + labels2, loc='upper right', fontsize=14, ncol=2)
fig.savefig("Prefetch_bandwidth.eps", format='eps')
plt.show()
# 
# 
# plt.rc('font', **font)
# fig, axs = plt.subplots(1, 1, figsize=(10, 5))
# x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
# axs.bar(x_bar_pos, 100*(y2/y1 - 1), width=0.3, color='limegreen', label='IPC Improvement with Prefetch')
# axs.set_ylabel('% of IPC Improvement')
# axs.set_xticks(x_bar_pos, bench_names, fontsize=14, rotation=45, ha='right')
# handles, labels = axs.get_legend_handles_labels()
# plt.subplots_adjust(top=0.86, bottom=0.325, left=0.085, right=0.985, hspace=0.2, wspace=0.2)
# plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
# fig.legend(handles, labels, loc='upper right', ncol=2)
# fig.savefig("Prefetch_improve_IPC.eps", format='eps')
# plt.show()
# 
# plt.rc('font', **font)
# fig, axs = plt.subplots(1, 1, figsize=(10, 5))
# x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
# axs.bar(x_bar_pos, 100*(1 - bp2/bp1), width=0.2, color='coral', label='MPKI Reduction with Prefetch')
# axs.bar(x_bar_pos+0.2, 100*upperbound, width=0.2, color='purple', label='Upperbound')
# axs.set_ylabel('% of MPKI Reduction')
# axs.set_xticks(x_bar_pos, bench_names, fontsize=14, rotation=45, ha='right')
# handles, labels = axs.get_legend_handles_labels()
# plt.subplots_adjust(top=0.86, bottom=0.325, left=0.085, right=0.985, hspace=0.2, wspace=0.2)
# plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
# fig.legend(handles, labels, loc='upper right', ncol=2)
# fig.savefig("Prefetch_MPKI_reduction.eps", format='eps')
# plt.show()
