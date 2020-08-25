import binascii

# Constants Provided
N = 84364443735725034864402554533826279174703893439763343343863260342756678609216895093779263028809246505955647572176682669445270008816481771701417554768871285020442403001649254405058303439906229201909599348669565697534331652019516409514800265887388539283381053937433496994442146419682027649079704982600857517093
C = 58851190819355714547275899558441715663746139847246075619270745338657007055698378740637742775361768899700888858087050662614318305443064448898026503556757610342938490741361643696285051867260278567896991927351964557374977619644763633229896668511752432222528159214013173319855645351619393871433455550581741643299
e = 5

from math import *

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def multiply(p1,p2):
    '''
    Multiply two given polynomials p1 and p2
    Please ensure that the given degree should be the
    length of the array being used
    4x^2 + 2x + 1 = [4,2,1]
    '''
    deg1 = len(p1)
    deg2 = len(p2)
    deg = deg1 + deg2 - 1
    poly = [0]*deg
    for i in range(deg1):
        for j in range(deg2):
            poly[i+j] += p1[i]*p2[j]
    return poly

def scale(p1,alpha):
    '''
    Scales polynomial p(x) by p(alpha x)
    This will be used while scaling the coefficients
    '''
    deg1 = len(p1) - 1
    return [p1[i]*(alpha**(deg1-i)) for i in range(len(p1))]


def eval_poly(p,x):
    deg1 = len(p) - 1
    return sum([x**(deg1-i)*p[i] for i in range(len(p))])

def search_roots(p,hi = 2**80, lo = 0):
    max_iter=0
    while max_iter < 200:
        mid = (lo + hi)//2
        val = eval_poly(p,mid)
        if val == 0:
            return mid
        # Now check signs
        val1 = eval_poly(p,hi)
        val2 = eval_poly(p,lo)
        if val1==0:
            return hi
        elif val2==0:
            return lo
        elif eval_poly(p,hi)*val > 0:
            hi = mid
        else:
            lo = mid
        max_iter += 1
    return None

degree = e #Same as the exponent
scale_factor = int(N**0.1) #Any large value < 0.2 should do
# print(scale_factor)

base = "This door has RSA encryption with exponent 5 and the password is ".encode('UTF-8')
base = int(binascii.hexlify(base),16)<<72

poly = [1%N,(5*(base))%N,(10*(base**2))%N,(10*base**3)%N,(5*base**4)%N,((base**5)-C)%N] #The polynomial under investigation

basis_poly = [] # Make lattice of 10 polynomials
for i in range(2):
        for j in range(5):
            p1 = [0]*5
            p1[-j-1] = scale_factor**j
            p2 = [0]*6
            p2[-1] = N**(2-i)
            p_temp = multiply(p1,p2)
            if i > 0:
                p_dash =  scale(poly,scale_factor)
                p_temp = multiply(p_temp[-5:],p_dash)
            basis_poly.append(p_temp)
# print(basis_poly)

basis_matrix = Matrix(ZZ, 10) # Init a 10x10 matrix


# Changing format
for i in range(10):
    for j in range(10):
        basis_matrix[i,j] = basis_poly[i][9-j]
# print(basis_matrix[0])

# fpylll implementation of LLL
# opylll fails because of high coefficients
basis_matrix = basis_matrix.LLL()
# The smallest LLL factor is in 1st row

shortest_lattice = basis_matrix[0]
# print(shortest_lattice)

root = search_roots([shortest_lattice[9 - i]/scale_factor**(9 - i) for i in range(10)])
print('Password = ',int2bytes(root).decode('UTF-8'))