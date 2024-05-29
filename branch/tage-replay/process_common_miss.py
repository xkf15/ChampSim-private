

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
    consecutive_unmatched = 0
    
    
    pc_trace_common = open(f_common_o, "w")
    
    with open(f_trace2_i, "r") as f_miss_trace:
        for line in f_miss_trace:
            tokens = line.split()
            if len(tokens) < 3:
                continue
            if_matched = False
            # for i in range(len(trace1)):
            # for i in range(max(0, idx_miss - 1000), min(len(trace1), idx_miss + 3000)):
            # for i in range(0, min(len(trace1), idx_miss + 100000)):
            #     if tokens[0] == trace1[i][0] and tokens[1] == trace1[i][1]:
            i = (tokens[0], tokens[1])
            if i in trace1:
                pc_trace_common.write(line)
                matched += 1
                if_matched = True
                if tokens[2] == trace1[i]:
                    correct += 1
                # if if_matched:
                #     consecutive_unmatched = 0
                #     if i - idx_miss > 2000:
                #         idx_miss += 1
                # if idx_miss < i:
                #     idx_miss += 1
                # if idx_miss < i - 1000:
                #     idx_miss += 1
                # if idx_miss < i - 2000:
                #     idx_miss += 2
            # else:
            #     consecutive_unmatched += 1
            # if consecutive_unmatched > 50: #and idx_miss < line_cnt + 3000:
            #     idx_miss += 10
            #     consecutive_unmatched = 0
            # if consecutive_unmatched > 100 and idx_miss < line_cnt + 1000:
            #     idx_miss += 2
            line_cnt += 1
            if line_cnt % 1000 == 0:
                print("Line count:", line_cnt,"Matched:", matched, "Correct:", correct, "idx:", idx_miss)
    
    # pc_trace_common.close()
    print("Miss num:", line_cnt, "Matched:", matched, "Correct:", correct)
        
find_common_miss("pc_trace1.txt", "pc_trace2.txt", "pc_trace_common_tmp.txt")
