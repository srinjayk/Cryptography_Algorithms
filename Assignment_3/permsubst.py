import sys
import math
import subprocess

str2 = None
n = 0
m = 0
def next_permutation(a):
    '''
    return True => More permutation to follow
    return False => No more permutation to follow 
    '''
    i = len(a) - 2
    while not (i < 0 or a[i] < a[i+1]):
        i -= 1
    if i < 0:
        return False
    j = len(a) - 1
    while not (a[j] > a[i]):
        j -= 1
    a[i], a[j] = a[j], a[i]        # swap
    a[i+1:] = reversed(a[i+1:])    # reverse elements from position i+1 till the end of the sequence
    return True

def replace(str1,a):
    global str2,m,n
    # Assume a stores the permutation
    assert(n%m == 0)
    iters = n//m
    temp = list(str1)
    new = list()
    for i in range(0,iters):
        start = m * i
        new += [temp[start+i] for i in a] 
    # print(''.join(new))
    new1 = list()
    j = 0
    for i in range(0,len(str2)):
        if(str2[i]==' ' or str2[i]=='.' or str2[i]==':' or str2[i]==',' or str2[i] == '!' or str2[i] == '_'):
            new1.append(str2[i])
        else:
            new1.append(new[j])
            j+=1
    return ''.join(new1)

def map_elements(str1,mapping):
    global str2,n
    temp = []
    str_list = list(str1)
    mapping_list = list(mapping)
    for i in range(0,len(str_list)):
        if(ord(str_list[i])>=97 and ord(str_list[i])<=122):
            temp.append(mapping_list[ord(str_list[i])-97])
    return ''.join(temp)

def break_cipher():
    global str2,n,m
    if(len(sys.argv) != 3):
        print("Input format : python3 permsubst.py break_cipher <expected_length_key>")
        exit(1)
    f = open("cipherText.txt", "r")
    str1 = f.read()
    str2 = list(str1)
    # Remove whitespaces/ bogus characters
    str1 = str1.replace(" ","")
    str1 = str1.replace(",","")
    str1 = str1.replace(".","")
    str1 = str1.replace("!","")
    str1 = str1.replace(":","")
    str1 = str1.replace("_","")

    n = len(str1)
    # Key length in sys.argv[1]
    m = int(sys.argv[2])
    assert(n%m == 0)
    # Trivial permutation
    a = [i for i in range(0,m)]
    # Compiles haskell file
    subprocess.check_output("cd cipher_breaker/ && ghc substcipher.hs && cd ../",shell = True)
    flag = True
    best = 0
    best_str = ""
    best_a = a
    print_after = 10
    iters = 0
    while(flag == True):
        newstr = replace(str1,a)
        with open('cipher_breaker/cipher.txt', 'w') as filetowrite:
            filetowrite.write(newstr)
        out = subprocess.check_output("cd cipher_breaker/ && ./substcipher && cd ../",shell = True).decode("utf-8") 
        results = int(out.split('\n')[1])
        if(results > best):
            best = results
            best_str = out.split('\n')[2]
            best_a = [a[i] for i in range(0,len(a))]
        iters += 1
        if((iters%print_after) == 0):
            print("After %d iters best score : %d"%(iters,best))
            print(best_str)
            print('\n')
        flag = next_permutation(a)
        # exit(0)
    print("After %d iters best score : %d"%(iters,best))
    print(best_str)
    print('\n')
    print(best_a)


def solve():
    global str2,n, m
    f = open("cipherText.txt", "r")
    str1 = f.read()
    str2 = list(str1)
    # Remove whitespaces/ bogus characters
    str1 = str1.replace(" ","")
    str1 = str1.replace(",","")
    str1 = str1.replace(".","")
    str1 = str1.replace("!","")
    str1 = str1.replace(":","")
    str1 = str1.replace("_","")

    n = len(str1)
    a = [1, 3, 4, 0, 2]
    m = len(a)
    mapping = "gpahtrfjkxscuqobdvzeilnywm"
    new_str = map_elements(str1,mapping)
    # print(new_str)
    print(replace(new_str,a))

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        break_cipher()
    else:
        solve()