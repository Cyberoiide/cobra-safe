import random
from utils import modular_exponentiation
from kdf import derive_key  # Importer la fonction de dérivation de clé

def verify_certificate(username):
    print(f"[INFO] Vérification du certificat pour {username}.")
    # Simuler une signature ou un tampon par une autorité
    return True  # Supposons que tous les certificats sont valides pour cette simulation


def authenticate_with_schnorr(username, password):
    try:
        # Charger les clés publiques et privées
        with open(f"users/{username}/public_key.txt", "r") as pub_file:
            p = int(pub_file.readline())
            g = int(pub_file.readline())
            public_key = int(pub_file.readline())
        with open(f"users/{username}/private_key.txt", "r") as priv_file:
            saved_private_key = int(priv_file.readline())
        print(f"[INFO] Clés chargées : p = {p}, g = {g}, public_key = {public_key}")
    except FileNotFoundError:
        print("[ERROR] Utilisateur introuvable.")
        return False

    # Dériver la clé privée à partir du mot de passe
    derived_key = int(derive_key(password), 16)
    s = derived_key % (p - 1)  # La clé privée dérivée du mot de passe
    print(f"[DEBUG] Clé privée dérivée (authentification) : {s}")
    print(f"[DEBUG] Clé privée sauvegardée (création) : {saved_private_key}")

    # Vérifier que la clé dérivée correspond à la clé privée sauvegardée
    if s != saved_private_key:
        print("[ERROR] Mot de passe incorrect.")
        return False

    # Étape 1 : Générer M
    m = random.randint(1, p - 1)
    M = modular_exponentiation(g, m, p)
    print(f"[DEBUG] M calculé : {M}")

    # Étape 2 : Serveur génère le challenge r
    r = random.randint(1, p - 1)
    print(f"[DEBUG] Challenge r : {r}")

    # Étape 3 : Calcul de la preuve
    proof = (m - r * s) % (p - 1)
    if proof < 0:
        proof += (p - 1)
    print(f"[DEBUG] Preuve calculée : {proof}")

    # Étape 4 : Vérification
    left = M
    right = (modular_exponentiation(g, proof, p) * modular_exponentiation(public_key, r, p)) % p
    print(f"[DEBUG] left = {left}, right = {right}")

    if left == right:
        print("[SUCCESS] Authentification réussie.")
        return True
    else:
        print("[FAILURE] Échec de l'authentification.")
        return False
