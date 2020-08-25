====================
DECIPHER
====================
author = Abhyuday Pandey

1. Install ghc and cabal.
2. Use cabal to install random library of haskell.
3. The cipher to be decrypted is placed in cipher.txt and wor.txt is a dictionary containing popular english words for reference.
4. ghc substcipher.hs
5. ./substcipher

----------------------
Algorithm
1. Start with a random mapping (preferably ordered by frequency).
2. Perform random swap in mappings and see if the number of words matched increases.
3. Backtrack if the word does not matches.
4. Repeat 2,3
5. Decrypt