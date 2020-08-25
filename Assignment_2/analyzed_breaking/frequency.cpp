//Abhyuday Pandey 170039
//Srinjay Kumar 170722
//Kumar Shivam 170354

#include <bits/stdc++.h>

using namespace std;

bool inverse(const pair<int,int> &num1, const pair<int,int> &num2){
    return(num1.first > num2.first);
}

//funtion to get the frequency of occurance of the alphabet in cipher text
void getFrequency(char* cipherText){
    //defining array to store the frequency and it's size is 26 becasue there are 26 alphabets and also sum to calculate the no of total alphabets for calculation of percentage                         
    int freq[26],sum = 0;      
    //initializing frequency array using memset library function                              
    memset(freq,0,sizeof(int)*26);
    //iterating through the cipher text                           
    for(int i=0; i<strlen(cipherText); i++){
        //using to lower function to convert capital alphabet to small and if the symbol is not an alphabet, it dosen't do anything                 
        char temp = tolower(cipherText[i]);   
        //processing alphabets only              
        if(temp >='a' && temp<='z'){   
            //counting alphabets                      
            freq[temp-'a']++;                                
            sum++;
        }
    }

    //vector pair for storing the frequency and alphabet pair
    vector <pair<int,int>> freq1;                           
    for(int i=0; i<26; i++){
        //giving vector data
        freq1.push_back(make_pair(freq[i],i));              
    }
    //sorting vector according to the frequency of letters in descending order
    sort(freq1.begin(),freq1.end(),inverse);   
    //setting the output prescision of float variable to two decimal places             
    std::cout << std::setprecision(2) << std::fixed;        
    cout<<"ALPHABET"<<" "<<"FREQUENCY(%)"<<endl;
    //iterating through sorted vector
    for(auto x:freq1){                                      
        if(x.first!=0){
            // printing the frequency and the percentage
            cout<<(char(x.second+'A'))<<"        "<<((float)x.first*100/sum)<<'%'<<endl; 
        }
        else
            cout<<(char(x.second+'A'))<<"        "<<"--"<<endl;
    }
    cout<<endl;
}

int main() {
    // the text to be deciphered
    char cipherText[] = "Lg ccud qh urg tgay ejbwdkt, wmgtf su bgud nkudnk lrd vjfbg. Yrhfm qvd vng sfuuxytj \"vkj_ecwo_ogp_ej_rnfkukf\" wt iq urtuwjm. Ocz iqa jdag vio uzthsivi pqx vkj pgyd encpggt. Uy hopg yjg fhkz arz hkscv ckoq pgfn vu wwygt nkioe zttft djkth.";
    // calling the frequency function
    getFrequency(cipherText);
}