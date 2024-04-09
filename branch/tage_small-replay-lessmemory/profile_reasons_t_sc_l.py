
fn = "/scratch/gpfs/kaifengx/function_bench_results/nokvm-2023-11-24_-_20-33-00-chameleon_short.trace_detailed_misses_reasons_his_tagesmall_base.out"
t = 0
sc = 0
l = 0
with open(fn, "r") as f_read:
    for line in f_read:
        tokens = line.split()
        if "Heartbeat CPU" in line:
            print("Insn: ", tokens[4], "Miss Reasons: T", t, "SC", sc, "L", l)
            continue
        if len(tokens) < 8:
            continue
        if tokens[0] != 'ip':
            continue
        if tokens[3] == 'M':
            if tokens[2] == 'T':
                t += 1
            elif tokens[2] == 'S':
                sc += 1
            elif tokens[2] == 'L':
                l += 1
        
