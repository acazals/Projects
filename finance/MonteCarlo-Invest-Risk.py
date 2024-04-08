import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
#from math import floor
#from termcolor import colored as cl

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

# EXTRACTING STOCK DATA
api_key = 'dc63e620e871917b093a012ab86dd6d4'
def extract_historical(api_key, start, symbol):
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start}&apikey={api_key}'
    data = requests.get(url) # sends an HTTP GET request to the URL 
    data = data.json()   # converts the response from the HTTP GET request into a JSON 
    df = pd.DataFrame(data['historical']).set_index('date') # setting the index to date 
    df.index = pd.to_datetime(df.index) # converting the index (date) to a datetime objects
    df = df.iloc[::-1] # reverse order for the rows
    return df

df = extract_historical(api_key, '2020-01-01', 'VOO') # Vanguard dataframe
#print(df)

# calculating daily return : 
daily_returns = df["adjClose"].pct_change().dropna() # removes rows with missing values
#print(daily_returns)


def price_simulation(num_simulations, forecast_days) : 
    simulations = np.zeros((num_simulations, forecast_days))
    last_price = df["adjClose"].iloc[-1]
    for i in range(num_simulations):
        cumulative_returns = np.random.choice(daily_returns, size=forecast_days, replace=True).cumsum()
        simulations[i, :] = last_price * (1 + cumulative_returns)
            #  function randomly samples from a given array: daily_returns
            # size = forecast_days : number of samples we want to extract
            # replace=True, it means that the same sample may be drawn multiple times.
            #np.random generates random daily returns from the daily return array
            # .cumsum() : calculates the cumulative sum of these returns, array where each element represents the cumulative sum of the daily returns up to that point
            # [i, :] : working on the whole row number i
    return simulations

simulations = price_simulation(1000, 365)

plt.figure(figsize=(10, 6))
plt.plot(simulations.T, alpha=0.09) # plotting the transposed matrix, alpha = 0.025 sets lines to be very transparent
plt.title("Monte Carlo Simulation of Future Prices")
plt.xlabel("Day")
plt.ylabel("Price")
plt.show()

def dailyreturn(dataframe):
    daily_returns = dataframe["adjClose"].pct_change().dropna() # assuming we hace a right dataframe
    return daily_returns

def averagedailyreturn(dataframe): 
    return ( dailyreturn(dataframe).mean())

def volatility(dataframe):
    return (dailyreturn(dataframe).std())

def dailylogreturn(dataframe): 
    return ( np.log(df["adjClose"] / df["adjClose"].shift(1)).dropna()) # assuming we have a corresponding dataframe


#calculating 
def results (initial_investment, num_simulation, forecast_days, desired_return, dataframe, confidence_level): 
    
    simulated_end_returns = np.zeros(num_simulation)
    average_daily_return = averagedailyreturn(dataframe)
    volatility_used = volatility(dataframe)

    for i in range(num_simulation):
        random_returns = np.random.normal(average_daily_return, volatility_used, forecast_days) # np.random.normal : getting numbers from a gaussian distribution with a specified mean, standard deviation and forecast_days = number of random numbers to generate
        cumulative_return = np.prod(1 + random_returns) # calculates the cumulative return by first adding 1 to each random return, and calculating the product of all the returns, giving a scalar value
        simulated_end_returns[i] = initial_investment * cumulative_return # simulating the growth of investment over time
    
    final_investment_values = simulated_end_returns
    sorted_returns = np.sort(final_investment_values)

    index_at_var = int((1-confidence_level) * num_simulation) # catching the index of the first return that is under 95% of the other investments
    # (1-conidence_level) percentile of the sorted returns, often 5%
    var =  initial_investment - sorted_returns[index_at_var] # loss at the limit of the confidence level
    conditional_var = initial_investment - sorted_returns[:index_at_var].mean() # average loss under the confidence level
    print(f"Value at Risk (95% confidence): £{var:,.2f}") #  format a floating-point number (var) with two decimal places and include a comma as a thousands separator
    print(f"Expected Tail Loss (Conditional VaR): £{conditional_var:,.2f}")

    condition = final_investment_values >= initial_investment * (1 + desired_return)
    num_success = np.sum(condition)
    probability_of_success = num_success / num_simulation
    print(f"Probability of achieving at least a {desired_return*100}% return: {probability_of_success*100:.2f}%")

    condition2 = final_investment_values >= initial_investment 
    num_no_loss = np.sum(condition2)
    probability_of_no_loss = num_no_loss / num_simulation
    print(f"Probability having a positive return is  {probability_of_no_loss*100:.2f}%")

    return (final_investment_values, initial_investment, desired_return, var) # returning what we need for the plot


statistics = results(initial_investment= 10000, num_simulation =1000, forecast_days=365, desired_return=0.10, dataframe = df, confidence_level=0.95)

final_investment_values = statistics[0]
initial_investment = statistics[1]
desired_return = statistics[2]
var = statistics[3]

plt.figure(figsize=(10, 6))
plt.hist(final_investment_values, bins=50, alpha=0.75) # plotting a histogram
plt.axvline(
    initial_investment * (1 + desired_return), #target value of the return
    color="r",
    linestyle="dashed",
    linewidth=2,
    )
plt.axvline(initial_investment - var, color="g", linestyle="dashed", linewidth=2) # return at the beginning of the top less 5%
plt.title("Distribution of Final Investment Values")
plt.xlabel("Final Investment Value")
plt.ylabel("Frequency") # 
plt.show()

"""
Important to know : 

 VaR, or Value at Risk, VaR is a statistical measure that quantifies the maximum potential loss

 
 about  a histogram : bins =50 histogram will divide the range (eg from 0 to 100 ) into 50 equal-width intervals, each spanning 2 units (since 100 / 50 = 2). It will then count the number of data points falling into each interval and display the counts as bars.
"""