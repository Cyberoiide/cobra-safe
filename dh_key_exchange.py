# projects/gs15_projet_cobra/dh_key_exchange.py

import os

def generate_random_symmetric_key(key_size=32):
    """
    Génère une clé symétrique aléatoire pour tester COBRA.
    :param key_size: Taille de la clé en octets (32 = 256 bits par défaut).
    :return: Clé symétrique aléatoire sous forme de bytes.
    """
    key = os.urandom(key_size)
    print(f"[DEBUG] Clé symétrique générée aléatoirement : {key.hex()}")
    return key

def start_dh_exchange():
    """
    Remplace temporairement l'échange Diffie-Hellman par une génération aléatoire
    de clé symétrique pour tester l'implémentation de COBRA.
    :return: Clé symétrique aléatoire (pour tester).
    """
    print("[INFO] Simulation de l'échange Diffie-Hellman désactivée.")
    print("[INFO] Génération d'une clé symétrique aléatoire pour les tests.")
    return generate_random_symmetric_key()

if __name__ == "__main__":
    # Test autonome
    test_key = start_dh_exchange()
    print(f"[TEST] Clé générée : {test_key.hex()}")
