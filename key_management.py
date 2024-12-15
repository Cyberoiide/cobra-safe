from utils import generate_large_prime, modular_exponentiation, generate_prime
from kdf import derive_key
import os
import random

def create_user(username, password):
    p = generate_large_prime()  # Generate a large prime number
    generatorFound = False
    g = 2  # Start at 2
    while not generatorFound:
        if pow(g, 2, p) != 1 and pow(g, (p-1)//2, p) != 1:
            generatorFound = True
        else:
            g += 1
    derived_key = int(derive_key(password), 16)
    s = derived_key % (p - 1)
    public_key = modular_exponentiation(g, s, p)

    # Save keys
    os.makedirs(f"users/{username}", exist_ok=True)
    with open(f"users/{username}/public_key.txt", "w") as pub_file:
        pub_file.write(f"{p}\n{g}\n{public_key}\n")
    with open(f"users/{username}/private_key.txt", "w") as priv_file:
        priv_file.write(f"{s}\n")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def create_rsa(username,bits=256):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    os.makedirs(f"users/{username}", exist_ok=True)
    with open(f"users/{username}/rsa_private_key.txt", "w") as priv_file:
        priv_file.write(f"{d}\n{n}\n")
    return (e, n)