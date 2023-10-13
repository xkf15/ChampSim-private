
miss_10M = [[], []]
mpki_10M = [[], []]
miss_1B = [[], []]
mpki_1B = [[], []]

def parse_output(fname, v):
    with open(fname, "r") as spec_output:
        for line in spec_output:
            tokens = line.split()
            if len(tokens) < 6:
                continue
            if "Insn" in tokens[0]:
                if int(tokens[1]) == 10000001:
                    miss_10M[v].append(int(tokens[5])) 
                    mpki_10M[v].append(int(tokens[5]) / 10000.0) 
            if "FinishBP!" in tokens[0]:
                if int(tokens[2]) == 1000000000:
                    miss_1B[v].append(int(tokens[6]))
                    mpki_1B[v].append(int(tokens[6]) / 1000000.0) 


for bench in [600, 602, 605, 620, 625, 631, 641, 648, 657, 998]:
    fname = "states_useronly_noaddrrandom_spec_{num}/useronly_ld_noaddrrandom_spec_{num}_{v}.out".format(num=bench, v=0)
    parse_output(fname, 0)
    fname = "states_useronly_noaddrrandom_spec_{num}/useronly_ld_noaddrrandom_spec_{num}_{v}.out".format(num=bench, v=10)
    parse_output(fname, 1)

print("MPKI at 10M insn")
print(mpki_10M[0])
print(mpki_10M[1])
print("MPKI at 1B insn")
print(mpki_1B[0])
print(mpki_1B[1])
                
