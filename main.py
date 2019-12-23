import random  
from Crypto.Util import number
from egcd import egcd
  
# Generating large random numbers 
def gen_key(q): 
  
    key = random.randint(3, q - 2) 
    while number.GCD(q, key) != 1: 
        key = random.randint(3, q - 2) 
  
    return key 
  
def gen_hidden_msg(p):
    M = random.randint(3, p - 2)
    while number.GCD(p, M) != 1 or number.GCD(p-1, M) != 1:
        M = random.randint(3, p - 2)
    return M

def gen_msg(hidden_M, p):
    M = random.randint(3, p - 2)
    while number.GCD(p, M) != 1 or number.GCD(M, hidden_M) != 1:
        M = random.randint(3, p - 2)
    return M


def sign(p, g, x, y, M):
    k = gen_key(p - 1)
    a = pow(g, k, p)

    k_inverse = number.inverse(k, p - 1)

    b = ((M - x * a) * k_inverse) % (p-1)

    return a, b

def check_sign(p, g, y, a, b, M):
    return (pow(y, a, p) * pow(a, b, p)) % p == pow(g, M, p)

def sign_with_hidden_msg(p, g, x, hidden_M):
    a = pow(g, hidden_M, p)

    hidden_M_inverse = number.inverse(hidden_M, p-1)

    while True:
        M = gen_msg(hidden_M, p)
        b =  ((M - x * a) * hidden_M_inverse) % (p-1)
        b_inverse = number.inverse(b, p - 1)
        if hidden_M == ((M - x*a) * b_inverse) % (p-1):
            break

    return a, b, M


# Driver code 
def main(): 
    p = number.getPrime(10)
    g = random.randint(2, p - 1)
    x = random.randint(2, p - 1)
    
    M = random.randint(2, p - 1)
    y = pow(g, x, p)

    a, b = sign(p, g, x, y, M)

    print("Yolter got message from message: ", M)
    print("Sign: ", check_sign(p, g, y, a, b, M))


    print("=========================================")
    print("Alice is trying send hidden message...")
    hidden_M = gen_hidden_msg(p)
    y = pow(g, x, p)

    a, b, M = sign_with_hidden_msg(p, g, x, hidden_M)

    print("Yolter got message from message: ", M)
    print("Sign: ", check_sign(p, g, y, a, b, M))


    print("Bob is trying get hidden message...")
    tmp = (M - x*a) % (p - 1)
    bob_recieved = (number.inverse(b, p - 1) * tmp) % (p - 1)
    print("hidden_M    :", hidden_M)
    print("bob recieved:",bob_recieved)


if __name__ == '__main__': 
    main() 

