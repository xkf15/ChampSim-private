
f_trace_o = "pc_his_common_miss_trace.txt"
# pc_his_common = open(f_trace_o, "w")
line_cnt = 0
with open(f_trace_o, "r") as f_test:
    for line in f_test:
        tokens = line.split()
        line_cnt += 1
        if line_cnt % 10000 == 0:
            print("Line_cnt: ", line_cnt, "Insn_cnt", int(tokens[3]))
        

