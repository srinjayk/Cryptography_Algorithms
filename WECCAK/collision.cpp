#include<iostream>
#include<fstream>
using namespace std;

uint r[5][5] = {
	{0,36,3,41,18},
	{1,44,10,45,2},
	{62,6,43,15,61},
	{28,55,25,21,56},
	{27,20,39,8,14}
};

uint rot(uint x,uint n){
	n = n%8;
	return ((x>>(8-n))+(x<<n))%(1<<8);
	}
uint R(uint A[][5]){
	uint B[5][5] = {0};
	uint C[5] = {0};
	uint D[5] = {0};
	// Theta
	for(uint x=0; x < 5; x++)
		C[x] = A[x][0]^A[x][1]^A[x][2]^A[x][3]^A[x][4];
	for(uint x=0; x < 5; x++)
		D[x] = C[(x+4)%5]^rot(C[(x+1)%5],1);
	for(uint x=0; x < 5; x++)
		for(uint y=0; y < 5; y++)
			A[x][y] = A[x][y]^D[x];
	// pi and rho
	for(uint x=0; x < 5; x++)
		for(uint y=0; y < 5; y++)
			B[y][(2*x+3*y)%5] = rot(A[x][y],r[y][(2*x+3*y)%5]);
	// chi
	for(uint x=0; x < 5; x++){
		for(uint y=0; y < 5; y++){
			A[x][y] = B[x][y]^((~B[(x+1)%5][y]) & B[(x+2)%5][y]);
		}
	}

	return 0;
}
int main(){
	// A random seed to replay the code
	srand(1256);
	// Maximum number of iterations
	uint t = 100000000;
	// Will store count of some k if retrieved
	uint fill[65536] = {0};
	uint idx = 0;
	uint filled = 0, attempts = 0;
	while(t--){
		uint A[5][5];
		for(uint i = 0; i<5; i++){
			for(uint j=0; j<5; j++){
				if(i==4 &&(j==4||j==3))
					A[i][j] = 0;
				else
					A[i][j] = rand()%256;
			}
		}
		R(A);
		R(A);
		idx = (A[4][3]<<8) + A[4][4];
		attempts += 1;
		fill[idx] += 1;
		if(attempts % 1000000 == 0){
			printf("Attempts done %d\n",attempts);
		}
	}
	printf("Attempts %d\n",attempts);
	printf("Count for all k values is dumped in cache.txt");
	FILE* fp = fopen("cache.txt","w");
	for(int j=0; j<65536; j++) fprintf(fp,"%d\n",fill[j]);
	fclose(fp);
	return 0;
}