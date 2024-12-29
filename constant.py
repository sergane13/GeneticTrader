SHORT_MA = 'short_ma'
LONG_MA = 'long_ma'
ATR = 'atr'
TAKE_PROFIT = 'take_profit'
STOP_LOSS = 'stop_loss'
POSITION_SIZE = 'position_size'

LOWER = 'lower'
UPPER = 'upper'

GENE_RANGES = {
    SHORT_MA: {
        LOWER: 10,
        UPPER: 50
    },
    LONG_MA: {
        LOWER: 100,
        UPPER: 200,
    },
    ATR: {
        LOWER: 0,
        UPPER: 5,
    },
    # Coeficient from entry price
    TAKE_PROFIT: {
        LOWER: 0.5,
        UPPER: 20
    },
    # Coeficient from entry price
    STOP_LOSS: {
        LOWER: 0.1,
        UPPER: 5
    }, 
    # Position size in %
    POSITION_SIZE: {
        LOWER: 0.001, # 0.1%
        UPPER: 1 # 0%  
    }
}

SHORT_MA_RANGE = {
    LOWER: 10,
    UPPER: 50
}

LONG_MA_RANGE = {
    LOWER: 100,
    UPPER: 200
}

ATR_RANGE = {
    LOWER: 0,
    UPPER: 5
}

# Coeficient from entry price
TAKE_PROFIT_RANGE = {
    LOWER: 0.5,
    UPPER: 20
}

# Coeficient from entry price
STOP_LOSS_RANGE = {
    LOWER: 0.1,
    UPPER: 5
}

# Position size in %
POSITION_SIZE_RANGE = {
    LOWER: 0.001, # 0.1%
    UPPER: 0.5    # 50%
}

POPULATION_SIZE = 100

TOP_PICK = 10
WHEEL_OF_FORTUNE = 80
RANDOM_INDIVIDUALS = 10

MUTATION_PROBABILITY = 0.1
CROSSOVER_RATE = 0.05

TOTAL_RETURN_COEFICIENT = 0.5
SHARP_RATIO_COEFICIENT = 0.3
MAX_DRAWDOWN_COEFICIENT = 0.2

GROUPS = {
    1: [SHORT_MA, LONG_MA],
    2: [ATR],
    3: [TAKE_PROFIT, STOP_LOSS],
    4: [POSITION_SIZE]
}
