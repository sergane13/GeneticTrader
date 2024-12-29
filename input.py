from pandas import read_csv
import numpy as np

spx = './data/S&P500.csv'
spx = read_csv(spx)
spx.set_index('Date', inplace=True)
spx_1990 = spx.loc['1940-01-02':'2014-11-01']


