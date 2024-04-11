
def shift_cipher(plain_text, shift, kind='encrypt'): 
    if kind == 'decrypt':
        shift *= -1
        
    cipher_text = ""
    for ch in plain_text:
        new_letter = ord(ch) + shift
        last_letter = chr(new_letter)
        cipher_text += last_letter
            
    return cipher_text


p = int(input())
g = int(input())
a = int(input())
b = int(input())
M = input()

m1 = (g ** a) % p
m2 = (g ** b) % p 

secret_key1 = (m1 ** b) % p
secret_key2 = (m2 ** a) % p

if secret_key1 != secret_key2:
    print('something is wrong!')
    exit()    
    
secret_key = secret_key1

# DEBUG
# print(secret_key)

m3 = shift_cipher(M, secret_key)
m4 = shift_cipher(m3, secret_key, kind='decrypt')

print(m1)
print(m2)
print(m3)
print(m4)
