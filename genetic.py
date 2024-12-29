import random
import constant
import input
import indicators
import backtesting
import pandas as pd

pd.set_option('mode.chained_assignment', None)

def generateShortMA():
    return random.randint(constant.SHORT_MA_RANGE[constant.LOWER], constant.SHORT_MA_RANGE[constant.UPPER])

def generateLongMA():
    return random.randint(constant.LONG_MA_RANGE[constant.LOWER], constant.LONG_MA_RANGE[constant.UPPER])

def generateATR():
    return round(random.randint(
            int(constant.ATR_RANGE[constant.LOWER] * 10),
            int(constant.ATR_RANGE[constant.UPPER] * 10)) * 0.1, 1)

def generateTakeProfit():
    return round(random.randint(
            int(constant.TAKE_PROFIT_RANGE[constant.LOWER] * 10), 
            int(constant.TAKE_PROFIT_RANGE[constant.UPPER] * 10)) * 0.1, 1)

def generateStopLoss():
    return round(random.randint(
            int(constant.STOP_LOSS_RANGE[constant.LOWER] * 10),
            int(constant.STOP_LOSS_RANGE[constant.UPPER] * 10)) * 0.1, 1)

def generatePositionSize():
    return round(random.randint(
            int(constant.POSITION_SIZE_RANGE[constant.LOWER] * 1000),
            int(constant.POSITION_SIZE_RANGE[constant.UPPER] * 1000)) * 0.001, 3)

# Population generation
#
# [short_ma, long_ma, atr, take_profit, stop_loss, position_size]
#
def generatePopulation(population = 100):
    created_population = []
    for _ in range(population):
        short_ma = generateShortMA()
        long_ma = generateLongMA()
        atr = generateATR()
        take_profit = generateTakeProfit()
        stop_loss = generateStopLoss()
        position_size = generatePositionSize()
        
        individual = {
            constant.SHORT_MA: short_ma,
            constant.LONG_MA: long_ma,
            constant.ATR: atr,
            constant.TAKE_PROFIT: take_profit,
            constant.STOP_LOSS: stop_loss,
            constant.POSITION_SIZE: position_size
        }
        
        created_population.append(individual)
    
    return created_population

def fitnessScore(total_return, sharpe_ratio, max_drawdown):
    return constant.TOTAL_RETURN_COEFICIENT * total_return + constant.SHARP_RATIO_COEFICIENT * sharpe_ratio - constant.MAX_DRAWDOWN_COEFICIENT * max_drawdown

#
# Get for each individual the score 
#
def runGeneration(population):
    individuals_performance = []
    
    for individual in population:
        short_ma_period = individual[constant.SHORT_MA]
        long_ma_period = individual[constant.LONG_MA]
        atr = individual[constant.ATR]
        take_profit = individual[constant.TAKE_PROFIT]
        stop_loss = individual[constant.STOP_LOSS]
        position_size = individual[constant.POSITION_SIZE]
        
        data = input.spx_1990

        data[constant.SHORT_MA] = indicators.calculate_moving_average(data['Value'], short_ma_period)
        data[constant.LONG_MA] = indicators.calculate_moving_average(data['Value'], long_ma_period)
        data[constant.ATR] = indicators.calculateAverageTrueRange(data['Value'])
        
        data['crossover_state'] = data.apply(
            lambda row: 0 if row[constant.SHORT_MA] > row[constant.LONG_MA] and row[constant.ATR] > atr else 1, axis=1
        )
        
        data['hasTransition'] = data['crossover_state'].diff().abs()
        total_return, sharpe_ratio, max_drawdown = backtesting.runBacktest(data, take_profit, stop_loss, position_size)
        
        score = fitnessScore(total_return, sharpe_ratio, max_drawdown)
        
        individuals_performance.append({
            'individual': individual,
            'score': score,
            'metrics': [total_return, sharpe_ratio, max_drawdown]
        })
    
    sorted_individuals = sorted(individuals_performance, key=lambda x: x['score'], reverse=True)
    return sorted_individuals


def wheelOfFortuneIndividuals(individuals):
    total_fitness = sum(individual['score'] for individual in individuals)
    selection_probabilities = [individual['score'] / total_fitness for individual in individuals]
    
    selected_individuals = []
    for _ in range(constant.WHEEL_OF_FORTUNE):
        selected_individual = random.choices(individuals, weights=selection_probabilities, k=1)[0]
        selected_individuals.append(selected_individual['individual'])
    
    return selected_individuals

#
# Apply uniform mutations to genes of individuals
#
def mutation(individuals):
    mutated_individuals = []
    
    for individual in individuals:
        mutated_individual = individual.copy()

        for gene, _ in mutated_individual.items():
            if random.random() < constant.MUTATION_PROBABILITY:            
                if gene == constant.SHORT_MA:
                    mutated_individual[gene] = generateShortMA()
                elif gene == constant.LONG_MA:
                    mutated_individual[gene] = generateLongMA()
                elif gene == constant.ATR:
                    mutated_individual[gene] = generateATR()
                elif gene == constant.TAKE_PROFIT:
                    mutated_individual[gene] = generateTakeProfit()
                elif gene == constant.STOP_LOSS:
                    mutated_individual[gene] = generateStopLoss()
                elif gene == constant.POSITION_SIZE:
                    mutated_individual[gene] = generatePositionSize()

        mutated_individuals.append(mutated_individual)
    
    return mutated_individuals

#
# [short_ma, long_ma, atr, take_profit, stop_loss, position_size]
#
# Groups
# 1 - short_ma, long_ma
# 2 - atr
# 3 - take_profit, stop_loss
# 4 - position_size
def crossover(individuals):
    random.shuffle(individuals)
    new_population = []
    
    for index in range(0, len(individuals), 2):
        parent1 = individuals[index]
        parent2 = individuals[index + 1]
        
        offspring1 = parent1.copy()
        offspring2 = parent2.copy()
        
        for _, genes in constant.GROUPS.items():
            if random.random() < constant.CROSSOVER_RATE:
                for gene in genes:
                    offspring1[gene], offspring2[gene] = offspring2[gene], offspring1[gene]
        
        new_population.append(offspring1)
        new_population.append(offspring2)
        
    return new_population

# 
# Pick the to individuals 
# Elitism
# Wheel of Fortune
#
def pickIndividuals(individuals):
    top_individuals = individuals[0:constant.TOP_PICK]
    top_individuals = [individual['individual'] for individual in top_individuals]
    
    remaining_individuals = individuals[constant.TOP_PICK:-constant.RANDOM_INDIVIDUALS]
    selected_individuals_by_wheel_of_fortune = wheelOfFortuneIndividuals(remaining_individuals)
    
    random_individuals = generatePopulation(constant.RANDOM_INDIVIDUALS)
    
    mutated_generation = top_individuals + selected_individuals_by_wheel_of_fortune + random_individuals
    combined_generation = crossover(mutated_generation)
    new_generation = mutation(combined_generation)
    
    return new_generation

population = generatePopulation(constant.POPULATION_SIZE)
individuals = runGeneration(population)
new_generation = pickIndividuals(individuals)

# for _ in range(20):
#     individuals = runGeneration(population)
#     top_individuals = individuals[0:constant.TOP_PICK]
#     top_individuals = [individual[0] for individual in top_individuals]

#     population = top_individuals + generatePopulation(constant.POPULATION_SIZE, constant.TOP_PICK)

print(len(new_generation))
for individual in new_generation:
    print(individual)