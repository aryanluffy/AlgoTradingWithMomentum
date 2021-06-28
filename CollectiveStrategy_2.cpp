#include "./CSV.h"

int main(){

    auto pd=CSV();
    auto df=pd.read_csv("C:/Users/aryan/Desktop/Finance/EQUITY_L.csv");
    string dataPath="C:/Users/aryan/Desktop/Finance/Data/";
    map <string,map<string,vector<double>>> timeSeriesMap;
    for (auto ticker:df["SYMBOL"]){
        auto data=pd.read_csv(dataPath+ticker+".csv");
        vector<double> heiken_ashi={0,0,0,0};
        for (int index=0;index<data["Volume"].size();index++){
            auto date=data["Date"][index];
            timeSeriesMap[date][ticker]={stod(data["Open"][index]),
                                                            stod(data["High"][index]),
                                                            stod(data["Low"][index]),
                                                            stod(data["Close"][index]),
                                                            stod(data["Volume"][index])};
            if (index==0){
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
        
       
    

        
    return 0;
}