"""
A Black Scholes Model Introduction

Author : Fabien Fouville

Editor : Antonin CAZALS

It is probably easier to take a look at the code on google collab : https://colab.research.google.com/drive/1sbe7sSBklJIKd-6TDS_av6IWh6bwTG5I?usp=sharing
"""

# library importation

import math
from scipy import stats
import scipy.optimize as opti
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

""" Collecting DATA"""
sp500_data = yf.download('^GSPC',"2019-01-01" ,"2023-12-31")
print("The type is:", type(sp500_data))
# let us now print the name of columns
sp500_data.shape
sp500_data.head()
#for col in sp500_data.columns:
#    print(col)

""" Plotting Close Price"""
plt.figure(figsize=(15, 5))
plt.title('S&P 500 Close Price')
# print the entries in the column whose name is 'Close'
sp500_data['Close'].plot()
plt.show()

"""Plot the Daily Log Return of SNP500"""
sp500_data['return'] = np.log(sp500_data['Close']).pct_change()
# ici on divise le log du close par la colonne d'avant donc le LOW sans prendre le log du low

plt.figure(figsize=(15, 5))
plt.title('S&P 500 Daily Log Return')
sp500_data['return'].plot()
plt.show()

plt.figure(figsize=(15, 3))
plt.title('Histogram of S&P 500 Daily Log Return')
sp500_data['return'].hist(bins=200, grid=False)
plt.show()

# plot the arithmetic daily return

#The arithmetic return is the most basic form of average: add the numbers together and divide them by the count of numbers that were added together

sp500_data['daily-return-V2'] = (sp500_data['Close']-sp500_data['Open'])/sp500_data['Open']
#daily return definition : you subtract the starting price from the closing price; You then divide by the opening price
# not quite understood : SP500 is already an average; on what should we do the average?

plt.figure(figsize=(15, 5))
plt.title('S&P 500 Daily Return V2')
sp500_data['daily-return-V2'].plot()
plt.show()

plt.figure(figsize=(15, 3))
plt.title('Histogram of S&P 500 Dail Return v2')
sp500_data['daily-return-V2'].hist(bins=200, grid=False)
print("mean and median of daily returns are ", sp500_data['daily-return-V2'].mean(), sp500_data['daily-return-V2'].median())
plt.show()

# sp500_data['return'] = np.log(sp500_data['Close']).pct_change()
# pct_change() ca calcul le pourcentage de changement par apport a la colonne precedente : dans notre cas le LOW

# sp500_data['return'] contains the data
#in order to plot both the statistics and an approximative gaussian distribution we first need the approximation on the mean and the standard deviation of the gaussian

# Remove non-finite values from the data
cleaned_data = sp500_data['return'][np.isfinite(sp500_data['return'])]

# Fit a Gaussian distribution to the cleaned data
a_fit, b_fit = stats.norm.fit(cleaned_data)
print("Normal fit yields ", a_fit, b_fit)


count, bins, ignored = plt.hist(sp500_data['return'], 30, density=True, alpha=0.5, color='b')
plt.plot(bins, 1/(b_fit * np.sqrt(2 * np.pi)) * np.exp( - (bins - a_fit)**2 / (2 * b_fit**2) ), linewidth=2, color='r')
plt.show()

# when executing, despite a clear lack of precision the approximation seems OK

# same but for the other definition of daily return

# Remove non-finite values from the data
cleaned_data = sp500_data['daily-return-V2'][np.isfinite(sp500_data['daily-return-V2'])]

# Fit a Gaussian distribution to the cleaned data
a_fit, b_fit = stats.norm.fit(cleaned_data)
print("Normal fit yields ", a_fit, b_fit)


count, bins, ignored = plt.hist(sp500_data['return'], 30, density=True, alpha=0.5, color='b')
plt.plot(bins, 1/(b_fit * np.sqrt(2 * np.pi)) * np.exp( - (bins - a_fit)**2 / (2 * b_fit**2) ), linewidth=2, color='r')
plt.show()

# here it is clear that the approximation is completely false : model is biased

# numerical test of the approximation, daily_return 1

# Remove non-finite values from the data
cleaned_data1 = sp500_data['return'][np.isfinite(sp500_data['return'])]

(statistic, pvalue) = stats.normaltest(cleaned_data1)
print (pvalue)
if pvalue < 0.05: # 0.05 is a common used limit for the pvalue test
    print("The data do not seem to follow a normal distribution.")
else:
    print("The data seem to follow a normal distribution.")

# numerical test of the approximation, daily_return_2

# Remove non-finite values from the data
cleaned_data2 = sp500_data['daily-return-V2'][np.isfinite(sp500_data['daily-return-V2'])]

(statistic, pvalue) = stats.normaltest(cleaned_data2)
print (pvalue)
if pvalue < 0.05: # 0.05 is a common used limit for the pvalue test
    print("The data do not seem to follow a normal distribution.")
else:
    print("The data seem to follow a normal distribution.")

def call_black_scholes(S, K, r, T, sigma):
  d1 = (1/(sigma*np.sqrt(T)))*(np.log(S/K)+(r+sigma**2/2)*T)
  d2 = d1-sigma*np.sqrt(T)
  price = S * stats.norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * stats.norm.cdf(d2, 0, 1)
  return price



# price a european put option
"""
Call option (C) and put option (P) prices are calculated using the following formulas:
Black-Scholes call price formula Black-Scholes put price formula

P=Ke−rTN(−d2​)−S0​N(−d1​)

N(x) is the standard normal cumulative distribution function
which looks like the opposite of the call price formula but with the N functon applied in -d1 and -d2
 """

def black_scholes_put_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    return put_price

# Example usage:
S0 = 100  # Current price of the underlying asset
K = 100   # Strike price of the option
T = 1     # Time to expiration (in years)
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility of the underlying asset

put_price = black_scholes_put_price(S0, K, T, r, sigma)
print("The price of the European put option is:", put_price)

# plot profiles of Vcall(S,K,r,T,σ) against K
S=100
#K=90
r=0.01
T=10
sigma=0.30

K = np.linspace(0, 500, 1000)  # Generates 100 evenly spaced values from -5 to 5
# Calculate y values using the function
y = call_black_scholes(S, K, r, T, sigma)

# Plot the function
plt.plot(K, y)
plt.xlabel('K Strike price of the option')
plt.ylabel('Price of the call option')

# plot profiles of Vcall(S,K,r,T,σ)  against T
S=100
K=90
r=0.01
sigma=0.30

T = np.linspace(0,100, 1000)  # Generates 100 evenly spaced values from -5 to 5
# Calculate y values using the function
y = call_black_scholes(S, K, r, T, sigma)

# Plot the function
plt.plot(T, y)
plt.xlabel('T Time to expiration (in years)')
plt.ylabel('Price of the call option')

# plot profiles of Vcall(S,K,r,T,σ) then against σ and interpret them.
S=100
K=90
r=0.01
T=10
#sigma=0.30

sigma = np.linspace(0, 3, 1000)  # usually a percentage but in certain cases can be higher then 1 example during COVID 19
# Calculate y values using the function
y = call_black_scholes(S, K, r, T, sigma)

# Plot the function
plt.plot(sigma, y)
plt.xlabel('sigma  : Volatility of the underlying asset')
plt.ylabel('Price of the call option')


def call_monte_carlo(N, S, K, r, T, sigma):
  #
  W = stats.norm.rvs(0, 1, N)  # create a vector of N independant brownian motions
  S_T = S*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*W)
  price = np.mean(np.exp(-r * T) * np.maximum(S_T - K, 0))
  return price

#Monte Carlo Methode Biased : we can calculate the difference between the real value calculated in the first part and the estimation that we calculate thanks to monte carlo

def difference(S,K,r,T,sigma,N):
  values_of_differences = np.array([])
  values_of_N = np.array([])
  exact_value = call_black_scholes(S, K, r, T, sigma)
  for i in range (N):
    delta_price= exact_value - call_monte_carlo(i, S, K, r, T, sigma)
    values_of_differences = np.append(values_of_differences, delta_price)
    values_of_N = np.append(values_of_N, i)

  plt.plot(values_of_N, values_of_differences )
  plt.axhline(y=0, color='red', linestyle='--')


  plt.xlabel('N : number of estimation with Monte Carlo')
  plt.ylabel('Difference of the exact stock price and the monte carlo estmation')

difference (S=100, K=90,  r=0.01, T=10, sigma=0.30, N=10000)


# 10000 is to small to know if the model is biased so we change strategy : we use a logarithmic scale (1,10,10**2,10**3...) and do a a number r of repeat at each power of ten; and then put a boxplot of the results

def difference(S,K,r,T,sigma,N):
  values_of_differences = np.array([])
  values_of_N = np.array([])
  exact_value = call_black_scholes(S, K, r, T, sigma)
  for i in range (N):
      delta_price= exact_value - call_monte_carlo(10**i, S, K, r, T, sigma)
      values_of_differences = np.append(values_of_differences, delta_price)
      values_of_N = np.append(values_of_N, 10**i)

  print (values_of_N)


  plt.scatter(values_of_N, values_of_differences )
  plt.axhline(y=0, color='red', linestyle='--')
  plt.xscale('log')
  plt.xlabel('N : number of estimation with Monte Carlo')
  plt.ylabel('Difference of the exact stock price and the monte carlo estmation')

difference (S=100, K=90,  r=0.01, T=10, sigma=0.30, N=8)

def call_monte_carlo_2(N, S, K, r, T, sigma):
  W = stats.norm.rvs(0, 1, N)  # create a vector of N independant brownian motions
  S_T = S*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*W)
  price = np.mean(np.exp(-r * T) * np.maximum(S_T - K, 0))
  return price

# numerical application
np.random # here we do not have a predefined seed
call_monte_carlo_2(N=10000, S=100, K=90, r=0.01, T=10, sigma=0.30)

def boxplot(S,K,r,T,sigma,N):
  widths_values = np.array([])
  values_of_N = np.array([])
  ALL_data = np.empty((N, 100))
  exact_value = call_black_scholes(S, K, r, T, sigma)

  for i in range (N):
    for j in range (100): # for each value of i we do a 100 simulation with 10**i brownian motions
      delta_price_i_j= -exact_value + call_monte_carlo_2(10**i, S, K, r, T, sigma)
      ALL_data[i][j] = delta_price_i_j
    values_of_N = np.append(values_of_N, 10**i)
    widths_values = np.append(widths_values, 10**i)

  #print (len(ALL_data))
  #print(len(values_of_N))


  plt.boxplot(ALL_data.T, positions=values_of_N, widths = widths_values, patch_artist=True)
  plt.axhline(y=0, color='red', linestyle='--')
  plt.xscale('log')
  plt.xlabel('N : number of estimation with Monte Carlo')
  plt.ylabel('Difference of the exact stock price and the monte carlo estmation')
  #plt.ylim(-20, 100)
  plt.show()

boxplot (S=100, K=90,  r=0.01, T=10, sigma=0.30, N=5)

""" Compute the volatility implied by the black scholes model given a european call price."""

# volatility is often expressed as a percentage and can go over one in certain extreme cases therefore we will guess that volatility is between 0.001 and 2

def black_implied_vol(S, K, r, T, price) :
  potential_volatility_values = np.arange(0.001,2,0.0001) # generates an array of values starting from 0.001 (inclusive), up to but not including 2, with a step size of 0.0001
  price_differences_values = np.zeros_like(potential_volatility_values) # here we create an array the same size as the potential values array but this one only has zeros
  for i in range(len(potential_volatility_values)):
      candidate = potential_volatility_values[i]
      price_differences_values[i] = price - call_black_scholes(S, K , r, T, candidate)


  index = np.argmin(abs(price_differences_values))
  implied_volatility = potential_volatility_values[index]
  return (implied_volatility)

 #Newton's Method : The idea is to start with an initial guess, then to approximate the function by its tangent line, and finally to compute the x-intercept of this tangent line. This x-intercept will typically be a better approximation to the original function's root than the first guess, and the method can be iterated.

#firstly we need a function that computes the partial derivative of the value of a call option with respect to volatility
"""
by calculating the partial derivatives of d1​ and d2​ with respect to σ and symplifing we get :
∂C/∂σ=S⋅N′(d1)⋅np.sqrt(T)
where N′(d1)N′(d1​) is the probability density function (PDF) of the standard normal distribution evaluated at d1
"""

N_prime = stats.norm.pdf # defining the probability density function (PDF) of the standard normal distribution using scipy.stats
N = stats.norm.cdf # already used before : cumulative distribution function (CDF) of the standard normal distribution

def partial_derivative(S, K, T, r, sigma):

    ### calculating d1
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    p_derivative = S * N_prime(d1) * np.sqrt(T)
    return p_derivative


def black_implied_vol_2(S, K, r, T, price, tolerance=0.01,
                            max_iterations=100):
    '''
    error tolerance in result tolerance
    max iterations to repete  the tangent line method to estimate sigma
    '''
    ## defining an  initial volatility estimatation for the Newton's method
    sigma_implied = 1
    for i in range(max_iterations):
        # difference between blackscholes price and market price with the iteratively updated volality estimation
        difference = call_black_scholes(S, K, T, r, sigma_implied) - price
        # if we are located under the tolerance level we break out
        if abs(difference) < tolerance:
            print(f'found on {i}th iteration')
            print(f'difference is equal to {difference}')
            break

        # if we are not under the tolerance level we update sigma using the newton method
        sigma_implied = sigma_implied - difference / partial_derivative(S, K, T, r, sigma_implied)
        print ( partial_derivative(S, K, T, r, sigma_implied))
    return sigma_implied