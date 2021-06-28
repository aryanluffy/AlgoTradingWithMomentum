#include "./CSV.h"

int main(){
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    auto pd=CSV();
    auto df=pd.read_csv("C:/Users/aryan/Desktop/Finance/EQUITY_L.csv");
    string dataPath="C:/Users/aryan/Desktop/Finance/Data/";
    unordered_map <string,unordered_map<string,vector<double>>> timeSeriesMap;
    for (auto ticker:df["SYMBOL"]){
        auto data=pd.read_csv(dataPath+ticker+".csv");
        vector<double> heiken_ashi={0,0,0,0};
        for (int index=0;index<data["Volume"].size();index++){
            auto date=data["Date"][index];
            // cout<<date<<"\n"; 
            // cout<<ticker<<"\n";
            timeSeriesMap[date][ticker]={stod(data["Open"][index]),
                                                            stod(data["High"][index]),
                                                            stod(data["Low"][index]),
                                                            stod(data["Close"][index]),
                                                            stod(data["Volume"][index])};
            if (index==0){
                // cout<<"2\n";
                heiken_ashi={stod(data["Open"][index]),
                                                            stod(data["High"][index]),
                                                            stod(data["Low"][index]),
                                                            stod(data["Close"][index]),
                                                            stod(data["Volume"][index])};
                for (auto x:heiken_ashi)
                timeSeriesMap[date][ticker].push_back(x);
            }
        }
            for (int i=1;i<data["Date"].size();i++ ){
                auto date=data["Date"][i];
                auto heiken_ashi_prev=heiken_ashi;
                // cout<<"3\n";
                heiken_ashi[3]=(stod(data["Open"][i])+stod(data["High"][i])+stod(data["Low"][i])+stod(data["Close"][i]))/4;
                heiken_ashi[0]=(heiken_ashi_prev[0]+heiken_ashi_prev[3])/2;
                heiken_ashi[1]=max(stod(data["High"][i]),heiken_ashi[0]);
                heiken_ashi[1]=max(heiken_ashi[3],heiken_ashi[1]);
                heiken_ashi[2]=min(heiken_ashi[3],heiken_ashi[0]);
                heiken_ashi[2]=min(heiken_ashi[2],stod(data["Low"][i]));
                for(auto x:heiken_ashi)
                timeSeriesMap[date][ticker].push_back(x);
            }
    }
        
    map <string,double>returns;
    map<string,double> myStock;
    int correct=0,wrong=0;
    map <string,int> maxSimultaneousOppurtunities;
    vector <string> dates;
    for(auto x:timeSeriesMap)dates.push_back(x.first);
    sort(dates.begin(),dates.end());
    for (int i=1;i<timeSeriesMap.size();i++){
        auto date=dates[i];
        if (date.substr(0,4)<"2010")
            continue;
        if (returns.find(date.substr(0,4))==returns.end())
            returns[date.substr(0,4)]=0;
        if (myStock.size()!=0){
            vector <string> soldStocks;
            for (auto tick :myStock){
                auto ticker=tick.first;
                if (timeSeriesMap[date].find(ticker)==timeSeriesMap[date].end()){
                    soldStocks.push_back(ticker);
                    continue;
                }
                if (timeSeriesMap[date][ticker][1]/myStock[ticker]>1.0025){
                    returns[date.substr(0,4)]+=max(0.0025-0.00224,timeSeriesMap[date][ticker][0]/myStock[ticker]-1.00224);
                    correct+=1;
                }
                else{
                    auto val=timeSeriesMap[date][ticker][2]/myStock[ticker];
                    if (isnan(val)){
                        returns[date.substr(0,4)]+=-0.01;
                    }
                    else{
                        returns[date.substr(0,4)]+=max(val-1.00224,-0.02);
                    }
                    wrong+=1;
                }
                soldStocks.push_back(ticker);
            }
            for (auto ticker :soldStocks)
                myStock.erase(ticker);
        }
            
        for (auto tick : timeSeriesMap[date]){
            auto ticker=tick.first;
            if (timeSeriesMap[dates[i-1]].find(ticker)==timeSeriesMap[dates[i-1]].end())
                continue;
            auto val=timeSeriesMap[date][ticker][3]/timeSeriesMap[dates[i-1]][ticker][3];
            if (val<1.005)
                continue;
            if (timeSeriesMap[date][ticker][5]!=timeSeriesMap[date][ticker][7])
                continue;
            if (timeSeriesMap[date][ticker][5]>timeSeriesMap[date][ticker][8])
                continue;
            if (myStock.find(ticker)!=myStock.end())
                continue;
            if (timeSeriesMap[date][ticker][3]*timeSeriesMap[date][ticker][4]<1e7)
                continue;
            if (myStock.size()>79)
                break;
            myStock[ticker]=timeSeriesMap[date][ticker][3];
        }
        if (maxSimultaneousOppurtunities.find(date.substr(0,4))==maxSimultaneousOppurtunities.end())
            maxSimultaneousOppurtunities[date.substr(0,4)]=0;
        maxSimultaneousOppurtunities[date.substr(0,4)]=max(maxSimultaneousOppurtunities[date.substr(0,4)],(int)myStock.size());
    }
    cout<<correct<<" "<<wrong<<"\n";
    for(auto x:returns){
        cout<<x.first<<" "<<x.second<<"\n";
    }
    for(auto x:maxSimultaneousOppurtunities){
        cout<<x.first<<" "<<x.second<<"\n";
    }
    return 0;
}

// 131076 11984
// 2010 58.8437
// 2011 22.0033
// 2012 45.5984
// 2013 26.5914
// 2014 63.0698
// 2015 50.9555
// 2016 50.1126
// 2017 70.7859
// 2018 47.4244
// 2019 36.1713
// 2020 123.466
// 2021 66.9459