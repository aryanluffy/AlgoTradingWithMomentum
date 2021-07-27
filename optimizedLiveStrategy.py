from numpy import add, isnan
import pandas as pd
import glob,os
import time
from sqlalchemy.util.langhelpers import symbol
import someUtils
import pymysql
from sqlalchemy import create_engine
import yfinance as yf
import datetime as dt
from Indicators import heikinAshi
import multiprocessing 
import threading
from OrderPlacer import placeOrder

user = 'aryan'
passw = 'pcmkcvib'
host =  '127.0.0.1'  # either localhost or ip e.g. '172.17.0.2' or hostname address 
port = 3306 
database = 'trading'

mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)
if not mydb.has_table('mcap31032021'):
    mcaps=pd.read_excel('C:\\Users\\aryan\\Desktop\\Trading\\MCAP31032021_0.xlsx')
    mcaps.to_sql('mcap31032021',con=mydb,if_exists='replace',index='False')
stocksCapWise= mydb.execute("SELECT * FROM `mcap31032021` LIMIT 600;").fetchall()

def getPredictions(rangeBegin,rangeEnd,recommendedStocks):
    stocks=[]
    for i in range(rangeBegin,rangeEnd):
        stockRow=stocksCapWise[i]
        stockSymbol=stockRow[2]
        stockSymbol=stockSymbol.lower()+'.ns'
        stocks.append(stockSymbol)

    liveData=yf.download(tickers=stocks,start=dt.datetime.today().strftime('%Y-%m-%d'),end=(dt.datetime.today()+dt.timedelta(days=1)).strftime('%Y-%m-%d'))
    # liveData=yf.download(tickers=stocks,period='1d')
    for index in liveData.index:
        for stock in stocks:
            if not mydb.has_table(stock):
                continue
            openPrice=liveData['Open'][stock.upper()][index]
            highPrice=liveData['High'][stock.upper()][index]
            lowPrice=liveData['Low'][stock.upper()][index]
            closePrice=liveData['Close'][stock.upper()][index]
            volume=liveData['Volume'][stock.upper()][index]
            if openPrice==None or highPrice==None or lowPrice==None or closePrice==None:
                continue
            if isnan(openPrice) or isnan(highPrice) or isnan(lowPrice) or isnan(closePrice):
                continue
            lastHeikinCandles=mydb.execute("select * from `heikinashi"+stock+"` order by Date DESC LIMIT 1").fetchall()
            if len(lastHeikinCandles)<1:
                continue
            shouldIbuy=True
            for row in lastHeikinCandles:
                if row[1]==row[3]:
                    shouldIbuy=False
            prevDayCandle=mydb.execute("select Close from `"+stock+"` order by Date DESC LIMIT 1").fetchall()
            prevClose=prevDayCandle[0][0]
            if prevClose==None:
                continue
            if closePrice/prevClose-1<0.005:
                shouldIbuy=False
            heikinAshiClosePrice=(openPrice+highPrice+lowPrice+closePrice)/4
            heikinAshiOpenPrice=(lastHeikinCandles[0][1]+lastHeikinCandles[0][4])/2
            heikinAshiLowPrice=min(heikinAshiOpenPrice,heikinAshiClosePrice,lowPrice)
            if heikinAshiOpenPrice!=heikinAshiLowPrice:
                shouldIbuy=False
            if closePrice*volume<5e7:
                shouldIbuy=False
            if shouldIbuy:
                recommendedStocks.append([closePrice/prevClose-1,stock[0:-3],closePrice])

if __name__ == "__main__":
    begin=time.time()
    processes=[]
    recommendedStocks=multiprocessing.Manager().list()
    for i in range(0,8):
        processes.append(multiprocessing.Process(target=getPredictions,args=(i*62,(i+1)*62,recommendedStocks,)))

    for i in range(0,8):
        processes[i].start()

    for i in range(0,8):
        processes[i].join()
    # capital=input("Enter Available Money\n")
    recommendedStocks=sorted(recommendedStocks,reverse=True)
    for stock in recommendedStocks:
        print(stock[1]+" "+str(round(stock[0]*100,2))+" "+str(round(stock[2],3)))
    # placeOrder(recommendedStocks,capital)
    # print(time.time()-begin)
    # time.sleep(60)
