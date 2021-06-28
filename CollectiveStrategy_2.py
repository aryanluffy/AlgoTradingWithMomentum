from numpy import isnan
import pandas as pd

#5000cr+ market cap
#delta closing between 0.5% to 2%
#current heiken candle green with no lower wick
#previous must not be breakout
badStocks =[]
df=pd.read_csv('C:/Users/aryan/Desktop/Finance/EQUITY_L.csv')
dataPath='C:/Users/aryan/Desktop/Finance/Data/'

returnsFile=open('C:/Users/aryan/Desktop/Finance/CollectiveReturns.txt','w+')

timeSeriesMap={}

blueChipStocks={'RELIANCE','TATAELXSI','INFY','IGL',
                'BAJFINANCE','HDFCBANK','HINDUNILVR',
                'VOLTAS','BERGEPAINT','TITAN','HAVELLS',
                'CHOLAFIN'}


for index in df.index:
    ticker=df['SYMBOL'][index]
    data=pd.read_csv(dataPath+ticker+'.csv')
    heiken_ashi=[0,0,0,0]
    for index in data.index:
        if data['Date'][index] not in timeSeriesMap:
            timeSeriesMap[data['Date'][index]]={}
        timeSeriesMap[data['Date'][index]][ticker]=[data['Open'][index],
                                                        data['High'][index],
                                                        data['Low'][index],
                                                        data['Close'][index],
                                                        data['Volume'][index]]
        if index==0:
            heiken_ashi=[data['Open'][index],data['High'][index],data['Low'][index],data['Close'][index]]
            timeSeriesMap[data['Date'][index]][ticker].extend(heiken_ashi)
    for i in range(1,len(data.index)):
        date=data['Date'][i]
        heiken_ashi_prev=heiken_ashi
        heiken_ashi[3]=(data['Open'][i]+data['High'][i]+data['Low'][i]+data['Close'][i])/4
        heiken_ashi[0]=(heiken_ashi_prev[0]+heiken_ashi_prev[3])/2
        heiken_ashi[1]=max(data['High'][i],heiken_ashi[0])
        heiken_ashi[1]=max(heiken_ashi[3],heiken_ashi[1])
        heiken_ashi[2]=min(heiken_ashi[3],heiken_ashi[0])
        heiken_ashi[2]=min(heiken_ashi[2],data['Low'][i])
        timeSeriesMap[date][ticker].extend(heiken_ashi)
dates=sorted(timeSeriesMap.keys())
capital=1
returns={}
myStock={}
correct=0
wrong=0
maxSimultaneousOppurtunities={}
aveLen=0
for i in range(1,len(dates)):
    date=dates[i]
    if date[0:4]<'2010':
        continue
    if not date[0:4] in returns:
        returns[date[0:4]]=0
    if len(myStock)!=0:
        soldStocks=[]
        for ticker in myStock:
            if  ticker not in timeSeriesMap[date]:
                soldStocks.append(ticker)
                continue
            # val=timeSeriesMap[date][ticker][0]/myStock[ticker]-1
            # if not isnan(val):
            #     returns[date[0:4]]+=val
            if timeSeriesMap[date][ticker][1]/myStock[ticker]>1.0025:
                returns[date[0:4]]+=max(0.0025-0.00224,timeSeriesMap[date][ticker][0]/myStock[ticker]-1.00224)
                correct+=1
            else:
                val=timeSeriesMap[date][ticker][2]/myStock[ticker]
                if isnan(val):
                    returns[date[0:4]]+=-0.01
                else:
                    returns[date[0:4]]+=max(val-1.00224,-0.02)
                    # returns[date[0:4]]+=val-1.00224
                wrong+=1
            soldStocks.append(ticker)
        for ticker in soldStocks:
            myStock.pop(ticker,None)
    for ticker in timeSeriesMap[date]:
        if ticker not in timeSeriesMap[dates[i-1]]:
            continue
        # val=timeSeriesMap[date][ticker][3]/timeSeriesMap[dates[i-1]][ticker][0]
        val=timeSeriesMap[date][ticker][3]/timeSeriesMap[dates[i-1]][ticker][3]
        if val<1.005:
            continue
        if timeSeriesMap[date][ticker][5]!=timeSeriesMap[date][ticker][7]:
            continue
        if timeSeriesMap[date][ticker][5]>timeSeriesMap[date][ticker][8]:
            continue
        if ticker in myStock:
            continue
        if timeSeriesMap[date][ticker][3]*timeSeriesMap[date][ticker][4]<1e7:
            continue
        if len(myStock)>79:
            break
        myStock[ticker]=timeSeriesMap[date][ticker][3]
    if date[0:4] not in maxSimultaneousOppurtunities:
        maxSimultaneousOppurtunities[date[0:4]]=0
    maxSimultaneousOppurtunities[date[0:4]]=max(maxSimultaneousOppurtunities[date[0:4]],len(myStock))
    aveLen+=len(myStock)
print(correct)
print(wrong)
print(maxSimultaneousOppurtunities)
print(aveLen/len(dates))
print(returns)
tenYearAvg=0
fiveYearAvg=0
threeYearAvg=0
for x in range(2011,2021):
    tenYearAvg+=returns[str(x)]
for x in range(2016,2021):
    fiveYearAvg+=returns[str(x)]
for x in range(2018,2021):
    threeYearAvg+=returns[str(x)]  
print("TenYearAvg = " + str(tenYearAvg/10))
print("FiveYearAvg = " + str(fiveYearAvg/5))
print("ThreeYearAvg = " + str(threeYearAvg/3))




