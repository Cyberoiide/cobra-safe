from hash import generate_hash

def derive_key(password):
    key = password.encode()
    for _ in range(10000):
        key = generate_hash(key)
    derived_key = key.hex()
    print(f"[DEBUG] Clé dérivée pour le mot de passe '{password}': {derived_key}")
    return derived_key
