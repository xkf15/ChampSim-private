import random
import time
import datetime
import os
from deap import base, creator, tools

# TAGE parameters
TAGE_BIMODAL_TABLE_SIZE = 16384
TAGE_NUM_COMPONENTS = 12
TAGE_MAX_INDEX_BITS = 12
TAGE_ENTRY_LENGTH = 3 + 16 + 2
fpath = ""

def store(fname, bitstream):
    # print("Start Writing BP States\n")
    bp_states = open(fname, "w")
    for i in range(TAGE_BIMODAL_TABLE_SIZE):
        bin_str = ''.join(str(bit) for bit in bitstream[i*8:i*8+8])
        integer_value = int(bin_str, 2)
        bp_states.write(format(integer_value, '02x') + " ")
    bp_states.write("\n")
    tage_base_idx = TAGE_BIMODAL_TABLE_SIZE * 8
    for i in range(TAGE_NUM_COMPONENTS):
        for j in range(1 << TAGE_MAX_INDEX_BITS):
            tmp_idx = tage_base_idx + (i * (1 << TAGE_MAX_INDEX_BITS) + j) * TAGE_ENTRY_LENGTH
            bin_str = ''.join(str(bit) for bit in bitstream[tmp_idx:tmp_idx+3])
            ctr = int(bin_str, 2)
            bin_str = ''.join(str(bit) for bit in bitstream[tmp_idx+3:tmp_idx+19])
            tag = int(bin_str, 2)
            bin_str = ''.join(str(bit) for bit in bitstream[tmp_idx+19:tmp_idx+21])
            useful = int(bin_str, 2)
            bp_states.write(format(ctr, '02x') + " " + format(tag, '04x') + " " + format(useful, '02x') + " ")
        bp_states.write("\n")
    bp_states.close()
    # print("Finish Writing BP States!")
    return

def load(bitstream):
    return

# DEAP Parameters
POPULATION_SIZE = 100
BITSTREAM_LENGTH = TAGE_BIMODAL_TABLE_SIZE * 8 + TAGE_NUM_COMPONENTS * (1 << TAGE_MAX_INDEX_BITS) * TAGE_ENTRY_LENGTH
MUTATION_RATE = 0.01
NUM_GENERATIONS = 50

# Manually defined fitness function
# Check output files from ChampSim
def eval(bitstream, gen, idx, fpath):
    # Check if output file exists
    while not os.path.isfile(fpath):
        print(f"{fpath} not found yet, Wait for 10 mins")
        time.sleep(600)
    fit = 0
    while True:
        out_file = open(fpath, "r")
        while True:
            line = out_file.readline()
            if not line:
                break
            # results
            if "FinishBP" in line:
                tokens = line.split()
                insn = int(tokens[2])
                insn_b = int(tokens[4])
                bp_miss = int(tokens[6])
                fit = 1000.0 - 1000.0 * bp_miss / insn
                break
        out_file.close()
        # Check if fit gets updated
        if fit > 0.1:
            break
        else:
            # Check every 10 mins for the file
            # print("Recheck the file for results")
            time.sleep(600)
    return fit,

# Initialize the DEAP framework
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=BITSTREAM_LENGTH)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", eval, gen=0, idx=0, fpath="")
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=MUTATION_RATE)
toolbox.register("select", tools.selTournament, tournsize=3)

def Get_Current_Readable_Time():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    # print(eval([0], 0, 0, "test-20230807_140354/Gen_0/pop_0.txt.out"))
    # return
    population = toolbox.population(n=POPULATION_SIZE)
    # have all 0s in the initial states
    for i in range(BITSTREAM_LENGTH):
        population[0][i] = 0
    
    wk_dir = "test-" + Get_Current_Readable_Time()
    os.mkdir(wk_dir)
 
    for generation in range(NUM_GENERATIONS):
        # Submit all jobs
        os.mkdir(f"{wk_dir}/Gen_{generation}")
        for i in range(POPULATION_SIZE):
            fpath = f"./{wk_dir}/Gen_{generation}/pop_{i}.txt"
            store(fpath, population[i])
            os.system(f"sbatch champsim-slurm-qemutrace.sh {fpath}")

        # Evaluate the fitness of each individual in the population
        fitness_scores = []
        for idx, ind in enumerate(population):
            # print(ind.fitness.values)
            ind.fitness.values = toolbox.evaluate(ind, gen=generation, idx=idx, fpath=f"./{wk_dir}/Gen_{generation}/pop_{idx}.txt.out")
            fitness_scores.append(ind.fitness.values)
        # Find the index of the individual with the highest fitness score
        best_index = max(range(POPULATION_SIZE), key=lambda i: fitness_scores[i])
        # # Print the best bitstream and its fitness score for this generation
        os.system(f"echo 'Generation {generation}: Best Bitstream = # {best_index} MPKI = {1000 - fitness_scores[best_index][0]}'")

        # Create a new generation using tournament selection
        offspring = toolbox.select(population, len(population))
        offspring = list(offspring)

        # Clone the selected individuals
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Apply crossover and mutation to the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTATION_RATE:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Replace the old population with the new generation
        population[:] = offspring

if __name__ == "__main__":
    main()
