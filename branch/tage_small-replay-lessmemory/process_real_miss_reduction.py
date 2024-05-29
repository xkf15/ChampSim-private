
fname = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-32-28-chameleon_short.trace_detailed_misses_reasons_his_tagesmall_base_ld.out"
num_prefetch = 0
num_prefetch_m = 0
num_misses = 0
line_cnt = 0
GI_set = {' '}
with open(fname, "r") as f_trace_new_bench:
    for line in f_trace_new_bench:
        tokens = line.split()
        line_cnt += 1
        if "Heart" in line:
            print("Insn:", tokens[4], "Total Misses:", num_misses, "P:", num_prefetch, "PM:", num_prefetch_m, "GI num:", len(GI_set))
            continue
        if len(tokens) < 8:
            continue
        elif tokens[0] != 'ip':
            continue
        if tokens[2] == 'P':
            # print(tokens[1], line_cnt)
            # exit()
            num_prefetch += 1
            if tokens[3] == 'M':
                num_prefetch_m += 1
            # See how many GI it occupies
            if tokens[10] not in GI_set:
                GI_set.add(tokens[10])
        if tokens[3] == 'M':
            num_misses += 1
            


print(fname)
print("Total Misses:", num_misses, "P:", num_prefetch, "PM:", num_prefetch_m)


