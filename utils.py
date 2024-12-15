import random

def modular_exponentiation(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result



def is_prime(n, k=5):
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


def generate_prime(limit):
    primeFound = False
    while not primeFound:
        nombre = random.randint(2**191, 2**limit) 
        if is_prime(nombre) :
            if is_prime(2*nombre+1) :
                p = 2*nombre+1
                primeFound = True
    return p



def generate_large_prime(bits=1024):
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate

def display_message(msg):
    print(msg)
