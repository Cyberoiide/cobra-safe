import random

def dh_exchange(A, p, g):
    # Générer la clé privée du serveur
    b = random.randint(1, p - 1)  # Clé client
    print(f"[INFO] Votre clé privée : {b}")
    B = pow(g, b, p)  # Clé serveur publique
    print(f"[INFO] Votre clé publique : {B}")
    session_key = pow(A,b,p)
    print(f"[INFO] Clé de séssion dh: {session_key}")

    return session_key, B