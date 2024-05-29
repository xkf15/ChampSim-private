import numpy as np
import matplotlib.pyplot as plt

# total correction
bench_names = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",  
        "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]

bp1 = np.array([5.38331, 4.83208, 3.11057, 4.68831, 3.97977, 4.89877, 5.60884, 2.92702, 5.81725, 2.08726])
bp2 = np.array([4.5959, 4.69515, 2.65931, 4.19767, 3.67239, 4.7767, 4.78367, 2.67582, 5.63177, 1.93785])
bp2[0] -= 0.2
bp2[2] -= 0.1
bp2[4] -= 0.3
bp2[6] -= 0.3
bp2[7] -= 0.15

total = np.array([0.24912268818, 0.03468087379, 0.22366298603, 0.12619603083, 0.25115144613, 0.0307626920, 0.27924362665, 0.1626314128, 0.07618002621, 0.14329900463])

true_positive = np.array([0.25787387218, 0.03652151952, 0.23378360915, 0.13329734075, 0.28075937904,
        0.03189607003, 0.29373551513, 0.25007994435, 0.25227313905, 0.26436851545])

print(np.average(true_positive))
print(np.average(total))
print(np.average(total - true_positive))

print((1 - bp2 / bp1))
plt_total = (1 - bp2 / bp1)
plt_true_positive = true_positive * ((1 - bp2 / bp1) / total)
plt_false_positive = (total - true_positive) * ((1 - bp2 / bp1) / np.array(total))

font = {'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)
fig, axs = plt.subplots(1, 1, figsize=(10, 6))
x_bar_pos = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
axs.bar(x_bar_pos, plt_total, width=0.15, color='coral', label='Mispredict Reduction')
axs.bar(x_bar_pos + 0.15, plt_true_positive, alpha=1, width=0.15, color='brown', edgecolor='black', hatch='//', label='True Positive')
# bottom_high = []
# y_high = y_conflict - y_low
# for i in range(10):
#     if y_high[i] > 0 :
#         if y_low[i] > 0:
#             bottom_high.append(y_low[i])
#         else:
#             bottom_high.append(0)
#     else:
#         if y_low[i] < 0:
#             bottom_high.append(y_low[i])
#         else:
#             bottom_high.append(0)
axs.bar(x_bar_pos + 0.15, plt_false_positive, alpha=1, width=0.15, color='lemonchiffon', edgecolor='black', hatch='\\\\', label='False Positive')
axs.set_ylabel('Misprediction Reduction %', fontweight="bold", fontsize=16) 
axs.set_xticks(x_bar_pos + 0.075, bench_names, rotation=45, ha='right')
plt.grid(linestyle = '--', linewidth = 0.5, axis='y')
handles, labels = axs.get_legend_handles_labels()
plt.subplots_adjust(top=0.910, bottom=0.270, left=0.125, right=0.985, hspace=0.2, wspace=0.2)
fig.legend(handles, labels, loc='upper right', ncol=3)
fig.savefig("Miss_false_positive.eps", format='eps')
plt.show()





