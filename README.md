# GeneticTrader

## Introduction

This research employs Genetic Algorithms to identify optimal parameters for a trading strategy aimed at maximizing performance on the NASDAQ 100 index since its inception. Additionally, we utilize Hidden Markov Models to detect market regimes, ensuring that the trading strategy is applied exclusively during periods characterized by an "uptrend."

## Details


## Hidden Markov Model (HMM)
- Number of Hidden States: 3
- Observation Features (Emissions):
  - Returns
  - Volatility
  - (Optional) Interest Rate
  - (Optional) M1 Velocity
  - (Optional) Consumer Price Index
 
## Trading Strategy
- A simple Exponential Moving Average (EMA) crossover strategy defined by two parameters (x1, x2).
- Enter long positions when EMA x1 exceeds EMA x2.

## Genetic Algorithms
- Optimization of Exponential Moving Average parameters (x1, x2).
- Determination of Position Size as a percentage of the total portfolio.
- Specification of Risk per Trade as a percentage of the portfolio.

## License
MIT License

Copyright (c) [2025] [Serban-Constantin Chisca]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
