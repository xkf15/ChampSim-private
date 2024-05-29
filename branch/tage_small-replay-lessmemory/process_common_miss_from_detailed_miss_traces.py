import os
f_dir = "/scratch/gpfs/kaifengx/function_bench_results/"
f_prefix = "nokvm-2024-04-1"
# f_prefix = "nokvm-2024-03"
# bench = "chameleon_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
# bench = "rnnserving"
# bench = "imageprocessing"
# bench = "chameleon"
# bench = "videoprocessing"
# bench = "floatoperation"
# bench = "matmul"
# bench = "linpack"
# bench = "pyaes"
# bench = "modelserving"
bench = "modeltraining"
f_suffix = "detailed_misses_reasons_his_tagesmall_base.out"

fnames = []
for fn in os.listdir(f_dir):
    if f_prefix in fn and bench in fn and f_suffix in fn:
        fnames.append(f_dir + fn)
for fn in os.listdir(f_dir):
    if "nokvm-2023-11-2" in fn and bench in fn and f_suffix in fn:
        fnames.append(f_dir + fn)
# fnames.reverse()
print(fnames)
# exit()


f_cnt = 0
his_len = 1024
for fn in fnames:
    with open(fn, "r") as f_br:
        print("Start File " + str(f_cnt))
        fn_o = "miss_trace_real_" + bench + str(f_cnt) + ".txt"
        if fn_o in os.listdir("./"):
            print("File " + str(f_cnt) + " Exists")
            # just generate once
            continue
        f_miss_trace = open(fn_o, "w")
        f_cnt += 1
        insn_cnt = 0
        for line in f_br:
            tokens = line.split()
            if "Heartbeat CPU 0" in line:
                insn_cnt = int(tokens[4])
                continue
            if len(tokens) < 9:
                continue
            if tokens[0] == "ip":
                pc = int(tokens[1], 16)
            else:
                continue
            if tokens[3] == 'M':
                # phist = '21_' + tokens[8] + '_' + tokens[9]
                # f_miss_trace.write(hex(pc))
                # f_miss_trace.write(' ' + phist + ' ' + tokens[4] + ' ' + str(insn_cnt) + '\n')
                phist = '22_' + tokens[10] + '_' + tokens[11]
                f_miss_trace.write(hex(pc))
                f_miss_trace.write(' ' + phist + ' ' + tokens[4] + ' ' + str(insn_cnt) + '\n')


# for fn in fnames:
#     with open(fn, "r") as f_br:
#         print("Start File " + str(f_cnt))
#         fn_o = "miss_trace" + str(f_cnt) + ".txt"
#         f_cnt += 1
#         f_miss_trace = open(fn_o, "w")
#         line_cnt = 0
#         insn_cnt = 0
#         br_pc_list = {}
#         phist = ""
#         for line in f_br:
#             tokens = line.split()
#             # find current insn count
#             if "Heartbeat CPU 0" in line:
#                 insn_cnt = int(tokens[4])
#                 continue
#             if len(tokens) < 5:
#                 continue
#             if tokens[0] == "ip":
#                 pc= int(tokens[1], 16)
#             else:
#                 continue
#             line_cnt += 1
#             if (pc, phist) in br_pc_list:
#                 matched_pc_his = True
#                 br_pc_list[(pc, phist)]["num"] += 1
#                 if tokens[3] == 'M':
#                     br_pc_list[(pc, phist)]["miss"] += 1
#                 else:
#                     br_pc_list[(pc, phist)]["hit"] += 1
#             else:
#                 br_pc_list[(pc, phist)] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0,
#                         "h_t": 0, "m_t": 0, "h_l": 0, "m_l": 0, "h_s": 0, "m_s": 0, "last_outcome": tokens[4]}
#             if tokens[3] == 'M':
#                 f_miss_trace.write(hex(pc))
#                 f_miss_trace.write(' ' + phist + ' ' + tokens[4] + ' ' + str(insn_cnt) + '\n')
#             if len(phist) < his_len:
#                 phist += tokens[4]
#             else:
#                 phist = phist[1:] + tokens[4]
# 

pc_his_list_all = []
pc_his_all = {} # (pc, his) to [taken, not taken]
pc_all = {} # use this to remove all data dependent pc
def preprocess_all_common_miss(f_trace):
    trace1 = {}
    with open(f_trace, "r") as f_miss_trace:
        for line in f_miss_trace:
            tokens = line.split()
            if len(tokens) < 3:
                continue
            trace1[(tokens[0], tokens[1])] = tokens[2]
            if (tokens[0], tokens[1]) not in pc_his_all:
                if tokens[2] == '1':
                    pc_his_all[(tokens[0], tokens[1])] = [1, 0]
                else:
                    pc_his_all[(tokens[0], tokens[1])] = [0, 1]
                pc = tokens[0]
                if pc not in pc_all: # check how many unique PCs
                    pc_all[pc] = 1
                else:
                    pc_all[pc] += 1
            else:
                if tokens[2] == '1':
                    pc_his_all[(tokens[0], tokens[1])][0] += 1
                else:
                    pc_his_all[(tokens[0], tokens[1])][1] += 1
    pc_his_list_all.append(trace1)
    print("Finish preprocessing a trace")


def find_common_miss(f_trace1_i, f_trace2_i, f_common_o):
    # trace1 = []
    trace1 = {}
    with open(f_trace1_i, "r") as f_miss_trace:
    # with open("pc_trace_common.txt", "r") as f_miss_trace:
        for line in f_miss_trace:
            tokens = line.split()
            if len(tokens) < 3:
                continue
            # trace1.append(tokens)
            trace1[(tokens[0], tokens[1])] = tokens[2]

    print("Finish Trace 1, miss num:", len(trace1))

    idx_miss = 0
    matched = 0
    line_cnt = 0
    correct = 0
    if_matched = False
    
    pc_trace_common = open(f_common_o, "w")
    
    with open(f_trace2_i, "r") as f_miss_trace:
        for line in f_miss_trace:
            tokens = line.split()
            if len(tokens) < 3:
                continue
            if_matched = False
            i = (tokens[0], tokens[1])
            if i in trace1:
                pc_trace_common.write(line)
                matched += 1
                if_matched = True
                if tokens[2] == trace1[i]:
                    correct += 1
            line_cnt += 1
            if line_cnt % 10000 == 0:
                print("Line count:", line_cnt,"Matched:", matched, "Correct:", correct, "idx:", idx_miss)
    
    # pc_trace_common.close()
    print("Miss num:", line_cnt, "Matched:", matched, "Correct:", correct)
        
for i in range(len(fnames) - 1):
    preprocess_all_common_miss("miss_trace_real_" + bench + str(i) + ".txt")

common = 0
common_tuple = {}
for key in pc_his_all:
    (pc_tmp, his_tmp) = key
    find_cnt = 0
    for pc_his_dic in pc_his_list_all:
        if key in pc_his_dic:
            find_cnt += 1
    if find_cnt > 2:
        # if pc_tmp in pc_all: # remove data dependent branch
        #     if pc_all[pc_tmp] > 512:
        #         continue
        significant_taken = pc_his_all[key][0] * 1.0 / (pc_his_all[key][0] + pc_his_all[key][1]) - 0.5
        if significant_taken < 0.8 and significant_taken > 0.2:
            continue # remove data dependent branch
        common += 1
        common_tuple[key] = [significant_taken, -1] # 0: percentage taken, 1: smallest insn count that this showsup
        # common_tuple[key] = [0, -1]
print("All common:", common)


# Now pc_his_all is the common pc and history pairs
# Use this to test if we have match in those invocations

for i in range(len(fnames)):
    matched = 0
    line_cnt = 0
    correct = 0
    if_matched = False
    with open("miss_trace_real_" + bench + str(i) + ".txt", "r") as f_miss_trace:
        for line in f_miss_trace:
            tokens = line.split()
            if len(tokens) < 3:
                continue
            if_matched = False
            pc_his = (tokens[0], tokens[1])
            if pc_his in common_tuple:
                matched += 1
                if_matched = True
                if (int(tokens[2]) - 0.5) * common_tuple[pc_his][0] > 0:
                    correct += 1
                # # Test if this is a new place to insert entry
                if common_tuple[pc_his][1] < 0 or common_tuple[pc_his][1] > int(tokens[3]):
                    # # if taken +1, else -1
                    # if int(tokens[2]) > 0:
                    #     common_tuple[pc_his][0] += 1
                    # else:
                    #     common_tuple[pc_his][0] -= 1
                    common_tuple[pc_his][1] = int(tokens[3])
            line_cnt += 1
            # if line_cnt % 10000 == 0:
            #     print("Line count:", line_cnt,"Matched:", matched, "Correct:", correct, "idx:", idx_miss)
    print("Line count:", line_cnt,"Matched:", matched, "Correct:", correct)

# sort by PC first, and then insn_cnt next
def custom_sort_pc_insn(item):
    key, value = item
    pc, his = key
    return [pc, value[1]]

def custom_sort_insn(item):
    return item[1][1]

def write2file():
    # prefetch all misses when PC is reached
    sorted_dict_1 = dict(sorted(common_tuple.items(), key=lambda x: custom_sort_pc_insn(x)))
    f_trace_o = "pc_his_common_miss_real_trace_" + bench + ".txt"
    pc_his_common = open(f_trace_o + "tmp", "w")
    count = 0
    for key, value in sorted_dict_1.items():
        pc, his = key
        [t_nt, insn_cnt] = value
        # print(insn_cnt)
        # if abs(t_nt) <= 2:
        #     continue
        if t_nt >= 0:
            t_nt = '1'
        else:
            t_nt = '0'
        pc_his_common.write(pc + ' ' + his + ' ' + t_nt + ' ' + str(insn_cnt) + '\n')
        # pc, his = key
        # t_nt = value[0] 
        # insn_cnt = value[1]
        # if pc == pc_last:
        #     # sorted_dict_1.update({key: [t_nt, insn_cnt_last]})
        #     sorted_dict_1.update({key: value})
        # else:
        #     pc_last = pc
        #     insn_cnt_last = insn_cnt
        #     # if insn_cnt == 5000:
        #     #     print(key, value)
    pc_his_common.close()

    # pc_his_common_2.open(f_trace_o + "tmp", "r")
    dic2 = {}
    with open(f_trace_o + "tmp", "r") as pc_his_common_2:
        pc_last = ''
        insn_cnt_last = 0
        for line in pc_his_common_2:
            tokens = line.split()
            pc = tokens[0]
            his = tokens[1]
            t_nt = tokens[2]
            insn_cnt = int(tokens[3])
            if pc == pc_last:
                insn_cnt = insn_cnt_last
            else:
                pc_last = pc
                insn_cnt_last = insn_cnt
            dic2[(pc, his)] = [t_nt, insn_cnt]

    sorted_dict_2 = dict(sorted(dic2.items(), key=lambda x: custom_sort_insn(x)))

    pc_his_common_2 = open(f_trace_o, "w")
    for key, value in sorted_dict_2.items():
        pc, his = key
        [t_nt, insn_cnt] = value
        tokens_his = his.split('_') # 0: bank id, 1: index, 2: tag
        pc_his_common_2.write(pc + ' ' + tokens_his[0] + ' ' + tokens_his[1] + ' ' + tokens_his[2]  + ' ' + t_nt + ' ' + str(insn_cnt) + '\n')
        # if count < 10:
        #     print(key, value)
        #     count += 1
        # else:
        #     break
    pc_his_common_2.close()

write2file()


