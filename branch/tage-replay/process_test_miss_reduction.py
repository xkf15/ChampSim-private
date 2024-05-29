f_trace_common = "pc_his_common_miss_trace.txt"
# pc_his_common = open(f_trace_o, "w")
line_cnt = 0
pc_his_list = []
pc_his_dic_all = {}
with open(f_trace_common, "r") as f_test:
    for line in f_test:
        tokens = line.split()
        pc_his_list.append([int(tokens[0], 16), tokens[1], tokens[2], tokens[3]])
        pc_his_dic_all[(int(tokens[0], 16), tokens[1])] = [tokens[2], tokens[3]]
        line_cnt += 1
        if line_cnt % 10000 == 0:
            print("Line_cnt: ", line_cnt, "Insn_cnt", int(tokens[3]))
        
fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-32-28-chameleon_short.trace_store_states_tageonly_pid.out"
# fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2024-03-26_-_17-34-33-chameleon_short.trace_detailed_misses_reasons_tageonly_base.out"


his_len = 1024
# Have a prefetch buffer
buffer_len = 16000
# init buffer
idx_pc_his = 0
pc_his_dic = {}
for i in range(buffer_len):
    pc_his_dic[(pc_his_list[i][0], pc_his_list[i][1])] = [pc_his_list[i][2], pc_his_list[i][3]]
    idx_pc_his += 1

with open(fname, "r") as f_trace_new_bench:
    line_cnt = 0
    insn_cnt = 0
    corrected = 0
    corr2wrong = 0
    total_miss_original = 0
    phist = ""
    for line in f_trace_new_bench:
        tokens = line.split()
        # find current insn count
        if "Heartbeat CPU 0" in line:
            insn_cnt = int(tokens[4])
            # update pc_his_dic
            while int(list(pc_his_dic.values())[-1][1]) < insn_cnt + 100:
                # pop the oldest entry
                # pc_his_dic.pop(next(iter(pc_his_dic)))
                pc_his_dic[(pc_his_list[idx_pc_his][0], pc_his_list[idx_pc_his][1])] = [pc_his_list[idx_pc_his][2], pc_his_list[idx_pc_his][3]]
                idx_pc_his += 1
            #if insn_cnt % 100000  < 100:
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
        line_cnt += 1
        if (pc, phist) in pc_his_dic:
            if pc_his_dic[(pc, phist)][0] == tokens[4]:
        # if (pc, phist) in pc_his_dic_all:
        #     if pc_his_dic_all[(pc, phist)][0] == tokens[4]:
                if tokens[3] == 'M':
                    corrected += 1
            else:
                if tokens[3] == 'H':
                    corr2wrong += 1
        if len(phist) < his_len:
            phist += tokens[4]
        else:
            phist = phist[1:] + tokens[4]
        if tokens[3] == 'M':
            total_miss_original += 1
    print("Corrected:", corrected, "Correct to worng", corr2wrong)
    print("Original total miss:", total_miss_original, "Corrected", corrected-corr2wrong)

