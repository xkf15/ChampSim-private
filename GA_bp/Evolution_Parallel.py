import random
import datetime
import os
from deap import base, creator, tools

# TAGE parameters
TAGE_BIMODAL_TABLE_SIZE = 16384
TAGE_NUM_COMPONENTS = 12
TAGE_MAX_INDEX_BITS = 12
TAGE_ENTRY_LENGTH = 3 + 16 + 2

def store(fname, bitstream):
    print("Start Writing BP States\n")
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
    print("Finish Writing BP States!\n")
    return

def load(bitstream):
    return

# DEAP Parameters
POPULATION_SIZE = 20
BITSTREAM_LENGTH = TAGE_BIMODAL_TABLE_SIZE * 8 + TAGE_NUM_COMPONENTS * (1 << TAGE_MAX_INDEX_BITS) * TAGE_ENTRY_LENGTH
MUTATION_RATE = 0.01
NUM_GENERATIONS = 50

# Manually defined fitness function (you should replace this with your own function)
def eval(bitstream):
    # Example fitness function: Count the number of '1's in the bitstream
    return sum(bitstream),

# Initialize the DEAP framework
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=BITSTREAM_LENGTH)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", eval)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=MUTATION_RATE)
toolbox.register("select", tools.selTournament, tournsize=3)

def Get_Current_Readable_Time():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    population = toolbox.population(n=POPULATION_SIZE)
    
    wk_dir = "test-" + Get_Current_Readable_Time()
    os.mkdir(wk_dir)
    os.mkdir(wk_dir + "/init")
    for i in range(POPULATION_SIZE):
        store(f"./{wk_dir}/init/test_init_{i}.txt", population[i])
    return
 
    for generation in range(NUM_GENERATIONS):
        # Evaluate the fitness of each individual in the population
        fitness_scores = [toolbox.evaluate(individual)[0] for individual in population]

        # Find the index of the individual with the highest fitness score
        best_index = max(range(POPULATION_SIZE), key=lambda i: fitness_scores[i])

        # Print the best bitstream and its fitness score for this generation
        print(f"Generation {generation + 1}: Best Bitstream = {population[best_index]}, Fitness = {fitness_scores[best_index]}")

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
