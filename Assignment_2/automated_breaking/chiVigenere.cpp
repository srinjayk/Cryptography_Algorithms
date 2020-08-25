#include <bits/stdc++.h>

using namespace std;


float getChiSquared(string cipherText){
    //defining array to store the frequency and it's size is 26 becasue there are 26 alphabets and also sum to calculate the no of total alphabets for calculation of percentage                         
    int freq[26],sum = 0;      
    //initializing frequency array using memset library function                              
    memset(freq,0,sizeof(int)*26);
    //iterating through the cipher text                           
    for(int i=0; i<cipherText.size(); i++){
        //using to lower function to convert capital alphabet to small and if the symbol is not an alphabet, it dosen't do anything                 
        char temp = tolower(cipherText[i]);   
        //processing alphabets only              
        if(temp >='a' && temp<='z'){   
            //counting alphabets                      
            freq[temp-'a']++;                                
            sum++;
        }
    }
    float expFreq[26];
    expFreq[0] = 8.167;
    expFreq[1] = 1.492;
    expFreq[2] = 2.202;
    expFreq[3] = 4.253;
    expFreq[4] = 12.702;
    expFreq[5] = 2.228;
    expFreq[6] = 2.015;
    expFreq[7] = 6.094;
    expFreq[8] = 6.966;
    expFreq[9] = 0.153;
    expFreq[10] = 1.292;
    expFreq[11] = 4.025;
    expFreq[12] = 2.406;
    expFreq[13] = 6.749;
    expFreq[14] = 7.507;
    expFreq[15] = 1.929;
    expFreq[16] = 0.095;
    expFreq[17] = 5.987;
    expFreq[18] = 6.327;
    expFreq[19] = 9.356;
    expFreq[20] = 2.758;
    expFreq[21] = 0.978;
    expFreq[22] = 2.560;
    expFreq[23] = 0.150;
    expFreq[24] = 1.994;
    expFreq[25] = 0.077;
    for(int i=0;i<26;i++){
        expFreq[i] = (expFreq[i]/100)*sum;
    }
    float chiSquared = 0.0;
    for(int i=0;i<26;i++){
        chiSquared = chiSquared + (freq[i] - expFreq[i])*(freq[i] - expFreq[i])/expFreq[i];
    }
    return chiSquared;
    
}

float shiftby(string text, int sft){
    string abc = "";
    for(int i=0;i<text.size();i++){
        char temp = text[i];
        temp = (((temp - 'a')+sft)%26)+'a';
        abc += temp;
    }
    return getChiSquared(abc);
}

void getMin3chi(string text, int arr[3]){
    arr[0] = 0;
    arr[1] = 0;
    arr[2] = 0;
    float firstmin= 1000000.00, secmin = 1000000.00 ,thirdmin = 1000000.00;
    for(int i=0;i<26;i++){
        float chi =  shiftby(text,i);
        if (chi < firstmin){ 
            thirdmin = secmin; 
            secmin = firstmin; 
            firstmin = chi; 
        }
  
        /* Check if current element is less than 
        secmin then update second and third */
        else if (chi < secmin){ 
            thirdmin = secmin; 
            secmin = chi; 
        } 
        else if (chi < thirdmin) 
            thirdmin = chi; 
        if(chi==firstmin) arr[0] = i;
        if(chi == secmin) arr[1] = i;
        if(chi== thirdmin ) arr[2] = i;
    }
}
map<string,bool> readDict(){
    FILE* fp;
    fp = fopen("dict.txt", "r");
    int c;
    string word = "";
    map<string,bool> dict;
    while ((c = fgetc(fp)) != EOF){
        char x = (char) c;
        if(x == ' '){
            dict[word] = true;
            word = "";
        }
        else{
            word= word + x;
        }
    }
    dict[word] = true;
    return dict;
}

void decrypt(string cipherText, int arr[],int keyLength){
    int shift = 0;
    string abc = "";
    for(int i=0;i<cipherText.size();i++){
        char temp = tolower(cipherText[i]);
        if(tolower(cipherText[i])>='a'&&tolower(cipherText[i])<='z'){
            temp = (((temp - 'a')+arr[shift])%26)+'a';
            // temp = temp - arr[shift];
            // if(temp<'a'){
            //     int a = 'a' - temp;
            //     temp = 'z' - a + 1;
            // }
            shift++;
        }
        abc+=temp;
        shift = shift % keyLength; 
    }
    cout<<abc<<endl;
}
int dictMatch(string cipherText, int arr[],int keyLength, map <string,bool>& dict){
    int score = 0;
    int shift = 0;
    string abc = "";
    for(int i=0;i<cipherText.size();i++){
        char temp = tolower(cipherText[i]);
        if(tolower(cipherText[i])>='a'&&tolower(cipherText[i])<='z'){
            temp = (((temp - 'a')+arr[shift])%26)+'a';
            // temp = temp - arr[shift];
            // if(temp<'a'){
            //     int a = 'a' - temp;
            //     temp = 'z' - a + 1;
            // }
            shift++;
        }
        abc+=temp;
        shift = shift % keyLength; 
    }
    string word = "";
    for (auto x : abc){
        if(x == ' '){
            if(dict.find(word)!=dict.end()){
                score++;
            }
            word = "";
        }
        else{
            word= word + x;
        }
    }
    if(dict.find(word)!=dict.end()){
        score++;
    }
    return score;
}

int main(int argc, char** argv) {
    // the text to be deciphered
    if(argc != 2){
        cerr<<"Expected input ./{binary} {keyLength}"<<endl;
        return 1;
    }
    map<string,bool> dict = readDict();
    // string cipherText1 = "qfc ujvc webraeb lym srrql tpnvbcj fn gqe asmmf js wgl knw scw kprae gk ewgqily fn vwtcjvag rn rzv kujmzwi abve mx kpr uarwi kujmzwia jrlj tv ubae gfkmensraeo gqal lyqf xnc a ru fnrggla gqe agum hbeb xfz gqiq evafjgc aj i frmndv ahksrakcgrol uzxunr gf npvlh baxqgb hynv jrnn qzzngnd zq o xyjcck wwe chgk iwhwd nsjajxrb aj oveel tvtbf wglywhc tfw bcbceq";
    string cipherText1 = "lg ccud qh urg tgay ejbwdkt wmgtf su bgud nkudnk lrd vjfbg yrhfm qvd vng sfuuxytj vkj ecwo ogp ej rnfkukf wt iq urtuwjm ocz iqa jdag vio uzthsivi pqx vkj pgyd encpggt uy hopg yjg fhkz arz hkscv ckoq pgfn vu wwygt nkioe zttft djkth";
    string cipherText = cipherText1;
    int length = cipherText.size();
    for (int i = length-1; i >= 0; --i){
        if(cipherText[i] == ' '||cipherText[i] == '.'||cipherText[i] == ',')
            cipherText.erase(i, 1);
        if(cipherText[i]>='A' && cipherText[i]<='Z')
        cipherText[i] = tolower(cipherText[i]);
    }
    
    int keyLength = atoi(argv[1]);
    string textShift [keyLength];
    for(int i = 0;i<keyLength;i++){
        textShift[i] = "";
    }
    for(int i=0 ; i<keyLength ; i++){
        for(int j=i; j<cipherText.size(); j = j + keyLength){
            textShift[i] += cipherText[j];
        }
    }
    
    int rotation[keyLength][3];
    int max_score = INT_MIN;
    int final_key[keyLength];
    for(int i=0;i<keyLength;i++){
        getMin3chi(textShift[i],rotation[i]);
    }
    // for(int i=0; i< keyLength; i++){
    //     cout << rotation[i][0] << " "<< rotation[i][1]<<" "<<rotation[i][2]<<endl;
    // }
    for (int i=0; i< pow(3,keyLength); i++){
        int t = i;
        int d = 0;
        int dig[keyLength] = {0};
        while(t>0){
            dig[d++] = t%3;
            t = t/3;
        }
        int key[keyLength];
        for(int i=0; i<keyLength; i++){
            key[i] = rotation[i][dig[i]];
        }
        int temp_score = dictMatch(cipherText1,key,keyLength,dict);
        // cout<<temp_score<<endl;
        if(temp_score > max_score){
            max_score = temp_score;
            for(int i=0; i< keyLength; i++) final_key[i] = key[i];
        }
    }
    cout<<"Best key: ";
    for(int i=0; i < keyLength; i++){
        // reverse used for all purposes
        cout<<(26-final_key[i])<<" ";
    }
    cout<<endl;
    decrypt(cipherText1,final_key,keyLength);

    return 0;
}