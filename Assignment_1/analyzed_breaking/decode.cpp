//Abhyuday Pandey 170039
//Srinjay Kumar 170722
//Kumar Shivam 170354

#include <bits/stdc++.h>

using namespace std;

// the function to get the plain text
void getPlainText(char* cipherText, char* key){
    // getting the length of the ciphertext
    int len = strlen(cipherText);
    // variable to store the plaintext
    char plainText[len];
    // iterating through all the characters of the ciphertext
    for(int i=0; i<strlen(cipherText); i++){
        char temp = tolower(cipherText[i]);
        if(temp >='a' && temp<='z')
            temp = char(key[(int(temp-'a'))]);
        if(cipherText[i]>='a' && cipherText[i]<='z')
            temp = tolower(temp);
        plainText[i] = temp;
    }
    cout<<plainText<<endl;
}

int main() {
    // it is the key derived manually
    char key[] = "CPTHAWMQBV-RNY-ELSF--GOIUD";
    // the text to be deciphered
    char cipherText[] = "Nwy dejp pmcplpz cdp sxlrc adegipl ws cdp aejpr. Er nwy aem rpp cdplp xr mwcdxmv ws xmcplprc xm cdp adegipl. Rwgp ws cdp qecpl adegiplr fxqq ip gwlp xmcplprcxmv cdem cdxr wmp, x eg rplxwyr. Cdp awzp yrpz swl cdxr gprrevp xr e rxgbqp ryircxcycxwm axbdpl xm fdxad zxvxcr dejp ippm rdxscpz in 2 bqeapr. Swl cdxr lwymz berrfwlz xr vxjpm ipqwf, fxcdwyc cdp hywcpr.";
    getPlainText(cipherText, key);
}