import numpy as np
import os

# fn1 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-50-modelserving.trace_detailed_misses_reasons_base.out"
# fn1 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-31-imageprocessing.trace_detailed_misses_reasons_base.out"
# fn1 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-25_-_00-29-28-rnnserving.trace_detailed_misses_reasons_tagesmall_base.out"
# fn1 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-25_-_00-29-28-rnnserving.trace_detailed_misses_reasons_base.out"
# fn2 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-50-modelserving.trace_load_states_lessmemory.out"
# fn2 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-31-imageprocessing.trace_load_states_lessmemory.out"
# fn2 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-25_-_00-29-28-rnnserving.trace_load_states_tagesmall_lessmemory.out"
# fn2 = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-25_-_00-29-28-rnnserving.trace_load_states_lessmemory.out"

bench_labels = ["chameleon", "floatoperation", "linpack", "rnnserving", "videoprocessing",
                "matmul", "pyaes", "imageprocessing", "modelserving", "modeltraining"]
# bench_labels = ["imageprocessing"]
f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"
end_insn = 80000000 # 990000000
period_insn = 5000000

for i in range(len(bench_labels)):
    for fn in os.listdir(f_dir):
        # if "detailed_misses_reasons_2" in fn and bench_labels[i] in fn:
        if "detailed_misses_reasons_base" in fn and bench_labels[i] in fn:
        # if "load_states_lessmemory" in fn and bench_labels[i] in fn:
            # fnames.append(f_dir + fn)
            fn1 = f_dir + fn
            break

    for fn in os.listdir(f_dir):
        if "load_states_lessmemory" in fn and bench_labels[i] in fn:
            # fnames.append(f_dir + fn)
            fn2 = f_dir + fn
            break

    tmp_miss_list = []
    total_miss_1 = 0
    line_num_1 = 0
    tmp_miss_1 = 0
    with open(fn1, "r") as f_1:
        for line in f_1:
            tokens = line.split()
            if "ip " not in line or len(tokens) != 6:
                continue
            if tokens[3] == 'M':
                total_miss_1 += 1
                tmp_miss_1 += 1
            line_num_1 += 1
            if line_num_1 % 10000 == 0:
                tmp_miss_list.append(tmp_miss_1)
                # print(total_miss_1, tmp_miss_1)
                tmp_miss_1 = 0
                if line_num_1 >= end_insn:
                    break
            if line_num_1 % 10000000 == 0:
                print(line_num_1) 
    
    line_num_2 = 0
    total_miss_2 = 0
    total_reduce = 0
    max_reduce = 0
    max_reduce_idx = 0
    max_reduce_line_num = 0
    tmp_miss_2 = 0
    tmp_idx = 0
    delta_miss = 0
    with open(fn2, "r") as f_2:
        tmp_idx = 0
        for line in f_2:
            tokens = line.split()
            if "ip " not in line or len(tokens) != 6:
                continue
            if tokens[3] == 'M':
                total_miss_2 += 1
                tmp_miss_2 += 1
            line_num_2 += 1
            if line_num_2 % 10000 == 0:
                # print("Current extra miss ", tmp_miss_2 - tmp_miss_list[tmp_idx])
                delta_miss += tmp_miss_2 - tmp_miss_list[tmp_idx]
                tmp_idx += 1
                tmp_miss_2 = 0
                if delta_miss <= max_reduce:
                    # print("Max Reduction", delta_miss, "Original Misses", np.sum(tmp_miss_list[0:tmp_idx]), "Branch count:", line_num_2)
                    max_reduce = delta_miss
                    max_reduce_idx = tmp_idx
                    max_reduce_line_num = line_num_2
                # else:
                #     print("Delta:", delta_miss, "Original Misses", np.sum(tmp_miss_list[0:tmp_idx]), "Branch count:", line_num_2)
                if line_num_2 >= end_insn:
                    break
            if line_num_2 % 10000000 == 0:
                print(line_num_2) 
    
   #  plt.rc('font', **font)
    print("Original Total miss:", total_miss_1, "Current:", total_miss_2)
    # print("Max Reduction", delta_miss, "Original Misses", np.sum(tmp_miss_list[0:max_reduce_idx]))
    print("Max Reduction", max_reduce, "Original Misses", np.sum(tmp_miss_list[0:max_reduce_idx]), "Branch count:", max_reduce_line_num)
    # print("Max reduce insn:", max_reduce_insn, "Reduce:", max_reduce)
