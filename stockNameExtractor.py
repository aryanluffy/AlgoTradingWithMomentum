import pandas as pd

df=pd.read_csv('C:/Users/aryan/Desktop/Finance/EQUITY_L.csv')
dataPath='C:/Users/aryan/Desktop/Finance/StockName.txt'
file=open(dataPath,'w+')

tickers=[]
for index in df.index:
    ticker=df['SYMBOL'][index]
    tickers.append(ticker)
file.write(str(len(tickers))+'\n')
for ticker in tickers:
    file.write(ticker+' ')

