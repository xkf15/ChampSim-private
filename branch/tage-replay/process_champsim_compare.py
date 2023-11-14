
tmp_miss_list = []
total_miss_1 = 0
with open("/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_2_v0_noprefetch.out", "r") as f_1:
    for line in f_1:
        if "Insn" not in line or "Finish" in line:
            continue
        tokens = line.split()
        tmp_miss = int(tokens[5]) - total_miss_1
        tmp_miss_list.append(tmp_miss)
        total_miss_1 = int(tokens[5])

total_miss_2 = 0
total_reduce = 0
max_reduce = 0
max_reduce_insn = 0
with open("/scratch/gpfs/kaifengx/useronly_tage-sc-l_detailed_misses_20230918_imageprocessing_2_v0_prefetch_insert.out", "r") as f_2:
    tmp_idx = 0
    for line in f_2:
        if "Insn" not in line or "Finish" in line:
            continue
        tokens = line.split()
        tmp_miss = int(tokens[5]) - total_miss_2
        delta_miss = tmp_miss - tmp_miss_list[tmp_idx]
        total_reduce += delta_miss 
        if total_reduce < max_reduce:
            max_reduce = total_reduce
            max_reduce_insn = int(tokens[1])
            print(max_reduce)
        total_miss_2 = int(tokens[5])
        tmp_idx += 1
        print(line[:-1], "Extra miss ", delta_miss)

print("Original Total miss:", total_miss_1, "Current:", total_miss_2)
print("Max reduce insn:", max_reduce_insn, "Reduce:", max_reduce)
