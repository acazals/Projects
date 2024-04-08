import yfinance as yf
import numpy as np
from ripser import Rips
import persim
import matplotlib.pyplot as plt
import warnings
plt.rcParams['text.usetex'] = False

def fetch_data(ticker_name, start_date, end_date): 
    raw_data = yf.download(ticker_name, start_date, end_date)
    adjusted_close = raw_data['Adj Close'].dropna()
    prices = adjusted_close.values
    log_returns = np.log(prices[1:] / prices [:-1])
    return adjusted_close, log_returns

# wasserstein distance : minimum amount of work needed to transform one segment into the other : here we have two segments, we want to change the persistance diagram of one into the one of the other
def compute_wasserstein_distances(log_returns, window_size, rips):
    """Compute the Wasserstein distances."""
    n = len(log_returns) - (2 * window_size) + 1 #number of consecutive segments we will extract from log_return
    distances = np.full((n, 1), np.nan) # Numpy array (n,1) to stock the distances

    for i in range(n): # for each segment
        # array slicing, arrays reshaped to column vectors 
        segment1 = log_returns[i:i+window_size].reshape(-1, 1)
        segment2 = log_returns[i+window_size:i+(2*window_size)].reshape(-1, 1)
        
        if segment1.shape[0] != window_size or segment2.shape[0] != window_size: # skip to the next iteration if one of the segment is not the right size
            continue
        
        # computing persistent homology : collection of persistence diagrams (only 0 dimensional here ) 
        dgm1 = rips.fit_transform(segment1)
        dgm2 = rips.fit_transform(segment2)

        # computing the wasserstein distance between each segment
        distance = persim.wasserstein(dgm1[0], dgm2[0], matching=False) # matching = False : we only want the wasserstein distance not the distance AND the cross-similarity matrix
        distances[i] = distance
        # distance index i associated to the values from index i to index i + 2*window_size
    return distances


def plot_data(prices, distances, threshold, window_size):
    """Generate the plots."""
    dates = prices.index[window_size:-window_size] # extracting the dates linked to each price
    valid_indices = ~np.isnan(distances)
    valid_dates = dates[valid_indices.flatten()]
    valid_distances = distances[valid_indices]
    alert_indices = [i for i, d in enumerate(valid_distances) if d > threshold]
    alert_dates = [valid_dates[i] for i in alert_indices]
    alert_values = [prices.iloc[i + window_size] for i in alert_indices]
    
    fig, ax = plt.subplots(2, 1, figsize=(25, 12), dpi=80)
    ax[0].plot(valid_dates, prices.iloc[window_size:-window_size], label=ticker_name)
    ax[0].scatter(alert_dates, alert_values, color='r', s=30)
    ax[0].set_title(f'{ticker_name} Prices Over Time')
    ax[0].set_ylabel('Price')
    ax[0].set_xlabel('Date')

    ax[1].plot(valid_dates, valid_distances)
    ax[1].set_title('Wasserstein Distances Over Time')
    ax[1].set_ylabel('Wasserstein Distance')
    ax[1].axhline(threshold, color='g', linestyle='--', alpha=0.7) # drawing a horizontal line over the plot : treshold
    ax[1].set_xlabel('Date')
    plt.tight_layout()
    plt.show()


ticker_name = '^GSPC' # SP500
start_date_string = "2007-01-01"
end_date_string = "2024-04-21"
window_size = 20
threshold = 0.045
# dgm1 or dgm2 might have points with non-finite death time when computing persistence diagrams, we have to ignore those points
warnings.filterwarnings('ignore')

prices, log_returns = fetch_data(ticker_name, start_date_string, end_date_string)
rips = Rips(maxdim=0) # includes 0-dimensional points but not 1-dimensional edges or 2-dimensional triangles
wasserstein_dists = compute_wasserstein_distances(log_returns, window_size, rips)
plot_data(prices, wasserstein_dists, threshold, window_size)



"""
how do we calculate the wasserstein distance between to datasets? 

we first compute their persistence diagrams (persistence diagram have a different number of points )

we than link each point of the persistence diagram A to the nearest point of the other dataset persistence diagram

if one point of one persistence diagram has no neighboors we will link him to the y=x axis

finally we compute the sum of all the distances of the point to their matching or to the y=x axis, it gives the total cost of transporting

The optimal matching minimizes the total cost of transporting

"""

"""
descrbing the plotting : 
~np.isnan(distances) : np.isnan(distances) returns a boolean array where True indicates NaN values, and False indicates non-NaN values. The ~ operator negates this boolean array, so valid_indices has True at valid indices and False at invalid (NaN) indices
valid_dates = dates[valid_indices.flatten()]  select only the valid dates from the dates array
valid_distances = distances[valid_indices] same but for distances
alert_indices = [i for i, d in enumerate(valid_distances) if d > threshold] :  If the distance d at index i is greater than the threshold, the index i is included in the list alert_indices.
alert_dates = [valid_dates[i] for i in alert_indices] # collecting the interesting dates lnked to distances over the treshhold
alert_values = [prices.iloc[i + window_size] for i in alert_indices]
"""