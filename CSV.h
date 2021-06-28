#include <bits/stdc++.h>

using namespace std;

class CSV{
    public:
    // Assumes first line contains the headers
    map <string,vector <string>> read_csv(string filePath=""){
        auto input=ifstream(filePath);
        string line="";
        vector <string> lines;
        map <string,vector <string>> dataFrame;
        vector <string> headers;
        while(getline(input, line)){
            if(line=="\n")break;
            vector <string> words;
            string word;
            stringstream stream(line);
            while(getline(stream,word,',')){
                words.push_back(word);
            }
            if(dataFrame.size()==0){
                headers=words;
                for(auto word:words){
                    dataFrame[word]={};
                }
                continue;
            }
            for(int i=0;i<words.size();i++){
                dataFrame[headers[i]].push_back(words[i]);
            }
        }
        return dataFrame;
    }
};
