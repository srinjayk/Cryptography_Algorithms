# Team Name SchutzSAS
# Abhyuday Pandey (170039)
# Kumar Shivam    (170354)
# Srinjay Kumar   (170722)

import subprocess
import json
import sys
import os
import random

# Constants defined from Moodle.cse.iitk.ac.in
# procedure taken from http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

# the initial permutation matrix to be used before starting DES
ip = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

# the inverse permutation matrix to be used after executing the rounds of the DES
ipinv = [8,40,16,48,24,56,32,64,
         7,39,15,47,23,55,31,63,
         6,38,14,46,22,54,30,62,
         5,37,13,45,21,53,29,61,
         4,36,12,44,20,52,28,60,
         3,35,11,43,19,51,27,59,
         2,34,10,42,18,50,26,58,
         1,33,9,41,17,49,25,57]

# the expansion matrix.
# it converts 32 bits to 48 bits
expand = [32,1,2,3,4,5,
       4,5,6,7,8,9,
       8,9,10,11,12,13,
       12,13,14,15,16,17,
       16,17,18,19,20,21,
       20,21,22,23,24,25,
       24,25,26,27,28,29,
       28,29,30,31,32,1]

# the permutation matrix
perm = [16,7,20,21,
        29,12,28,17,
        1,15,23,26,
        5,18,31,10,
        2,8,24,14,
        32,27,3,9,
        19,13,30,6,
        22,11,4,25]

# the matrices for the 8 boxes
s  =[[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
      [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
      [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
      [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

	 [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
      [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
      [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
      [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

	 [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
      [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
      [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
      [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

	 [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
      [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
      [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
      [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

	 [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
      [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
      [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
      [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

	 [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
      [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
      [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
      [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

	 [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
      [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
      [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
      [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

	 [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
      [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
      [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
      [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]]

# used for calculating key schedules
pc1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

# used for calculating key schedules
pc2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

# file to store the requests made to the server and their output 
file1 = open("inputoutput.txt","w") 

# function to calculate the gcd
def gcd(a, b): 
	if b == 0: 
		return a; 
	else: 
		return gcd(b, a % b)

# function to calculate left rotate
def leftRotate(arr, d, n): 
	d = d % n 
	g_c_d = gcd(d, n) 
	for i in range(g_c_d): 
		temp = arr[i] 
		j = i 
		while 1: 
			k = j + d 
			if k >= n: 
				k = k - n 
			if k == i: 
				break
			# print(j,k)
			arr[j] = arr[k] 
			j = k 
		arr[j] = temp 

# function to calculate output of i'th s box
def sbox(text,i):
	global s
	res = ""
	row = 2 * (ord(text[0]) - ord('0')) + (ord(text[5]) - ord('0'))
	col = 8 * (ord(text[1]) - ord('0')) + 4 * (ord(text[2]) - ord('0')) + 2 * (ord(text[3]) - ord('0')) + (ord(text[4]) - ord('0'))
	val = s[i][row][col]
	res = res + format(val, '04b')
	return res

# calculating output for S boxes
def Sbox(text):
	global s
	res = ""
	for i in range(0,8):
		row = 2 * (ord(text[i * 6]) - ord('0')) + (ord(text[i * 6 + 5]) - ord('0'))
		col = 8 * (ord(text[i * 6 + 1]) - ord('0')) + 4 * (ord(text[i * 6 + 2]) - ord('0')) + 2 * (ord(text[i * 6 + 3]) - ord('0')) + (ord(text[i * 6 + 4]) - ord('0'))
		val = s[i][row][col]
		res = res + format(val, '04b')
	return res

# calculating permutation
def permutation(text):
	global perm
	res = ""
	for i in perm:
		res = res + text[i-1]
	return res

def inv(perm1):
	inverse1 = [1]*len(perm1)
	for i,p in enumerate(perm1):
		inverse1[p-1] = i+1
	return inverse1

# calculate the expansion of the text
def expansion(text):
	global expand
	res = ""
	for i in expand:
		res = res + text[i-1]
	return res

# calculate xor of two strings
def xor(a,b):
    ans = ""
    y = int(a, 2)^int(b,2)
    return bin(y)[2:].zfill(len(a))

def sbox(text,i):
	global s
	res = ""
	row = 2 * (ord(text[0]) - ord('0')) + (ord(text[5]) - ord('0'))
	col = 8 * (ord(text[1]) - ord('0')) + 4 * (ord(text[2]) - ord('0')) + 2 * (ord(text[3]) - ord('0')) + (ord(text[4]) - ord('0'))
	val = s[i][row][col]
	res = res + format(val, '04b')
	return res


def inverseInputPermutation(text):
	global ip
	res = ""
	pinverse = inv(ip)
	for i in pinverse:
		res = res + text[i-1]
	return res

def inverseOutputPermutation(text):
	global ipinv
	res = ""
	pinverse = inv(ipinv)
	for i in pinverse:
		res = res + text[i-1]
	return res

def inversePermutation(text):
	global perm
	res = ""
	pinverse = inv(perm)
	for i in pinverse:
		res = res + text[i-1]
	return res

def convertHex(text):
	temp1 = ""
	for i in range(0,len(text)//4):
		temp1 = temp1 + chr(ord('f')+int(8*int(text[i*4])+4*int(text[i*4+1])+2*int(text[i*4+2])+int(text[i*4+3])))
	return temp1

def convertBinary(text):
	return ''.join(format(ord(i)-ord('f'), '0>4b') for i in text)


# def invManyToOne(arr,length):
# 	small_length = len(arr)
# 	# x means transition unknown
# 	res = ['x']*length
# 	for i,p in enumerate(arr):
# 		res[p-1] = i+1
# 	return res

# filling the bits in 64 bit key using the key from the third round
def getkeybitsfromK3(text):
	global pc1,pc2
	# CD is a 56 bit value
	CD = ['x']*56
	for i,p in enumerate(pc2):
		CD[p-1] = text[i]
	# Now we have CD intact 
	# print(CD) 
	C = CD[:28]
	D = CD[28:]
	leftRotate(C,-4,28)
	leftRotate(D,-4,28)
	CD = C + D
	# print(CD)
	# Now we have K_plus
	K = ['x']*64
	for i,p in enumerate(pc1):
		K[p-1] = CD[i]
	return K

# filling the bits in 64 bit key using the key from the third round
# if we have a conflict with a bit from the third round, then we have an error
def getkeybitsfromK2(text):
	global pc1,pc2
	# CD is a 56 bit value
	CD = ['x']*56
	for i,p in enumerate(pc2):
		CD[p-1] = text[i]
	# Now we have CD intact 
	# print(CD) 
	C = CD[:28]
	D = CD[28:]
	leftRotate(C,-2,28)
	leftRotate(D,-2,28)
	CD = C + D
	# print(CD)
	# Now we have K_plus
	K = ['x']*64
	for i,p in enumerate(pc1):
		K[p-1] = CD[i]
	return K

# getting keys for rounds one, two and three from the 64 bit key
def getK1K2K3(K):
	global pc1,pc2
	CD = [0]*56
	for i,p in enumerate(pc1):
		CD[i] = K[p-1]
	C,D = CD[:28],CD[28:]
	# Evaluate K1
	leftRotate(C,1,28)
	leftRotate(D,1,28)
	K1 = [0]*48
	CD = C+D
	for i,p in enumerate(pc2):
		K1[i] = CD[p-1]
	leftRotate(C,1,28)
	leftRotate(D,1,28)
	K2 = [0]*48
	CD = C+D
	for i,p in enumerate(pc2):
		K2[i] = CD[p-1]
	leftRotate(C,2,28)
	leftRotate(D,2,28)
	K3 = [0]*48
	CD = C+D
	for i,p in enumerate(pc2):
		K3[i] = CD[p-1]
	return ''.join(K1),''.join(K2),''.join(K3)

# breaking the third round of the DES
def breakDES3():
	poss_keys = []
	for i in range(0,8):
		poss_keys.append([])
		for j in range(0,63):
			temp_a = format(j,'06b')
			poss_keys[i].append(temp_a)
	ctr = 0
	xor_in = "ghikhighffffffff"
	xor_in = convertBinary(xor_in)

	while 1:
		ctr += 1
		#inpxor = int("405c000004000000",16)
		a_in = format(random.getrandbits(64),'064b')
		b_in = xor(a_in,xor_in)
		a = convertHex(inverseInputPermutation(a_in))
		b = convertHex(inverseInputPermutation(b_in))
		#send to server and get a_out and b_out
		str_in = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/des"%(a)
		file1.write(str_in)
		file1.write("\n")
		a_out = json.loads(subprocess.check_output(str_in,shell=True).decode())['ciphertext']
		file1.write(str(a_out))
		file1.write("\n")
		str_in = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/des"%(b)
		file1.write(str_in)
		file1.write("\n")
		out_dict = json.loads(subprocess.check_output(str_in,shell=True).decode())
		file1.write(str(out_dict))
		file1.write("\n")
		b_out = out_dict['ciphertext']
		file1.write(str(b_out))
		file1.write("\n")
		# print(out_dict['success']==False)
		# print(a_out)
		a_out = inverseOutputPermutation(convertBinary(a_out))
		b_out = inverseOutputPermutation(convertBinary(b_out))

		L0_a = a_in[:32]
		R0_a = a_in[32:]
		L3_a = a_out[:32]
		R3_a = a_out[32:]

		L0_b = b_in[:32]
		R0_b = b_in[32:]
		L3_b = b_out[:32]
		R3_b = b_out[32:]
		
		#3rd round
		R2_a = L3_a
		R2_b = L3_b

		R2_a_exp = expansion(R2_a)
		R2_b_exp = expansion(R2_b)
		R2_exp_xor = xor(R2_a_exp,R2_b_exp) #
		R3_xor = xor(R3_a,R3_b)
		L2_xor = xor(L0_a,L0_b)
		R2_sbox_xor = xor(inversePermutation(R3_xor),inversePermutation(L2_xor)) #

		for i in range(0,8):
			temp_keys = []
			for j in range(0,64):
				temp_a = format(j,'06b')
				temp_b = xor(temp_a, R2_exp_xor[6*i:6*i+6])
				temp_a_sbox = sbox(temp_a,i)
				temp_b_sbox = sbox(temp_b,i)
				if xor(temp_a_sbox,temp_b_sbox) == R2_sbox_xor[4*i:4*i+4]:
					key1 = xor(temp_a,R2_a_exp[6*i:6*i+6])
					key2 = xor(temp_b,R2_b_exp[6*i:6*i+6])
					temp_keys.append(key1)
					temp_keys.append(key2)
			# print(temp_keys)
			poss_keys[i] = list(set(poss_keys[i])&set(temp_keys))
		# print(poss_keys)
		flag = True
		for i in range(0,8):
			if(len(poss_keys[i])!=1):
				flag = False
		if(flag == True):
			print("Round 3 Key recovered in #%d chosen plaintext attacks"%(2*ctr))
			# print(poss_keys)
			K_3 = ''
			for i in range(0,8):
				K_3 += ''.join(poss_keys[i])
			return K_3
			# Find key_bits from K_3

# extracting the key for the second round after having the 
# key for the second key
def round2key(key_3r):
	poss_keys_2r = []
	for i in range(0,8):
		poss_keys_2r.append([])
		for j in range(0,63):
			temp_2r = format(j,'06b')
			poss_keys_2r[i].append(temp_2r)
	ctr2 = 0
	while 1:
		xor_in = "ghikhighghikhgst"
		xor_in = convertBinary(xor_in)
		#inpxor = int("405c000004000000",16)
		a_in = format(random.getrandbits(64),'064b')
		b_in = xor(a_in,xor_in)
		a = convertHex(inverseInputPermutation(a_in))
		b = convertHex(inverseInputPermutation(b_in))
		#send to server and get a_out and b_out
		str_in = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/des"%(a)
		file1.write(str_in)
		file1.write("\n")
		a_out = json.loads(subprocess.check_output(str_in,shell=True).decode())['ciphertext']
		file1.write(str(a_out))
		file1.write("\n")
		str_in = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/des"%(b)
		file1.write(str_in)
		file1.write("\n")
		b_out = json.loads(subprocess.check_output(str_in,shell=True).decode())['ciphertext']
		file1.write(str(b_out))
		file1.write("\n")
		# print(a_out)
		a_out = inverseOutputPermutation(convertBinary(a_out))
		b_out = inverseOutputPermutation(convertBinary(b_out))

		L0_a = a_in[:32]
		R0_a = a_in[32:]
		L3_a = a_out[:32]
		R3_a = a_out[32:]

		L0_b = b_in[:32]
		R0_b = b_in[32:]
		L3_b = b_out[:32]
		R3_b = b_out[32:]

		R2_a = L3_a
		R2_b = L3_b

		R2_a_exp = expansion(R2_a)
		R2_b_exp = expansion(R2_b)
		R2_exp_xor = xor(R2_a_exp,R2_b_exp) #
		R3_xor = xor(R3_a,R3_b)

		ctr2+=1
		R2_a_exp = xor(R2_a_exp, key_3r)
		R2_b_exp = xor(R2_b_exp, key_3r)
		R2_a_sbox = Sbox(R2_a_exp)
		R2_b_sbox = Sbox(R2_b_exp)
		R2_a_sbox = permutation(R2_a_sbox)
		R2_b_sbox = permutation(R2_b_sbox)

		L2_a = xor(R3_a,R2_a_sbox)
		L2_b = xor(R3_b,R2_b_sbox)
		R1_a = L2_a
		R1_b = L2_b
		R1_a_exp = expansion(R1_a)
		R1_b_exp = expansion(R1_b)
		




		R1_exp_xor = xor(R1_a_exp,R1_b_exp) #
		R2_xor = xor(R2_a,R2_b)
		L1_xor = xor(R0_a,R0_b)
		R1_sbox_xor = xor(inversePermutation(R2_xor),inversePermutation(L1_xor)) #

		for i_2r in range(0,8):
			temp_keys_2r = []
			for j_2r in range(0,64):
				temp_a_2r = format(j_2r,'06b')
				temp_b_2r = xor(temp_a_2r, R1_exp_xor[6*i_2r:6*i_2r+6])
				temp_a_sbox_2r = sbox(temp_a_2r,i_2r)
				temp_b_sbox_2r = sbox(temp_b_2r,i_2r)
				if xor(temp_a_sbox_2r,temp_b_sbox_2r) == R1_sbox_xor[4*i_2r:4*i_2r+4]:
					key1_2r = xor(temp_a_2r,R1_a_exp[6*i_2r:6*i_2r+6])
					key2_2r = xor(temp_b_2r,R1_b_exp[6*i_2r:6*i_2r+6])
					temp_keys_2r.append(key1_2r)
					temp_keys_2r.append(key2_2r)
			# print(temp_keys_2r)
			poss_keys_2r[i_2r] = list(set(poss_keys_2r[i_2r])&set(temp_keys_2r))
			#print(poss_keys_2r)
		# print(poss_keys)
		flag_2r = True
		for i_2r in range(0,8):
			if(len(poss_keys_2r[i_2r])!=1):
				flag_2r = False
		# for i_2r in range(0,8):
		# 	if(len(poss_keys_2r[i_2r])!=2):
		# 		xor_in = "ghikhighghikhgst"
		# 		xor_in = convertBinary(xor_in)
		if(flag_2r == True):
			print("Round 3 Key recovered in #%d chosen plaintext attacks"%(2*ctr2))
			# print(poss_keys)
			K_2 = ''
			for i in range(0,8):
				K_2 += ''.join(poss_keys_2r[i])
			return K_2

# decrypting ciphertext with all the three keys
def decrypt(ciphertext, key_1r, key_2r, key_3r):
	text = inverseOutputPermutation(convertBinary(ciphertext))
	R3 = text[32:]
	L3 = text[:32]
	R2 = L3
	L2 = xor(permutation(Sbox(xor(expansion(R2),key_3r))),R3)
	R1 = L2
	L1 = xor(permutation(Sbox(xor(expansion(R1),key_2r))),R2)
	R0 = L1
	L0 = xor(permutation(Sbox(xor(expansion(R0),key_1r))),R1)
	res = ""
	res = L0 + R0
	res = convertHex(inverseInputPermutation(res))
	return res

# the main function
if __name__ == '__main__':
	#  Working properly
	# print(getkeybitsfromK3('010101011111110010001010010000101100111110011001'))
	password_encrypt = "orrpgnijqipsqpjmomplfijifgskmhpj"
	K_3 = breakDES3()
	# Now we have the K_3 key
	K = getkeybitsfromK3(K_3)
	K_2 = round2key(K_3)
	K_dash = getkeybitsfromK2(K_2)
	K = ''.join(K)
	K_dash = ''.join(K_dash)
	# print(K)
	# print(K_dash)
	# exit()
	K_new = []
	unknown_bits = 0
	for i in range(0,64):
		if(K[i] == K_dash[i]):
			if(K[i] == 'x'):
				unknown_bits += 1
				K_new.append('x')
			else:
				K_new.append(K[i])
		else:
			if(K[i] != 'x' and K_dash[i] != 'x'):
				print("Probably, this is not 3 round DES %s %s %d"%(K[i],K_dash[i],i))
			elif(K[i] == 'x'):
				K_new.append(K_dash[i])
			else:
				K_new.append(K[i])
	K_new = ''.join(K_new)
	print(K_new)
	print("The key is of this format. Still %d bits are unknown"%(unknown_bits))
	print("Now we find possibilities of decryption of passwords")
	pass_poss = dict()
	for i in range(0,256):
		bin_i = format(i,'08b')
		# print(bin_i,bin_i[7])
		ctr = 0
		ctr_i = 0
		newK = []
		for iters in range(0,64):
			if(K_new[iters] == 'x'):
				newK.append(bin_i[ctr_i])
				# print(iters,ctr_i)
				ctr_i += 1
			else:
				newK.append(K_new[iters])
		newK = ''.join(newK)
		K1, K2, K3 = getK1K2K3(newK)
		plain_text_1 = decrypt(password_encrypt[:16],K1,K2,K3)
		plain_text_2 = decrypt(password_encrypt[16:],K1,K2,K3)
		if((plain_text_1 + plain_text_2) not in pass_poss):
			pass_poss[(plain_text_1 + plain_text_2)] = True

	for poss in pass_poss:
		print(poss)
		print("Checking if this is the answer ....")
		str_in = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/des"%(poss)
		file1.write(str_in)
		file1.write("\n")
		a_out = json.loads(subprocess.check_output(str_in,shell=True).decode())
		file1.write(str(a_out))
		file1.write("\n")
		if(a_out['success']==True):
			print("Voila! The level is cleared:")
			print("Password : %s"%(poss))

