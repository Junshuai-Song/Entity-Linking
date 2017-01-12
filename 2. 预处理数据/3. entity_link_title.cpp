//
//  main.cpp
//  entity_link_title
//
//  Created by songjs on 17/1/10.
//  Copyright © 2017年 songjs. All rights reserved.
//

#include <iostream>
#include <stdio.h>
#include <algorithm>
#include <string.h>
#include <string>
#include <stdlib.h>
#include <vector>
#include <queue>
#include <math.h>
#include <fstream>
#include <map>
using namespace std;

void title_link(){
    /*
     对data.in文件进行处理，获取2W条entity_link记录，保存在title_link.dat文件
     */
    freopen("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/title_link.dataa","r",stdin);
    freopen("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/title_link.dat","w",stdout);
    string first; char content[50010];
    while(cin>>first){
        gets(content);                                           // 吸收余下内容
        string title = first.substr(29,first.length()-30);       // 1. 对于title前缀相同
        string link = "http://dbpedia.org/resource/" + title;    // 2. 对于link，相同的前缀 + title
        cout<<title<<" "<<link<<endl;                            // 输出结果，中间用空格隔开
    }
}
void entity_final(){
    // 生成 Graph http://asx... 0.3 0.1 0 0.12 ...
    fstream title_link,final_theta;
    title_link.open("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/title_link.dat", fstream::in);
    final_theta.open("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/model-final.theta", fstream::in);
    freopen("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/entity.final","w",stdout);
    
    string str1,str2,str;
    while(getline(title_link, str1)){
//        getline(str, title_link)
        getline(final_theta, str2);
        str1 += " ";
        str1 += str2;
        cout<<str1<<endl;
    }
    title_link.close();
    final_theta.close();
}

void word_final(){
    
//    {
//        string str;
//        str = "12:43";
//        int t = (int)str.find(':');
//        cout<<t<<endl;
//        cout<<str.substr(0,t)<<" "<<str.substr(t+1,str.length()-t)<<endl;
//        return ;
//    }
    
    fstream word_map,word_tassign;
    word_map.open("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/wordmap.txt", fstream::in);
    word_tassign.open("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/model-final.tassign", fstream::in);
    freopen("/Users/songjs/Desktop/workspace/entity_link_title/entity_link_title/word.final","w",stdout);
    
    map<string, string> name;
    map<string, vector<string>> cnt;
    
    int num;
    word_map>>num;
    for(int i=0;i<num;i++){
        string str1,str2;
        word_map>>str1>>str2;
        name[str2] = str1;  // id --> name
    }
    
    string str;
    while(word_tassign>>str){
        int t=0;
        t = (int)str.find_first_of(':');        // ':'的下标
        string word_id = str.substr(0,t);
        string topic_id = str.substr(t+1, str.length()-t);
        string word_name = name[word_id];
        cnt[word_name].push_back(topic_id);     // Graph 2  2  3  2 4 ... 每个单词下面，保存了其所有的历史被赋予主题的情况
    }
    
    // 对cnt进行统计，最后输出
    int f[55];
    for(map<string, vector<string>>::iterator iter=cnt.begin(); iter!=cnt.end(); iter++){
        memset(f,0,sizeof(f));
        for(vector<string>::iterator iter2 = (*iter).second.begin(); iter2!=(*iter).second.end(); iter2++){
            f[stoi((*iter2))]++;
        }
        cout<<(*iter).first;    // word_name
        for(int i=0;i<50;i++){   //topic 是 [0-49]
            cout<<" "<<f[i];
        }
        cout<<endl;
    }
}

int main() {
    // 这里为了简便，直接用了freopen，所以下面两个程序要分开跑
    title_link();
//    entity_final();
//    word_final();
    
    return 0;
}
