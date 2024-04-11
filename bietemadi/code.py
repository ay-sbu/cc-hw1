import random
from math import gcd as bltin_gcd

###################################################### global
MAX = 1000000007

def hash(message):
    global MAX
    res = 1
    for c in message:
        res = res * ord(c) % MAX
    return res

def coprime2(a, b):
    return bltin_gcd(a, b) == 1

def mod_inverse(n: int, mod: int):
    return pow(n, -1, mod)

###################################################### sender
def calculate_g(h, p, q):
    if (p-1) % q != 0:
        print('q should be divisor of (p-1)')
        exit(1)
    return (h**((p-1) // q)) % p

def calculate_y(g, x, p):
    return g**x % p

def calculate_r(g, k, p, q):
    return ((g**k) % p) % q

def calculate_s(k, m, x, r, q):
    return (mod_inverse(k, q) * (hash(m) + x*r)) % q

def sign(m, p, q, g, private_key):
    x = private_key


    k, r, s = 2, 1, 1
    while True:
        if coprime2(k, q):
            # print('DEBUG g k p q', g, k, p, q)
            r = calculate_r(g, k, p, q)
            s = calculate_s(k, m, x, r, q)
            # print('DEBUG s r', s, r)
            
            if r != 0 and s != 0:
                break
        
        # k = random.randint(1, q-1)
        k += 1

    print(k)
    print(r)
    print(s)

    return (r, s)

###################################################### receiver
def calculate_w(s_prim, q):
    return mod_inverse(s_prim, q)

def calculate_u1(m_prim, w, q):
    return (hash(m_prim) * w) % q

def calculate_u2(r_prim, w, q):
    return (r_prim * w) % q

def calculate_v(g, u1, y, u2, p, q):
    return (((g**u1)*(y**u2)) % p) % q

def verify(signature, tampered_message, p, q, g, public_key) -> bool:
    r_prim = signature[0]
    s_prim = signature[1]
    m_prim = tampered_message
    y = public_key

    w = calculate_w(s_prim, q)
    print(w)

    u1 = calculate_u1(m_prim, w, q)
    print(u1)

    u2 = calculate_u2(r_prim, w, q)
    print(u2)

    v = calculate_v(g, u1, y, u2, p, q)
    print(v)

    if v == r_prim:
        return True
    else:
        return False

###################################################### main
m = input()
m_prim = input()        # prim everywhere means receiver side

p = 6700417
print(p)

q = 17449
print(q)

h = 2

g = 1
while True:
    g = calculate_g(h, p, q)
    if g != 1:
        break
    
    h += 1

print(g)

x = 9
private_key = x
print(x)

y = calculate_y(g, x, p)
public_key = y
print(y)

sender_signature = sign(m, p, q, g, private_key)
# print('DEBUG sender_signature', sender_signature)

receiver_result = verify(sender_signature, m_prim, p, q, g, public_key)

print(receiver_result)




