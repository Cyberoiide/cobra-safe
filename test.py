def encrypt(public_key, plaintext):
    e, n = public_key
    return [(ord(char) ** e) % n for char in plaintext]

def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr((char ** d) % n) for char in ciphertext])

if __name__ == "__main__":
    # Prompt for keys
    username = "clem"
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
    
    # Input plaintext
    plaintext = input("Enter a message to encrypt: ")

    # Encrypt the plaintext
    ciphertext = encrypt(public_key, plaintext)
    print(f"Ciphertext: {ciphertext}")

    # Decrypt the ciphertext
    decrypted_message = decrypt(saved_private_key, ciphertext)
    print(f"Decrypted Message: {decrypted_message}")
