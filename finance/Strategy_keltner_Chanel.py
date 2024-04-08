# IMPORTING PACKAGES
import requests
import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored as cl
import math

plt.rcParams['figure.figsize'] = (20,10)
plt.style.use('fivethirtyeight') 



# EXTRACTING HISTORICAL DATA
api_key = 'dc63e620e871917b093a012ab86dd6d4'

def extract_historical(api_key, start, symbol):
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start}&apikey={api_key}'
    response = requests.get(url)    
    """
    # Check if the request was successful
    if response.status_code == 200:
    # Convert the JSON response to a Python dictionary
        data = response.json()
    
    # Check if 'historical' key exists in the dictionary
        if 'historical' in data:
        # Create DataFrame from the 'historical' data and set 'date' column as index
            df = pd.DataFrame(data['historical']).set_index('date')

        else:
            print("No 'historical' data found in the response.")

    else:
        print(f"Error: {response.status_code}")
    """

    #df = pd.DataFrame(response['historical']).set_index('date')

    data = response.json() #converting the JSON data to a python dictionnary
    df = pd.DataFrame(data['historical']).set_index('date')  # 'date' column is set as the index of the DataFrame.

    df.index = pd.to_datetime(df.index) # converts the index of the DataFrame df to datetime format
    df = df.iloc[::-1] # reverses the rows of the DataFrame

    """
    pd.set_option('display.max_columns', None)
    print (df.head())
    print (df.tail())
    """
    return df

wheat_hist = extract_historical(api_key, '2000-01-01', 'AAPL')
wheat_hist


# KELTNER CHANNEL CALCULATION
def get_kc(high, low, close, kc_lookback, multiplier, atr_lookback):
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift()))
    tr3 = pd.DataFrame(abs(low - close.shift()))
    frames = [tr1, tr2, tr3]

    # True Range : greatest of the 
    # difference between the current high and the current low.
    # absolute value of the difference between the current high and the previous close.
    # absolute value of the difference between the current low and the previous close.

    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1) # true range for each time period
    # True Range : computes the maximum value along each row 

    atr = tr.ewm(alpha = 1/atr_lookback).mean()  
    # exponential moving average of the true range 

    # The alpha parameter determines the decay factor, with smaller values giving more weight to recent observations

    kc_middle = close.ewm(kc_lookback).mean()
    kc_upper = close.ewm(kc_lookback).mean() + multiplier * atr
    kc_lower = close.ewm(kc_lookback).mean() - multiplier * atr
    return kc_middle, kc_upper, kc_lower

wheat_hist = wheat_hist.iloc[:,:5]
wheat_hist['kc_middle'], wheat_hist['kc_upper'], wheat_hist['kc_lower'] = get_kc(wheat_hist['high'], wheat_hist['low'], wheat_hist['close'],20,2,20) 
wheat_hist

# KELTNER CHANNEL PLOT
plt.plot(wheat_hist[:200]['close'], linewidth = 3, label = 'RED')
plt.plot(wheat_hist[:200]['kc_upper'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC UPPER 20')
plt.plot(wheat_hist[:200]['kc_middle'], linewidth = 1.5, color = 'grey', label = 'KC MIDDLE 20')
plt.plot(wheat_hist[:200]['kc_lower'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC LOWER 20')
plt.legend(fontsize = 15)
plt.title('RED KELTNER CHANNEL 20')
plt.show()



# BACKTESTING THE STRATEGY
def implement_strategy(wheat_hist, investment, symbol):
    in_position = False
    equity = investment
    no_of_shares = 0 # we start with no shares

    for i in range(1, len(wheat_hist)-1):  #Looping through historical data

        if wheat_hist['close'][i-1] > wheat_hist['kc_lower'][i-1] and wheat_hist['close'][i] < wheat_hist['kc_lower'][i] : # condition for buying : 
            # closing price of the previous day is greater than the lower Keltner Channel (kc_lower) of the previous day AND the closing price of the current day is lower than the lower keltner channel today
            no_of_shares += math.floor(equity/wheat_hist.close[i]) # updating the number of shares we own
            no_of_shares_bought = math.floor(equity/wheat_hist.close[i])
            equity -= (no_of_shares_bought) *(wheat_hist.close[i]) # equity updated after having bought 
            in_position = True  # we now have a position
            print ( cl('BUY: ', color = 'green', attrs = ['bold']), f'{no_of_shares_bought} Shares are bought at ${wheat_hist["close"][i]} on {wheat_hist.index[i]}')




        elif (wheat_hist['close'][i-1] < wheat_hist['kc_upper'][i-1]) and (wheat_hist['close'][i] > wheat_hist['kc_upper'][i]) and (in_position == True):
        # condition for selling
        # here we sell even if we don't own : short sell strategy (thanks to a broker)
        # if the previous day stock price was under the upper keltner channel and now is Above the upper keltner channel we sell
            
            equity += (no_of_shares * wheat_hist.close[i]) # updating the value of equity 
            
            in_position = False # we don't have a position on this stock market anymore
            print(cl('SELL: ', color='red', attrs=['bold']), f'{no_of_shares} Shares are sold at ${wheat_hist["close"][i]} on {wheat_hist.index[i]}')
            no_of_shares = 0 # we sold everything

    if in_position == True:

        equity += (no_of_shares * wheat_hist.close[len(wheat_hist)-1])
        print(cl(f'\nClosing position at {wheat_hist.close[len(wheat_hist)-1]} on {str(wheat_hist.index[len(wheat_hist)-1])[:10]}', attrs = ['bold']))
        in_position = False

    earning = round( equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    print (earning)
    print (roi)


implement_strategy(wheat_hist, 100000, 'AAPL')




"""

Let's break down the strategy:

    Initialization:
        in_position is set to False, indicating whether the strategy currently holds a position in the market.
        equity is initialized with the initial investment amount.

    Looping through historical data:
        The loop iterates through each data point in wheat_hist starting from the second data point (range(1, len(wheat_hist))).

    Condition for Buying:
        If the closing price of the previous day is greater than the lower Keltner Channel (kc_lower) of the previous day AND the closing price of the current day is less than the lower Keltner Channel of the current day, it suggests a potential buy signal.
        It calculates the number of shares that can be bought with the available equity and buys those shares at the closing price.
        It updates the equity by deducting the cost of the purchased shares.
        It sets in_position to True to indicate that a position has been taken.

    Condition for Selling:
        If the closing price of the previous day is less than the upper Keltner Channel (kc_upper) of the previous day AND the closing price of the current day is greater than the upper Keltner Channel of the current day, it suggests a potential sell signal.
        It calculates the proceeds from selling the shares held in the position and adds it to the equity.
        It sets in_position to False to indicate that the position has been closed.

    Updating equity:
        If the strategy is still in a position (in_position == True), it updates the equity based on the current value of the held shares.

    Printing buy/sell signals and closing positions:
        It prints buy and sell signals along with the number of shares bought/sold and the respective closing prices.
        It prints the closing position at each iteration.

    Calculating Earnings and ROI:
        After the loop, it calculates the earnings (earning) by subtracting the initial investment from the final equity.
        It calculates the Return on Investment (ROI) by dividing the earnings by the initial investment and multiplying by 100.

"""