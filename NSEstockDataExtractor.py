import yfinance as yf
import pandas as pd
import os 

df=pd.read_csv('C:/Users/aryan/Desktop/Finance/EQUITY_L.csv')
dataPath='C:/Users/aryan/Desktop/Finance/Data/'
if not os.path.exists(dataPath):
    os.mkdir(dataPath)
for index in df.index:
    ticker=df['SYMBOL'][index]+'.NS'
    data=yf.download(tickers=ticker,interval='1d',period='max')
    data.to_csv(path_or_buf=dataPath+ticker[0:-3]+'.csv')

