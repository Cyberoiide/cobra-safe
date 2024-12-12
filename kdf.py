import hashlib

def derive_key(password):
    key = password.encode()
    for _ in range(10000):
        key = hashlib.sha256(key).digest()
    derived_key = key.hex()
    print(f"[DEBUG] Clé dérivée pour le mot de passe '{password}': {derived_key}")
    return derived_key
