#we will explore how to implement dynamic portfolio rebalancing using Python.
# We will download real financial data using the yfinance library, analyze the data and create a dynamic
# rebalancing strategy based on historical performance. We will leverage object-oriented programming concepts
# to build a rob ust and flexible portfolio management system.

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#ata for three diverse assets: Tesla (TSLA), Amazon (AMZN) and Bitcoin (BTC-USD).
#We will fetch data until the end of February 2024 to analyze the performance over a substantial period

assets = ['TSLA', 'ETH-USD', 'BTC-USD', 'AAPL', 'VOO', 'AMZN']
#assets = ['TSLA', 'AMZN', 'AAPL']

data = yf.download(assets, start='2020-01-01', end='2024-03-14')['Adj Close'] # extract the 'Adj Close' column from the downloaded data

#visualizing asset prices 

plt.figure(figsize=(14, 7))
for asset in assets:
    plt.plot(data.index, data[asset], label=asset)

plt.title('Historical Asset Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
#plt.show()

#  Calculating Returns and Volatility


returns = data.pct_change()  #computes the percentage change from one row to the next
#print (returns ) 
#gives a [1056 rows x 3 columns]
mean_returns = returns.mean() #mean (average) returns for each asset over the entire period
#print (mean_returns)
cov_matrix = returns.cov() #computes the covariance matrix of the returns
#print (cov_matrix)

# Annualized returns and covariance matrix
annual_returns = mean_returns * 252
annual_covariance = cov_matrix * 252

#Markowitz Portfolio Optimization technique to find the optimal
# asset allocation that maximizes returns while minimizing risk.


class Portfolio:

    #constructor
    def __init__(self, returns, cov_matrix):
        self.returns = returns  # instance attribut
        self.cov_matrix = cov_matrix    # instance attribut

    def generate_random_portfolios(self, num_portfolios): # instance method
        results = np.zeros((3, num_portfolios)) # numpy array of shape 3 x num_portfolios
        weights_record = [] # here we will store the weights assigned to each asset i the portfolio

        for i in range(num_portfolios):
            weights = np.random.random(6) # array of foor random numbers that will be the weights of the four assets
            weights /= np.sum(weights) # weights are normalized : by dividing by the sum of weights
            weights_record.append(weights) #we add to the array where we store all the weights of each portfolio

            portfolio_return = np.sum(self.returns * weights) * 252 
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights))) * np.sqrt(252) #standard deviation

            # storing for each portfolio : return, standard deviation and Sharpe Ratio in the array results
            results[0, i] = portfolio_return
            results[1, i] = portfolio_std_dev
            results[2, i] = portfolio_return / portfolio_std_dev

        return results, weights_record
    

my_portfolio = Portfolio(annual_returns, annual_covariance) # instancing a portfolio 
num_portfolios = 10000
results, weights = my_portfolio.generate_random_portfolios(num_portfolios)

plt.figure(figsize=(14, 7))
plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis')
# x axis : results[1, :], standard deviation
# y axis : results[0, :] porfolio returns
# c=results[2, :] --> color of each point in the scatter plot will be determined by the Sharpe ratio of the corresponding portfolio
# cmap : colormap we decide to use : dark blue for low values to yellow for high values

plt.title('Efficient Frontier')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.colorbar(label='Sharpe Ratio')
plt.show()

# Dynamic Portfolio Rebalancing Strategy
# Now that we have explored the efficient frontier, we can implement a dynamic portfolio rebalancing strategy
# based on historical performance. We will rebalance the portfolio quarterly based on the optimal asset
# allocation derived from the efficient frontier.

class RebalancingStrategy:
    def __init__(self, assets, returns, cov_matrix):
        self.assets = assets
        self.returns = returns
        self.cov_matrix = cov_matrix

    def get_optimal_weights(self):
        portfolio = Portfolio(self.returns, self.cov_matrix) #creating a portfolio
        num_portfolios = 10000 # hee we want to generate random portfolios
        results, weights = portfolio.generate_random_portfolios(num_portfolios) # we use the returns based on the weights of each of thse 10000 portfolios
        max_sharpe_idx = np.argmax(results[2]) # finding the maximum sharpe ratio (return / standard deviation)
        optimal_weights = weights[max_sharpe_idx] # storing the weights associated to the best sharpe ratio
        return optimal_weights
    

    def rebalance_portfolio(self):
        optimal_weights = self.get_optimal_weights() 
        current_prices = data.iloc[-1] # last price of the assets, stored in the data frame
        portfolio_value = 1000000 # setting the sum we want to invest
        asset_values = {asset: portfolio_value * weight for asset, weight in zip(self.assets, optimal_weights)}
        # dictionnary : asset_values, to an asset associates the value we can buy with the optimal weights already  assiocated to this asset
        shares_to_buy = {asset: asset_values[asset] / price for asset, price in current_prices.items()}
        # dictionnary storing the number of shares we want to buy for each asset
        weights_used = {asset : weight*100 for asset, weight in zip(self.assets, optimal_weights)}
        return shares_to_buy, asset_values, weights_used
    
strategy = RebalancingStrategy(assets, annual_returns, annual_covariance)
shares_to_buy = strategy.rebalance_portfolio()[0]
asset_values = strategy.rebalance_portfolio()[1]
weights_used = strategy.rebalance_portfolio()[2]
print(weights_used)
print(asset_values)
print(shares_to_buy)

# here we use Markowitz, an other model is black - Litterman