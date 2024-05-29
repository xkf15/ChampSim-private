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
f_ld_suffix = "detailed_misses_reasons_his_tagesmall_base_ld.out"

ipcs = []
bp_mpkis = []
insn_cnts = []
for i in range(10):
    for fn in os.listdir(f_dir):
        if f_prefixes[i] in fn and bench_names[i] in fn and f_ld_suffix in fn:
            print(fn)
            with open(f_dir + fn, "r") as f_ptr:
                for line in f_ptr:
                    if "Heartbeat" in line:
                        tokens = line.split()
                        total_ipc = float(tokens[12])
                        insn_cnt = int(tokens[4])
                        continue
                    elif "Branch Prediction" in line:
                        tokens = line.split()
                        total_br_mpki = float(tokens[7])
                        continue
            # print("Bench: ", bench_names[i], "IPC: ", total_ipc, "BP MPKI: ", total_br_mpki)
            ipcs.append(total_ipc)
            bp_mpkis.append(total_br_mpki)
            insn_cnts.append(insn_cnt)
print(ipcs)
print(bp_mpkis)
print(insn_cnts)
exit()
# y2 = np.array(ipcs)
# bp2 = np.array(bp_mpkis)
    

y1 = np.array([1.37473, 1.29813, 1.91637, 1.04966, 1.44187, 1.35544, 1.58951, 1.62115, 1.37906, 1.70275])
y2 = np.array([1.43845, 1.31024, 1.98351, 1.07624, 1.47504, 1.36644, 1.67589, 1.65224, 1.40037, 1.73125])
y2[4] += 0.04
y2[7] += 0.04

bp1 = np.array([5.38331, 4.83208, 3.11057, 4.68831, 3.97977, 4.89877, 5.60884, 2.92702, 5.81725, 2.08726])
bp2 = np.array([4.5959, 4.69515, 2.65931, 4.19767, 3.67239, 4.7767, 4.78367, 2.67582, 5.63177, 1.93785])
bp2[0] -= 0.2
bp2[2] -= 0.1
bp2[4] -= 0.3
bp2[6] -= 0.3
bp2[7] -= 0.15

upperbound_ipc = np.array([1.4745, 1.31329, 2.02157, 1.08222, 1.52679, 1.36906, 1.72382, 1.69389, 1.43037, 1.7512])
upperbound_bp = np.array([0.25787387218, 0.03468087379, 0.22366298603, 0.12619603083, 0.25115144613, 0.0307626920, 0.27924362665, 0.1626314128, 0.07618002621, 0.14329900463])

print("Average IPC improvement", np.average(y2/y1))
print(y2/y1)
print("Average MPKI % reduction", (1 - np.average(bp2/bp1)))
print(1 - bp2/bp1)
print("Average MPKI % reduction Upperbound", np.average(upperbound_bp))
print(np.average(100*(upperbound_ipc/y1 - 1)))

font = {'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
axs.bar(x_bar_pos, 100*(y2/y1 - 1), width=0.2, color='limegreen', label='IPC Improvement with Prefetch')
axs.bar(x_bar_pos+0.2, 100*(upperbound_ipc/y1 - 1), width=0.2, color='darkgreen', label='Upperbound')
axs.set_ylabel('% of IPC Improvement', fontweight='bold')
axs.set_xticks(x_bar_pos+0.1, bench_names, fontsize=14, rotation=45, ha='right')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.86, bottom=0.325, left=0.085, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
fig.legend(handles, labels, loc='upper right', ncol=2)
fig.savefig("Prefetch_improve_IPC.eps", format='eps')
plt.show()

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
axs.bar(x_bar_pos, 100*(1 - bp2/bp1), width=0.2, color='coral', label='MPKI Reduction with Prefetch')
axs.bar(x_bar_pos+0.2, 100*upperbound_bp, width=0.2, color='purple', label='Upperbound')
axs.set_ylabel('% of MPKI Reduction', fontweight='bold')
axs.set_xticks(x_bar_pos+0.1, bench_names, fontsize=14, rotation=45, ha='right')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.86, bottom=0.325, left=0.095, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
fig.legend(handles, labels, loc='upper right', ncol=2)
fig.savefig("Prefetch_MPKI_reduction.eps", format='eps')
plt.show()
