import random
import constant
import input
import indicators
import backtesting
import pandas as pd

pd.set_option('mode.chained_assignment', None)

# Population generation
#
# [short_ma, long_ma, atr, take_profit, stop_loss, position_size]
#
def generatePopulation(population = 100, already_selected = 0):
    created_population = []
    for _ in range(population - already_selected):
        short_ma = random.randint(constant.SHORT_MA_RANGE['lower'], constant.SHORT_MA_RANGE['upper'])
        long_ma = random.randint(constant.LONG_MA_RANGE['lower'], constant.LONG_MA_RANGE['upper'])
        atr = round(random.randint(
            int(constant.ATR_RANGE['lower'] * 10),
            int(constant.ATR_RANGE['upper'] * 10)) * 0.1, 1)

        take_profit = round(random.randint(
            int(constant.TAKE_PROFIT_RANGE['lower'] * 10), 
            int(constant.TAKE_PROFIT_RANGE['upper'] * 10)) * 0.1, 1)

        stop_loss = round(random.randint(
            int(constant.STOP_LOSS_RANGE['lower'] * 10),
            int(constant.STOP_LOSS_RANGE['upper'] * 10)) * 0.1, 1)

        position_size = round(random.randint(
            int(constant.POSITION_SIZE_RANGE['lower'] * 1000),
            int(constant.POSITION_SIZE_RANGE['upper'] * 1000)) * 0.001, 3)
        
        individual = {
            'short_ma': short_ma,
            'long_ma': long_ma,
            'atr': atr,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'position_size': position_size
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
        short_ma_period = individual['short_ma']
        long_ma_period = individual['long_ma']
        atr = individual['atr']
        take_profit = individual['take_profit']
        stop_loss = individual['stop_loss']
        position_size = individual['position_size']
        
        data = input.spx_1990

        data['short_ma'] = indicators.calculate_moving_average(data['Value'], short_ma_period)
        data['long_ma'] = indicators.calculate_moving_average(data['Value'], long_ma_period)
        data['atr'] = indicators.calculateAverageTrueRange(data['Value'])
        
        data['crossover_state'] = data.apply(
            lambda row: 0 if row['short_ma'] > row['long_ma'] and row['atr'] > atr else 1, axis=1
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
# Pick the top individuals 
# Elitism
# Wheel of Fortune
#
def pickIndividuals(individuals):
    top_individuals = individuals[0:constant.TOP_PICK]
    top_individuals = [individual['individual'] for individual in top_individuals]
    
    remaining_individuals = individuals[constant.TOP_PICK:constant.WHEEL_OF_FORTUNE]
    selected_individuals_by_wheel_of_fortune = wheelOfFortuneIndividuals(remaining_individuals)
    
    random_individuals = generatePopulation(constant.POPULATION_SIZE, constant.WHEEL_OF_FORTUNE)
    
    new_generation = top_individuals + selected_individuals_by_wheel_of_fortune + random_individuals


population = generatePopulation(constant.POPULATION_SIZE)
individuals = runGeneration(population)

# for _ in range(20):
#     individuals = runGeneration(population)
#     top_individuals = individuals[0:constant.TOP_PICK]
#     top_individuals = [individual[0] for individual in top_individuals]

#     population = top_individuals + generatePopulation(constant.POPULATION_SIZE, constant.TOP_PICK)

for individual in individuals:
    print(individual)