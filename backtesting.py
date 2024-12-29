import pandas as pd

def calculateSharpeRatio(returns, risk_free_rate = 0):
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()

def calculateMaxDrawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown

# Long only
# to do: add also a short strategy
def runBacktest(data, stop_loss, take_profit, position_size):
    long_position_open = False
    entry_price = 0
    returns = []
    
    for i in range(1, len(data)):
        if data['hasTransition'].iloc[i] == 1.0:
            if data['crossover_state'].iloc[i] == 1 and data['crossover_state'].iloc[i-1] == 0:
                long_position_open = True
                entry_price = data['Value'].iloc[i]
            
            if long_position_open:
                current_price = data['Value'].iloc[i]
                current_return = (current_price - entry_price) / entry_price
                
                if current_return <= -stop_loss or current_return >= take_profit:
                    returns.append(current_return * position_size)
                    long_position_open = False
                    continue

            if data['crossover_state'].iloc[i] == 0 and data['crossover_state'].iloc[i-1] == 1:
                if long_position_open:
                    exit_price = data['Value'].iloc[i]
                    trade_return = (exit_price - entry_price) / entry_price
                    returns.append(trade_return * position_size)
                    long_position_open = False
    
    returns_series = pd.Series(returns)
    total_return = (1 + returns_series).prod() - 1
    sharpe_ratio = calculateSharpeRatio(returns_series)
    max_drawdown = calculateMaxDrawdown(returns_series)

    return total_return * 100, sharpe_ratio,  max_drawdown
