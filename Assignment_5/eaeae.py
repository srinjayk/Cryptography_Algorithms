import subprocess
import json
import sys
import os
import random
from os import path
import binascii

# Defining some constants for GF(7)
# All elements of form a^b will be stored where a,b \in GF(7)
exp = [[] for i in range(128)]
io_dict = dict()
num_plain_texts = 0
# First we'll break the diagonal elements
import pyfinite.ffield as ffield
F = ffield.FField(7)

def addGF(p1,p2):
	# Assume both a and b are integers
	return p1^p2

def multGF(p1, p2):
	return F.Multiply(p1,p2)

def convertHex(list_p1):
	text = ""
	for p1 in list_p1:
		text += format(p1,'08b')
	temp1 = ""
	for i in range(0,len(text)//4):
		temp1 = temp1 + chr(ord('f')+int(8*int(text[i*4])+4*int(text[i*4+1])+2*int(text[i*4+2])+int(text[i*4+3])))
	return temp1

def convertVector(str_in):
	bin_str = ''.join(format(ord(i)-ord('f'), '0>4b') for i in str_in)
	out = []
	for i in range(0,64,8):
		out.append(int(bin_str[i:i+8],2))
		# print(int(bin_str[i:i+8],2))
	return out

def checkServer(str_in):
	'''
	input : "fffffffffg"
	output : {'ciphertext': [blah], 'success':[blah]}
	'''
	if(str_in in io_dict):
		return io_dict[str_in]
	else:
		to_send = "curl -H \"Content-Type: application/json\" --request POST --data \'{\"plaintext\": \"%s\", \"password\": \"7d1480a22895004ec4879c98dacc6d32\", \"teamname\": \"SchutzSAS\"}\' -k https://172.27.26.181:9998/eaeae"%(str_in)
		out = json.loads(subprocess.check_output(to_send,shell=True).decode())
		io_dict[str_in] = out
		return out

def convertBinary(text):
	return ''.join(format(ord(i)-ord('f'), '0>4b') for i in text)

def preprocess():
	for i in range(0,128):
		e = 1
		for j in range(0,128):
			exp[i].append(e)
			e = multGF(e,i)
			# print(e)
def evalSingleEAEAE(x, e, a):
	return exp[multGF(a,exp[multGF(a,exp[x][e])][e])][e]

def evalEAEAE(x,E,A):
	# EAEAE
	y = [0]*8
	for i in range(0,8):
		y[i] = exp[x[i]][E[i]]
		# print(y[i])
	AEx = [0]*8
	for i in range(0,8):
		AEx[i] = 0
		for j in range(0,8):
			AEx[i] ^= multGF(A[i][j],y[j])
	y = AEx.copy()
	# print(y)
	for i in range(0,8):
		y[i] = exp[y[i]][E[i]]
		# print(y[i])
	for i in range(0,8):
		AEx[i] = 0
		for j in range(0,8):
			AEx[i] ^= multGF(A[i][j],y[j])
	y = AEx.copy()
	# print(y)
	for i in range(0,8):
		# print(y[i])
		# print(y[i],E[i],exp[y[i]][E[i]])
		y[i] = exp[y[i]][E[i]]
	# print(y)
	del(AEx)
	return y

def attackDiagExp():
	# Attack diagonal
	pairs_poss = []
	for i in range(0,8):
		# Attack i^th bit
		attack_arr = [0]*8
		possible_pairs = [(i,j) for i in range(1,127) for j in range(1,127)]
		for byte_in in range(1,128):
			attack_arr[i] = byte_in
			byte_out = convertVector(checkServer(convertHex(attack_arr))['ciphertext'])[i]
			new_possible_pairs = []
			for pair in possible_pairs:
				d,e = pair
				if(evalSingleEAEAE(byte_in, e, d) == byte_out):
					new_possible_pairs.append((d,e))
			possible_pairs = list(set(possible_pairs)&set(new_possible_pairs))
		pairs_poss.append(possible_pairs)
	return pairs_poss

def attackAll(pairs_poss,tries=10):
	'''
	a_{i+j}{i} 0<i<8-j will be attacked
	'''
	# Now bruteforce
	# Attack second line
	exp_A = [[0]*8 for i in range(0,8)]
	exp_E = [1 for i in range(0,8)]
	for k in range(0,7):
		# a_{j+1}{j}
		j = 6-k
		A = [[0]*8 for i in range(0,8)]
		E = [1 for i in range(0,8)]
		x = [0 for i in range(0,8)]
		poss = []
		for a_j1j in range(1,128):
			for a_j1j1,e_j1 in pairs_poss[j+1]:
				for a_jj,e_j in pairs_poss[j]:
					ctr = 0
					flag = True
					while ctr < tries:
						ctr += 1
						x[j] = random.randint(1,127)
						A[j+1][j+1] = a_j1j1
						A[j][j] = a_jj
						A[j+1][j] = a_j1j
						E[j+1] = e_j1
						E[j] = e_j
						x_act = convertVector(checkServer(convertHex(x))['ciphertext'])
						x_exp = evalEAEAE(x,E,A)
						if(x_act[j+1] != x_exp[j+1]):
							flag = False
					if(flag == True):
						poss.append([a_j1j,a_j1j1,e_j1,a_jj,e_j])
		new_possible_pairs_j = []
		new_possible_pairs_j1 = []
		for elem in poss:
			new_possible_pairs_j.append((elem[3],elem[4]))
			new_possible_pairs_j1.append((elem[1],elem[2]))
		pairs_poss[j] = list(set(pairs_poss[j])&set(new_possible_pairs_j))
		pairs_poss[j+1] = list(set(pairs_poss[j+1])&set(new_possible_pairs_j1))
		if(len(poss) == 1):
			exp_A[j+1][j] = poss[0][0]
			exp_A[j+1][j+1] = poss[0][1]
			exp_A[j][j] = poss[0][3]
			exp_E[j+1] = poss[0][2]
			exp_E[j] = poss[0][4]
			# print(j)
		else:
			print("Alas")
	# print("E is recovered.")
	# At this stage E is completely broken
	for l in range(2,8):
		# Now attack all positions left
		# print(l)
		for k in range(0,8-l):
			j = 7-l-k
			corr_ele = 0
			# Attack a_{j+l}{j}
			A = exp_A.copy()
			x = [0 for i in range(0,8)]
			true_labels = 0
			for a_jlj in range(1,127):
				# print(a_jlj)
				ctr = 0
				flag = True
				while ctr < tries:
					ctr += 1
					x[j] = random.randint(1,127)
					A[j+l][j] = a_jlj
					x_act = convertVector(checkServer(convertHex(x))['ciphertext'])
					x_exp = evalEAEAE(x,exp_E,A)
					if(x_act[j+l] != x_exp[j+l]):
							flag = False
				if(flag == True):
					true_labels += 1
					corr_ele = a_jlj
			if(true_labels > 1):
				print("problems")
			else:
				exp_A[j+l][j] = corr_ele
			del(A)
	return exp_A, exp_E


def decryptPass(password_l,E,A):
	pass_v = convertVector(password_l)
	# print(pass_v)
	exp_x = [0]*8
	for j in range(0,8):
		x = exp_x.copy()
		for x_j in range(0,128):
			x[j] = x_j
			if(evalEAEAE(x,E,A)[:j+1]==pass_v[:j+1]):
				exp_x[j] = x_j
	return convertHex(exp_x)
	

if __name__ == '__main__':
	preprocess()
	# print(len(exp[57]))
	random.seed(100)
	if(path.isfile('f.json')):
		io_dict = json.load(open("f.json","r"))
	pairs_poss = attackDiagExp()
	num_plain_texts = len(io_dict.keys())
	# print(pairs_poss)
	A,E = attackAll(pairs_poss)
	print("E:",E)
	print("Matrix A is as follows")
	for i in range(0,8):
		print_str = ""
		for aij in A[i]:
			print_str+=str(aij)+"\t"
		print(print_str)
	password_encrypt = "ktirlqhtlqijmmhqmgkplijngrluiqlq"
	password = decryptPass(password_encrypt[0:16],E,A)+decryptPass(password_encrypt[16:],E,A)
	n = int(convertBinary(password),2)
	print("The password is ",n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
	print("Number of plaintext attacks",num_plain_texts)
	json.dump(io_dict,open("f.json","w"),indent=True)