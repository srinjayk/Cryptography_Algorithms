//Abhyuday Pandey 170039
//Srinjay Kumar 170722
//Kumar Shivam 170354

#include <cctype>
#include <iostream>
#include <cstring>
#include <cstdio>


using namespace std;

// checking if the character is a alphabet
bool isalpha(char ch){
	if(ch >= 'a' && ch <= 'z') return true;
	if(ch >= 'A' && ch <= 'Z') return true;
	return false;
}

int main(){
	// the text to be decrypted
	char inp[] = "Lg ccud qh urg tgay ejbwdkt, wmgtf su bgud nkudnk lrd vjfbg. Yrhfm qvd vng sfuuxytj \"vkj_ecwo_ogp_ej_rnfkukf\" wt iq urtuwjm. Ocz iqa jdag vio uzthsivi pqx vkj pgyd encpggt. Uy hopg yjg fhkz arz hkscv ckoq pgfn vu wwygt nkioe zttft djkth.";
	for (int i=0; i<strlen(inp); i++)
        if(inp[i]>='A' && inp[i]<='Z') inp[i] += 32;

    int j=0;
    // the key to be found out manually
	int key[] = {2,3,5,2,2,1,10,2,6};
	// iterating over all the possible keys
	for(int i=0; i<9; i++){
		char out[1024];
		out[j] = '\0';
		int l=0;
		// iterating over all the characters of the text
		for(int k=0; k<strlen(inp); k++){
			if(isalpha(inp[k])){
				// getting key for a particular character
				int toShift = key[(i+l)%9];
				// deciphering the character
				out[k] = (inp[k] - toShift >= 97) ? (inp[k] - toShift) : (inp[k] - toShift + 26);
				l++;
			}
			else{
				out[k] = inp[k];
			}
		}
		// printing the plain text
		cout<<out<<endl;
	}
	return 0;
}
