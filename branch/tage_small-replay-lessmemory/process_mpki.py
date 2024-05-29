from collections import OrderedDict
import random
import numpy as np
import matplotlib.pyplot as plt
import os

bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing", 
                "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]

br_mpki_list=[5.38331, 4.83208, 3.11057, 4.68831, 3.97977, 4.89877, 5.60884, 2.92702, 5.81725, 2.08726]

font = {'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 5))
x_bar_pos = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
y1 = np.array(br_mpki_list)
print("Average BP MPKI", np.average(y1))
axs.bar(x_bar_pos, y1, width=0.3, color='sandybrown', label='128Kbits TAGE-SC-L')
# axs.bar(x_bar_pos, y2, width=0.3, color='limegreen', label='No Branch Missprediction')
axs.set_ylabel('MPKI', fontweight='bold')
# axs.set_xlabel('Instruction Count')
axs.set_xticks(x_bar_pos, bench_labels, fontsize=14, rotation=45, ha='right')
# ax2 = axs.twinx()
# ax2.plot(x_insn_count, y_bp_mpki, linestyle='dashed', linewidth=2, color = 'firebrick', label = 'MPKI')
# ax2.set_ylabel('MPKI')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.875, bottom=0.325, left=0.075, right=0.985, hspace=0.2, wspace=0.2)
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
fig.legend(handles, labels, loc='upper right', ncol=2)
fig.savefig("MPKI.eps", format='eps')
plt.show()
