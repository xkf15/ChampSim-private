from collections import OrderedDict


br_pc = {}

tmp_pc = "0x7ffff7fda678"
tmp_str = ''

# with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v0.out", "r") as f_misses:
with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_ld10000000_v1.out", "r") as f_misses:
# with open("/scratch/gpfs/kaifengx/useronly_ld_noaddrrandom_detailed_misses_20230918_imageprocessing_2_ld10000000_v0.out", "r") as f_misses:
    line_cnt = 0
    init_miss = 0
    total_miss = 0
    use_bimodal = 0
    use_bimodal_miss = 0
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
        if line_cnt % 20000 == 0:
            print(line_cnt)
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
            br_pc[pc] = {"num": 1, "miss": 0, "hit": 0, "T": 0, "NT": 0}
            if tokens[3] == 'M':
                init_miss += 1
        # update miss/hit
        if tokens[3] == 'M':
            br_pc[pc]["miss"] += 1
        else:
            br_pc[pc]["hit"] += 1
        if tokens[4] == '0':
            br_pc[pc]["NT"] += 1
        else:
            br_pc[pc]["T"] += 1
        if pc == int(tmp_pc, 16):
            tmp_str += tokens[4]




# ordered = OrderedDict(sorted(br_pc.items(), key=lambda i: i[1]["num"]))
ordered = sorted(br_pc.items(), key=lambda i: i[1]["miss"], reverse=True)

only_1_cnt = 0
total_cnt = 0
for k,v in ordered:
    total_cnt += 1
    if v['num'] == 1:
        only_1_cnt += 1
    if total_cnt < 20:
        print(hex(k), v)

print("Total Miss", total_miss)
print("Use bimodal:", use_bimodal, " Misses:", use_bimodal_miss)
print("Init Miss", init_miss)
print("Total branch PCs: ", total_cnt, "Branch PC only occurs once: ", only_1_cnt)

print(tmp_pc, tmp_str)

table = {}
local_miss = 0
len_localtable = 10
for i in range(len(tmp_str)):
    if i < len_localtable + 1:
        continue
    table[tmp_str[i-1-len_localtable:i-1]] = tmp_str[i]

for i in range(len(tmp_str)):
    if i < len_localtable + 1:
        continue
    if tmp_str[i] != table[tmp_str[i-1-len_localtable:i-1]]:
        local_miss += 1 
print(local_miss)
