import matplotlib.pyplot as plt

corr_list = []
with open("miss_common_progressive_corr.csv", "r") as fin:
    for line in fin:
        tokens = line.split(',')
        for token in tokens:
            corr_list.append(float(token))

plt.plot(corr_list)
plt.show()



