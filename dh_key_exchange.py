from utils import modular_exponentiation, is_prime, generate_prime
import random
import socket
import struct




       
def compute_shared_secret(private_key, peer_public_key, p):
    return modular_exponentiation(peer_public_key, private_key, p)
def generate_dh_keys():
    return

def start_dh_exchange():
    # Étape 1 : Génération de vos clés DH




    p = generate_prime(255)  # Generate a large prime number

    #p-1 = 2q 
    #print(f"Le nombre premier p est {bin(p)}.")
    print(f"Le nombre premier p est {p.bit_length()}.")
    generatorFound = False
    g = 2  # Start at 2
    while not generatorFound:
        if pow(g, 2, p) != 1 and pow(g, (p-1)//2, p) != 1:
            generatorFound = True
        else:
            g += 1
    print(f"[INFO] Vos paramètres DH : p = {p}, g = {g}")
    a = random.randint(1, p - 1)  # Clé client
    print(f"[INFO] Votre clé privée : {a}")

    A = pow(g, a, p)  # Clé client publique
    print(f"[INFO] Votre clé publique : {A}")
    

    # Close the connection
    return A, a, p, g

