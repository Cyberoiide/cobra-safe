from utils import generate_large_prime, modular_exponentiation
from kdf import derive_key
import os

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
