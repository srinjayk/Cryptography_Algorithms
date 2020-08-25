Author - Abhyuday Pandey, Srinjay Kumar and Kumar Shivam

======================================================
To prepare the dictionary to preimage attack -
g++ weccak_preimage.cpp
./a.out



All the preimages will be saved in a csv file with the format
Value of k, Preimage (as a bit string)
======================================================
To prepare the dictionary to second preimage attack -
g++ weccak_second_preimage.cpp
./a.out



All the preimages will be saved in a csv file with the format
Value of k, Preimage1, Preimage2 (as a bit string)
=======================================================
To analyze collisions refer to collisions.txt, the plot is in images/

