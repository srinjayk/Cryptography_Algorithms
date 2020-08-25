===================================
Vignere Solver
===================================
Author - Kumar Shivam, Abhyuday Pandey and Srinjay Kumar

1. g++ --std=c++17 chiVignere.cpp
2. ./a.out [keyLength]

===================================
Algorithm
===================================
1. Let the expected length of key be "k".
2. Take all letters distanced by "k" and form k strings.
3. for each string perform chiSq score for each ROT value and record 3 minimum value.
4. Brute force on these 3^{k} possibilities. 
