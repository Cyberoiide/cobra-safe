from cobra import cobra_encrypt_ecb, cobra_decrypt_ecb

def test_cobra_ecb():
    original_text = "salut je suis amy et je test ça pour la premiere fois"
    session_key = b"1234567890abcdef"  # 16 octets => 128 bits

    print("[DEBUG] Texte original :", original_text)
    plaintext_bytes = original_text.encode('utf-8')

    # Chiffrer
    ciphertext = cobra_encrypt_ecb(plaintext_bytes, session_key)
    print("[DEBUG] ciphertext hex =", ciphertext.hex())

    # Déchiffrer
    decrypted_bytes = cobra_decrypt_ecb(ciphertext, session_key)
    decrypted_text = decrypted_bytes.decode('utf-8')

    print("[DEBUG] Texte déchiffré :", decrypted_text)

if __name__ == "__main__":
    test_cobra_ecb()
