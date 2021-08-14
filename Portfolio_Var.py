import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import date
from sklearn.linear_model import LinearRegression

data = pd.read_csv("dataset_github.csv")
data = data.loc[(data['RSI'] > 20) & (data['RSI']< 90) & (data['STOCH'] > 10) & (data['STOCH']< 90) & (data['SHARPE'] < 10) & (data['SHARPE']> 0) & (data['TREYNOR'] > 0) & (data['TREYNOR']< 80) & (data['P/VL'] > 0) & (data['P/VL']< 3.1)]
df = Metrics.standarization(data)
Metrics.clustering(df)
n = data.shape[1]
data.insert(n, "CLUSTERS",df['CLUSTERS'])
print("CLUSTERS:")
data['CLUSTERS'].value_counts()
means = data.groupby('CLUSTERS').mean()
selected = data[data['CLUSTERS'] == 1]
portfolio = Metrics.standarization(selected)
Metrics.clustering(portfolio)
selected = selected.drop(['CLUSTERS'], axis=1)
n = selected.shape[1]
selected.insert(n, "CLUSTERS", portfolio['CLUSTERS'])
selected['CLUSTERS'].value_counts()
means = selected.groupby('CLUSTERS').mean()
selected_portfolio = selected[selected['CLUSTERS'] == 1]
portfolio = (np.random.choice(selected_portfolio['TICKER'], 5, replace=False)).tolist()
composite = '^IXIC'
Risk_Free_Rate = float(input("Enter the risk free rate: "))
Confidence_Interval = float(input("Enter the confidence interval: "))
Years = int(input("Enter the years to calculate: "))
today = date.today()
start = today.replace(year=today.year - Years)
prices = yf.download(portfolio, start = start, end = today, interval="1d" )['Adj Close']
prices[composite] = yf.download(composite, start = start, end = today, interval="1d" )['Adj Close']
prices = prices.fillna(method='ffill')
prices = prices.fillna(method='bfill')
prices = prices.fillna(prices.mean())
if prices.loc[:, prices.isna().any()].shape[1] >= 1:
    Last_price, prices, portfolio = Metrics.null_portfolio(prices, portfolio, selected_portfolio)
else:
    Last_price = yf.download(portfolio, start = start, end = today)['Adj Close']
Shares = [int(input("Enter the quantity of shares for {} ".format(portfolio[i]))) for i in range (0, len(portfolio))]
Ponderation, Average_Daily_Return, Portfolio_Daily_Risk, Portfolio_Annual_Return, Portfolio_Annual_Risk, Investment = Metrics.Risk(portfolio, composite, prices, Last_price, Risk_Free_Rate, Shares, Year)
Daily_VaR, Percent_VaR, Diversification = Metrics.VaR(prices, portfolio, Last_price, Shares, Confidence_Interval)
print(f"Investment in Portfolio: ${round(float(Investment),2)}")
print(f"Portfolio Annual Return: {round((float(cleaner(Portfolio_Annual_Return)) * 100),2)}%")
print(f"Portfolio Daily Risk: {round((float(cleaner(Portfolio_Daily_Risk)) * 100),2)}%")
print(f"Portfolio Annual Risk: {round((float(cleaner(Portfolio_Annual_Risk)) * 100),2)}%")
print(f"Portfolio VaR:\n{Percent_VaR * 100}")
if Diversification < float(Daily_VaR.T['TOTAL']):
    print("Great VaR diversification")
else:
    print("Need to review the diversification")
