from utils import modular_exponentiation
import random

def generate_dh_keys():
    # Define a large prime p and base g
    p = 23  # Example small prime for testing; replace with larger prime for production
    g = 5
    private_key = random.randint(1, p - 2)
    public_key = modular_exponentiation(g, private_key, p)
    return p, g, private_key, public_key

def compute_shared_secret(private_key, peer_public_key, p):
    return modular_exponentiation(peer_public_key, private_key, p)

def start_dh_exchange():
    # Étape 1 : Génération de vos clés DH
    p, g, private_key, public_key = generate_dh_keys()
    print(f"[INFO] Vos paramètres DH : p = {p}, g = {g}")
    print(f"[INFO] Votre clé publique : {public_key}")

    # Simuler la clé publique d'un pair (normalement reçue via réseau)
    peer_public_key = random.randint(1, p - 1)  # Simulation
    print(f"[INFO] Clé publique reçue du pair : {peer_public_key}")

    # Étape 2 : Calcul du secret partagé
    shared_secret = compute_shared_secret(private_key, peer_public_key, p)
    print(f"[INFO] Secret partagé calculé : {shared_secret}")
    return shared_secret

