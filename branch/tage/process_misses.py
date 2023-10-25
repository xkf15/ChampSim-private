from collections import OrderedDict



hot_miss = 0
hot_hit = 0
pc_history = []
max_pc_num = 10 # how many hot pcs to record for each period
real_num_his = [] # record how many pcs are really recorded, because sometimes only 1~2 pcs show up in that period
def preprocess_branch_misses(br_pc, insn_cnt):
    global hot_miss
    global hot_hit
    ordered = sorted(br_pc.items(), key=lambda i: i[1]["miss"], reverse=True)

    tmp_str = ''
    total_cnt = 0
    for k,v in ordered:
        # store first max_pc_num pcs into pc history
        if total_cnt < max_pc_num:
            hot_miss += v['miss']
            hot_hit += v['hit']
            print(hex(k), v)
            pc_history.append({'pc': k, 'local_his': '', 'table': {}, 'local_his_long': ''})
            total_cnt += 1
    real_num_his.append(total_cnt)
    # print(total_cnt)
    # assert(total_cnt == pc_num)

# only use local history
hot_miss_2 = 0
hot_hit_2 = 0
extra_miss_2 = 0
def process_hot_misses(pc_history_index, br_pc, taken, miss_hit):
    global hot_miss_2
    global hot_hit_2
    global extra_miss_2
    length_local = 100
    length_long = 1024
    ####### Second implementation
    if br_pc == pc_history[pc_history_index]['pc']:
        pattern = pc_history[pc_history_index]['local_his']
        pattern_idx = pc_history[pc_history_index]['local_his_long'][:-1].rfind(pattern)
        if len(pc_history[pc_history_index]['local_his']) >= length_local and pattern_idx > 0 and pattern_idx + length_local < len(pc_history[pc_history_index]['local_his_long']):
            if pc_history[pc_history_index]['local_his_long'][pattern_idx + length_local] != taken:
                hot_miss_2 += 1
                if miss_hit == 'H':
                    extra_miss_2 += 1
            else:
                hot_hit_2 += 1
                if miss_hit == 'M':
                    extra_miss_2 += -1
    ####### End of Second Implementation
    ####### Original Implementation:
    # first check if this is in the hot miss addresses
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][pattern] != taken:
    #             hot_miss_2 += 1
    #             pc_history[pc_history_index]['table'][pattern] = taken
    #             if miss_hit == 'H':
    #                 extra_miss_2 += 1
    #         else:
    #             hot_hit_2 += 1
    #             if miss_hit == 'M':
    #                 extra_miss_2 += -1
    ####### End of Original implementation
        # else:
        #     pattern = pc_history[pc_history_index]['local_his']
        #     if pattern in pc_history[pc_history_index]['table']:
        #         if pc_history[pc_history_index]['table'][pattern] != taken:
        #             hot_miss_2 += 1
        #             pc_history[pc_history_index]['table'][pattern] = taken
        #         else:
        #             hot_hit_2 += 1
        else:
            if miss_hit == 'M':
                hot_miss_2 += 1
            else:
                hot_hit_2 += 1
            pc_history[pc_history_index]['table'][pattern] = taken
        if len(pc_history[pc_history_index]['local_his_long']) < length_long:
            pc_history[pc_history_index]['local_his_long'] += taken
        else:
            pc_history[pc_history_index]['local_his_long'] = pc_history[pc_history_index]['local_his_long'][1:] + taken
        if len(pc_history[pc_history_index]['local_his']) < length_local:
            pc_history[pc_history_index]['local_his'] += taken
        else:
            pc_history[pc_history_index]['local_his'] = pc_history[pc_history_index]['local_his'][1:] + taken


# Reload
hot_miss_3 = 0
hot_hit_3 = 0
extra_miss_3 = 0 # More misses due to this implementation, possibly negative
def reload_hot_misses(pc_history_index, br_pc, taken, miss_hit):
    global hot_miss_3
    global hot_hit_3
    global extra_miss_3
    length_local = 100
    if br_pc == pc_history[pc_history_index]['pc']:
        pattern = pc_history[pc_history_index]['local_his']
        pattern_idx = pc_history[pc_history_index]['local_his_long'][:-1].rfind(pattern)
        if len(pc_history[pc_history_index]['local_his']) >= length_local and pattern_idx > 0 and pattern_idx + length_local < len(pc_history[pc_history_index]['local_his_long']):
            if pc_history[pc_history_index]['local_his_long'][pattern_idx + length_local] != taken:
                hot_miss_3 += 1
                if miss_hit == 'H':
                    extra_miss_3 += 1
    # if br_pc == pc_history[pc_history_index]['pc']:
    #     pattern = pc_history[pc_history_index]['local_his']
    #     if pattern in pc_history[pc_history_index]['table']:
    #         if pc_history[pc_history_index]['table'][pattern] != taken:
    #             hot_miss_3 += 1
    #             if miss_hit == 'H':
    #                 extra_miss_3 += 1
    #             pc_history[pc_history_index]['table'][pattern] = taken
            else:
                hot_hit_3 += 1
                if miss_hit == 'M':
                    extra_miss_3 += -1
        else:
            if miss_hit == 'M':
                hot_miss_3 += 1
            else:
                hot_hit_3 += 1
        # if len(pc_history[pc_history_index]['local_his_long']) < length_local:
        #     pc_history[pc_history_index]['local_his_long'] += taken
        # else:
        #     pc_history[pc_history_index]['local_his_long'] = pc_history[pc_history_index]['local_his_long'][1:] + taken
        if len(pc_history[pc_history_index]['local_his']) < length_local:
            pc_history[pc_history_index]['local_his'] += taken
        else:
            pc_history[pc_history_index]['local_his'] = pc_history[pc_history_index]['local_his'][1:] + taken


br_pc = {}

# tmp_pc = "0x7ffff7fda678"
tmp_pc = "0x7ffff7fce505"
tmp_str = ''

# First Time, record hot PC
fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out"
for iteration in range(3):
    if iteration == 2:
        fn = "/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out"
    with open(fn, "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v1.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v10.out", "r") as f_misses:
    # with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out", "r") as f_misses:
        line_cnt = 0
        init_miss = 0
        init_miss_t = 0
        init_miss_b = 0
        total_miss = 0
        use_bimodal = 0
        use_bimodal_miss = 0
        real_num_his_idx = 0
        pc_history_index = 0
        hot_miss_2_prev = 0
        hot_hit_2_prev = 0
        for line in f_misses:
            tokens = line.split()
            if len(tokens) < 4:
                continue
            pc = 0
            if tokens[0] == "ip":
                pc = int(tokens[1], 16)
            else:
                continue
            line_cnt += 1
            # if line_cnt % 10000000 == 0:
            # if line_cnt % 1822781 == 0:
            # if line_cnt % 2738 == 0:
            # if line_cnt % 20000 == 0:
            if iteration == 0:
                if line_cnt % 20000 == 0:
                    # print(line_cnt)
                    preprocess_branch_misses(br_pc, line_cnt)
                    br_pc = {}
            elif iteration > 0:
                for tmp_idx in range(real_num_his[real_num_his_idx]):
                    # print(len(pc_history), pc_history_index + tmp_idx)
                    if pc == pc_history[pc_history_index + tmp_idx]['pc']:
                        if iteration == 1:
                            process_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3])
                        elif iteration == 2:
                            reload_hot_misses(pc_history_index + tmp_idx, pc, tokens[4], tokens[3])
                        break
                if line_cnt % 20000 == 0 and pc_history_index < len(pc_history) - real_num_his[-1]:
                    for tmp_idx in range(real_num_his[real_num_his_idx]):
                        print(hex(pc_history[pc_history_index + tmp_idx]['pc']), hot_miss_2 - hot_miss_2_prev, hot_hit_2 - hot_hit_2_prev)
                    hot_miss_2_prev = hot_miss_2
                    hot_hit_2_prev = hot_hit_2
                    pc_history_index += real_num_his[real_num_his_idx]
                    real_num_his_idx += 1
            if line_cnt % 1820000 == 0:
            # if line_cnt % 1822781 == 0:
                break
            # update num or init entry
            if tokens[2] == 'B':
                use_bimodal += 1
                if tokens[3] == 'M':
                    use_bimodal_miss += 1 
            if tokens[3] == 'M':
                total_miss += 1
            if pc in br_pc:
                br_pc[pc]["num"] += 1
            else:
                br_pc[pc] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0, "h_t": 0, "m_t": 0, "h_b": 0, "m_b": 0}
                if tokens[3] == 'M':
                    init_miss += 1
                    if tokens[2] == 'B':
                        init_miss_b += 1
                    else:
                        init_miss_t += 1
            # update miss/hit
            if tokens[3] == 'M':
                br_pc[pc]["miss"] += 1
                if tokens[2] == 'B':
                    br_pc[pc]["m_b"] += 1
                else:
                    br_pc[pc]["m_t"] += 1
            else:
                br_pc[pc]["hit"] += 1
                if tokens[2] == 'B':
                    br_pc[pc]["h_b"] += 1
                else:
                    br_pc[pc]["h_t"] += 1
            # update miss/hit by Tage or Bimodal
            if tokens[4] == '0':
                br_pc[pc]["NT"] += 1
            else:
                br_pc[pc]["T"] += 1
            if pc == int(tmp_pc, 16):
                tmp_str += tokens[4]




# ordered = OrderedDict(sorted(br_pc.items(), key=lambda i: i[1]["num"]))

print("Total Miss", total_miss, "Hot Miss", hot_miss)
print("Use bimodal:", use_bimodal, " Misses:", use_bimodal_miss)
print("Init Miss", init_miss, "Tage: ", init_miss_t, "Bimodal: ", init_miss_b)

# only_1_cnt = 0
# total_cnt = 0
# for k,v in ordered:
#     total_cnt += 1
#     if v['num'] == 1:
#         only_1_cnt += 1
#     if total_cnt < 20:
#         print(hex(k), v)
# print("Total branch PCs: ", total_cnt, "Branch PC only occurs once: ", only_1_cnt)

# print(tmp_pc, tmp_str)
# 
# table = {}
# local_miss = 0
# len_localtable = 10
# for i in range(len(tmp_str)):
#     if i < len_localtable + 1:
#         continue
#     table[tmp_str[i-1-len_localtable:i-1]] = tmp_str[i]
# 
# for i in range(len(tmp_str)):
#     if i < len_localtable + 1:
#         continue
#     if tmp_str[i] != table[tmp_str[i-1-len_localtable:i-1]]:
#         local_miss += 1 
# print(local_miss)

print("Hot Misses: ", hot_miss, "Hit: ", hot_hit)
print("Second Time Hot Misses: ", hot_miss_2, "Hit: ", hot_hit_2, "Extra Miss:", extra_miss_2)
print("Third Time Hot Misses: ", hot_miss_3, "Hit: ", hot_hit_3, "Extra Miss:", extra_miss_3)
