# DSA Algorithm

- Sender Side:
    - ciphertext = Encrypt([message, h=known_hash_func(message)], private_key)
- Reciever Side:
    - [message, h] = Decrypt(ciphertext, public_key)
    - if h == known_hash_func(message): 
        return True
      else:
        return False

- Signature Generation:
    - input: message, private_key, random_number, dsa_parameters
    - output: signature
- Signature Verification:
    - input: message, sender's public_key, signature, dsa_parameters
    - output: {True, False}

- $p$ - prime number and $2^{L-1} \lt p \lt 2^{L}$
- $q$ - prime divisor of $p-1$ that is also prime.
- $g$(global component) - $g=h^{\frac{p-1}{q}}\mod p$ - ($1 \lt h \lt p-1$)
- $y = g^x \mod p$
- Sender's public_key: $(p, q, g, y)$

- Sender's private_key: $x$ - random number - $(0 \lt x \lt q)$

- $k$ - secret number - $(0 \lt k \lt q)$
- $r = (g^k \mod p) \mod q$
- $s = [k^{-1}(H(M)+x.r)] \mod q$
- Sender's Signature: $(r, s)$

- $v = [(g^{u_1}y^{u_2}) \mod p] \mod q$
- $w = (s')^{-1} \mod q$
- $u_1 = [H(M').w] \mod q$
- $u_2 = [r'.w] \mod q$
- $v = r'$
- $'$ means reciever side.

- if random number in signature generation reused private_key can be found!!!
- private_key is all thing so when it is found by someone it is catastrophe!
- rfc6979: generate random_number based on message deterministicly
    - same random_number show same messages 

- digital signature is reverse of encryption/decryption
    - sign by private_key
    - verify by public_key
    
    - then everyone can verify message sender identity