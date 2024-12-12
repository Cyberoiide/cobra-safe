from utils import modular_exponentiation
import random
import socket
import struct

def is_prime_rabin_miller(n, k=5):
    """
    Vérifie si un nombre est premier en utilisant le test de primalité de Rabin-Miller.

    :param n: Nombre à vérifier
    :param k: Nombre d'itérations du test (plus élevé, plus précis)
    :return: True si n est probablement premier, sinon False
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Écrire n-1 comme 2^r * d avec d impair
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Effectuer k tests
    for _ in range(k):
        a = random.randint(2, n - 2)  # Choisir un nombre aléatoire dans [2, n-2]
        x = pow(a, d, n)  # Calculer (a^d) % n
        if x == 1 or x == n - 1:
            continue

        # Vérifier si x reste congru à n-1 pour un des 2^r * d
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True



       
def compute_shared_secret(private_key, peer_public_key, p):
    return modular_exponentiation(peer_public_key, private_key, p)
def generate_dh_keys():
    return

def start_dh_exchange():
    # Étape 1 : Génération de vos clés DH




    primeFound = False
    while not primeFound:
        nombre = random.randint(2**191, 2**255) 
        if is_prime_rabin_miller(nombre) :
            if is_prime_rabin_miller(2*nombre+1) :
                p = 2*nombre+1
                primeFound = True

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

