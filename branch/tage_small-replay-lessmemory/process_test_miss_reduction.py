# f_trace_common = "pc_his_common_miss_real_trace_rnnserving.txt"
# f_trace_common = "pc_his_common_miss_real_trace_imageprocessing.txt"
# f_trace_common = "pc_his_common_miss_real_trace_chameleon.txt"
# f_trace_common = "pc_his_common_miss_real_trace_videoprocessing.txt"
# f_trace_common = "pc_his_common_miss_real_trace_matmul.txt"
# f_trace_common = "pc_his_common_miss_real_trace_linpack.txt"
# f_trace_common = "pc_his_common_miss_real_trace_pyaes.txt"
# f_trace_common = "pc_his_common_miss_real_trace_modelserving.txt"
# f_trace_common = "pc_his_common_miss_real_trace_modeltraining.txt"
f_trace_common = "pc_his_common_miss_real_trace_floatoperation.txt"
# pc_his_common = open(f_trace_o, "w")
line_cnt = 0
pc_his_list = []
pc_his_dic_all = {}
with open(f_trace_common, "r") as f_test:
    for line in f_test:
        tokens = line.split()
        phist = tokens[1] + '_' + tokens[2] + '_' + tokens[3]
        pc_his_list.append([int(tokens[0], 16), phist, tokens[4], tokens[5]])
        pc_his_dic_all[(int(tokens[0], 16), phist)] = [tokens[4], tokens[5]]
        line_cnt += 1
        if line_cnt % 10000 == 0:
            print("Line_cnt: ", line_cnt, "Insn_cnt", int(tokens[5]))
        
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_14-59-00-imageprocessing.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-25_-_00-29-28-rnnserving.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-32-28-chameleon_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-16-videoprocessing.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-44-43-matmul_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-54-11-linpack_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-58-23-pyaes_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_21-33-50-modelserving.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_16-37-19-modeltraining.trace_detailed_misses_reasons_his_tagesmall_base.out"
fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-36-38-floatoperation_short.trace_detailed_misses_reasons_his_tagesmall_base.out"


# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-33-00-chameleon_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2024-03-26_-_17-34-33-chameleon_short.trace_detailed_misses_reasons_tageonly_base.out"


# his_len = 1024
# Have a prefetch buffer
####    buffer_len = 512
####    # init buffer
####    idx_pc_his = 0
####    pc_his_dic = {}
####    for i in range(buffer_len):
####        pc_his_dic[(pc_his_list[i][0], pc_his_list[i][1])] = [pc_his_list[i][2], pc_his_list[i][3]]
####        idx_pc_his += 1

with open(fname, "r") as f_trace_new_bench:
    line_cnt = 0
    insn_cnt = 0
    corrected = 0
    corr2wrong = 0
    total_miss_original = 0
    phist = ""
    pc_his_useful = {}
    for line in f_trace_new_bench:
        tokens = line.split()
        line_cnt += 1
        # find current insn count
        if "Heartbeat CPU 0" in line:
            insn_cnt = int(tokens[4])
            #####    # update pc_his_dic
            #####    while int(list(pc_his_dic.values())[-1][1]) < insn_cnt + 100:
            #####        # pop the oldest entry
            #####        # pc_his_dic.pop(next(iter(pc_his_dic)))
            #####        pc_his_dic[(pc_his_list[idx_pc_his][0], pc_his_list[idx_pc_his][1])] = [pc_his_list[idx_pc_his][2], pc_his_list[idx_pc_his][3]]
            #####        idx_pc_his += 1
            if insn_cnt % 1000000  < 100:
                print(insn_cnt)
                print("Corrected:", corrected, "Correct to worng", corr2wrong)
                print("Original total miss:", total_miss_original, "Corrected", corrected-corr2wrong)
            continue
        if len(tokens) < 5:
            continue
        if tokens[0] == "ip":
            pc = int(tokens[1], 16)
        else:
            continue
        phist = '22_' + tokens[10] + '_' + tokens[11]
        ####    if (pc, phist) in pc_his_dic:
        ####        if pc_his_dic[(pc, phist)][0] == tokens[4]:
        if (pc, phist) in pc_his_dic_all:
            use_pc_his = True
            if (pc, phist) not in pc_his_useful:
                pc_his_useful[(pc, phist)] = 0
            else:
                if pc_his_useful[(pc, phist)] < 0:
                    use_pc_his = False
            if pc_his_dic_all[(pc, phist)][0] == tokens[4]:
                if tokens[3] == 'M':
                    if use_pc_his:
                        corrected += 1
                    pc_his_useful[(pc, phist)] += 1
                    if pc_his_useful[(pc, phist)] > 3:
                        pc_his_useful[(pc, phist)] = 3
            else:
                if tokens[3] == 'H':
                    if use_pc_his:
                        corr2wrong += 1
                        # print(hex(pc), phist)
                    pc_his_useful[(pc, phist)] -= 1
                    if pc_his_useful[(pc, phist)] < -3:
                        pc_his_useful[(pc, phist)] = -3
        # if len(phist) < his_len:
        #     phist += tokens[4]
        # else:
        #     phist = phist[1:] + tokens[4]
        if tokens[3] == 'M':
            total_miss_original += 1
    print("Corrected:", corrected, "Correct to worng", corr2wrong)
    print("Original total miss:", total_miss_original, "Corrected", corrected-corr2wrong)

