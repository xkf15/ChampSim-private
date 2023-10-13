def print_bp(input_fn):
    count = 0
    with open(input_fn) as fp:
        output_fn = open(input_fn + "_print", "w")
        while True:
            line = fp.readline()
            if not line:
                break
            tokens = line.split()
            if count == 0:
                for value in tokens:
                    # print(value)
                    output_fn.write(value + "\n")
                count += 1
            else:
                str_tmp = ""
                i_tmp = 0
                for value in tokens:
                    str_tmp += value + " "
                    i_tmp += 1
                    if i_tmp > 2:
                        # print(str_tmp)
                        output_fn.write(str_tmp + "\n")
                        str_tmp = ""
                        i_tmp = 0
        output_fn.close()


# print_bp("states_useronly_noaddrrandom/insn10000000-v0")
# print_bp("states_useronly_noaddrrandom/insn10000000-v1")
# print_bp("states_useronly_noaddrrandom/insn10000000-v2")
# print_bp("states_useronly_noaddrrandom/insn10000000-v5")
# print_bp("states_useronly_noaddrrandom/insn10000000-v10")
# print_bp("states_useronly_noaddrrandom/insn10000000-v20")
# 
# print_bp("states_useronly_noaddrrandom/insn20000000-v0")
# print_bp("states_useronly_noaddrrandom/insn20000000-v1")
# print_bp("states_useronly_noaddrrandom/insn20000000-v2")
# print_bp("states_useronly_noaddrrandom/insn20000000-v5")
# print_bp("states_useronly_noaddrrandom/insn20000000-v10")
# print_bp("states_useronly_noaddrrandom/insn20000000-v20")

def diff_bp(bp1, bp2):
    new_entry = 0
    diff_tag = 0
    same_tag_sm = 0
    same_tag_wk = 0
    same_tag_st = 0
    line_cnt = 0
    with open(bp1) as fp1:
        with open(bp2) as fp2:
            while True:
                line1 = fp1.readline()
                line2 = fp2.readline()
                if not line1:
                    break
                if not line2:
                    break
                tokens1 = line1.split()
                tokens2 = line2.split()
                if len(tokens1) < 3:
                    continue
                line_cnt += 1
                # print(line1)
                # break
                if int(tokens1[1], 16) == 0 and int(tokens1[1], 16) != int(tokens2[1], 16):
                    new_entry += 1
                elif int(tokens1[1], 16) != int(tokens2[1], 16):
                    diff_tag += 1
                else:
                    if int(tokens1[0]) == int(tokens2[0]):
                        same_tag_sm += 1
                    elif abs(int(tokens1[0]) - 4) > abs(int(tokens2[0]) - 4):
                        same_tag_wk += 1
                    else:
                        same_tag_st += 1
    print(100.0 * line_cnt/line_cnt    , line_cnt, "Line_Count")
    print(100.0 * new_entry/line_cnt   , new_entry, "New_Entry")
    print(100.0 * diff_tag/line_cnt    , diff_tag, "Diff_Tag")
    print(100.0 * same_tag_sm/line_cnt , same_tag_sm, "Same_Tag_Same")
    print(100.0 * same_tag_wk/line_cnt , same_tag_wk, "Same_Tag_Weak")
    print(100.0 * same_tag_st/line_cnt , same_tag_st, "Same_Tag_Strong")

# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn10000000-v1_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn10000000-v2_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn10000000-v5_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v2_print", "states_useronly_noaddrrandom/insn10000000-v5_print")

# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v0_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v1_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v2_print")
# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v5_print")

# diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v1_print")
# diff_bp("states_useronly_noaddrrandom/insn20000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v1_print")
# diff_bp("states_useronly_noaddrrandom/insn20000000-v1_print", "states_useronly_noaddrrandom/insn20000000-v2_print")
# diff_bp("states_useronly_noaddrrandom/insn20000000-v2_print", "states_useronly_noaddrrandom/insn20000000-v5_print")

diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v1_print")
diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v2_print")
diff_bp("states_useronly_noaddrrandom/insn10000000-v0_print", "states_useronly_noaddrrandom/insn20000000-v5_print")
