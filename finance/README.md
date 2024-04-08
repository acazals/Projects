I worked on a few projects about finance and algorithmic trading thanks to  Abdelkarim Abdallah  and Fabien Fouville

1) Keltner Channel Trading Strategy (mathematical aspect : exponential moving average: EMA)

2) Wasserstein Distances / persistence diagram ( 0 dimensional) between prices of an asset on a window time of 20 days
We use the Wasserstein distance - a measure from the theory of optimal transport - on financial time series data.
The essence is to compare and contrast two sets of points, segments of logarithmic returns in this case,
to quantify the divergence of their structural patterns. This measure, although inherently dynamic,
provides insight into changes in market dynamics, potentially alluding to unforeseen market movements

3) Monte-Carlo Simulation of the return of an asset : using np.random () we compute the Value at Risk(95% confidence)
   and the Expected Tail Loss,

4) Protofolio Optimization using Markowitz, sharpe ratio and OOP in python
