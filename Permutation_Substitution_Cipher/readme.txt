==============================
PERMSUBST.py
==============================
Author - Abhyuday Pandey, Kumar Shivam and Srinjay Kumar
------------------------------
Please ensure that ghc (Haskell compiler is also present)

Commands
---------
cipherText.txt stores the cipher text.
To just break this cipher
python3 permsubst.py

To break any permutation + substitution cipher:
1. Make a list of likely words (dictionary) in cipher_breaker/wor.txt
	We used the deciphered text of previous 2 assignments as they were very likely to occur.
2. run the command
python3 permsubst.py break_cipher <expected_length_of_perm_key>
e.g. python3 permsubst.py break_cipher 5
3. Best solution will be printed time-to-time.

Algorithm
-----------
Is fairly simple, just generate n! permutations and try to break each of them using substitution cipher breaker (cipher_breaker/substcipher.hs).
Takes around 60s for breaking (n=5) (if hint words are really good, can speed up)

===================
Works only for n <= 7 and atleast 5-10 words should match from dictionary.