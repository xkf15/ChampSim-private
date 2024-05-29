import numpy as np
import matplotlib.pyplot as plt

line_size = 32
bench_names = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",  
        "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]

font = {'weight' : 'bold',
        'size'   : 18}

####plt.rc('font', **font)
####fig, axs = plt.subplots(1, 1, figsize=(10, 7))
####
####for bench in bench_names:
####    fn = "pc_his_common_miss_real_trace_" + bench + ".txttmp"
####    with open(fn, "r") as fn:
####        all_ranges = []
####        all_temporal = []
####        line_cnt = 0
####        start_pc = 0
####        end_pc = 0
####        for line in fn:
####            tokens = line.split()
####            if line_cnt == 0:
####                start_pc = int(tokens[0], 16)
####            elif line_cnt == 31:
####                end_pc = int(tokens[0], 16)
####                if (end_pc - start_pc) > 0:
####                    all_ranges.append(end_pc - start_pc)
####            line_cnt += 1
####            if line_cnt >= 32:
####                line_cnt = 0
####        data_sorted = np.sort(all_ranges)
####        cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
####    # plt.figure(figsize=(8, 5))
####    # plt.plot(data_sorted, cdf, marker='.', linestyle='-', color='b')
####    # plt.show()
####
####    # x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
####    # axs.bar(x_bar_pos, 100*(y2/y1 - 1), width=0.2, color='limegreen', label='IPC Improvement with Prefetch')
####    # axs.bar(x_bar_pos+0.2, 100*(upperbound_ipc/y1 - 1), width=0.2, color='darkgreen', label='Upperbound')
####    axs.plot(data_sorted, cdf, linestyle='-', label=bench)
####    axs.set_xlim([2, 0xffffff])
####    axs.set_xscale('log')
####    # axs.set_xticks(x_bar_pos+0.1, bench_names, fontsize=14, rotation=45, ha='right')
####axs.set_ylabel('CDF of Address Range in One Line', fontweight='bold')
####axs.set_xlabel('Address Range in One Line (Biggest PC - Smallest PC)', fontweight='bold')
####handles, labels = axs.get_legend_handles_labels()
####plt.subplots_adjust(top=0.845, bottom=0.1, left=0.1, right=0.985, hspace=0.2, wspace=0.2)
####plt.grid(linestyle = '--', linewidth = 0.5)
####fig.legend(handles, labels, loc='upper right', ncol=4, fontsize = 13)
##### fig.legend(fontsize = 14)
####fig.savefig("Prefetch_Table_CDF.eps", format='eps')
####plt.show()


plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 7))

pc_all = {}
insn_all = [213945005, 85195000, 288530006, 54095001, 999995004, 206000000, 304600007, 999995000, 999995006, 999995007]
for i in range(10):
    bench = bench_names[i]
    fn = "pc_his_common_miss_real_trace_" + bench + ".txt"
    with open(fn, "r") as fn:
        all_temporal = []
        line_cnt = 0
        for line in fn:
            tokens = line.split()
            tmp_pc  = int(tokens[0], 16)
            if tmp_pc in pc_all:
                continue
            else:
                pc_all[tmp_pc] = 0
                all_temporal.append(int(tokens[5]))
        # data_sorted = np.sort(all_temporal) / insn_all[i] * 100
        data_sorted = np.sort(all_temporal)
        cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    # plt.figure(figsize=(8, 5))
    # plt.plot(data_sorted, cdf, marker='.', linestyle='-', color='b')
    # plt.show()

    # x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
    # axs.bar(x_bar_pos, 100*(y2/y1 - 1), width=0.2, color='limegreen', label='IPC Improvement with Prefetch')
    # axs.bar(x_bar_pos+0.2, 100*(upperbound_ipc/y1 - 1), width=0.2, color='darkgreen', label='Upperbound')
    axs.plot(data_sorted, cdf, linestyle='-', label=bench)
    axs.set_xlim([0, 100])
    # axs.set_xticks(x_bar_pos+0.1, bench_names, fontsize=14, rotation=45, ha='right')
axs.set_ylabel('CDF of First Occurrence Timing for \n Hard-to-Predict Branches', fontweight='bold')
axs.set_xlabel('Instructions Executed in Function Invocation', fontweight='bold')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.845, bottom=0.1, left=0.13, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5)
fig.legend(handles, labels, loc='upper right', ncol=4, fontsize = 13)
# fig.legend(fontsize = 14)
fig.savefig("Prefetch_Temporal_CDF.eps", format='eps')
plt.show()
