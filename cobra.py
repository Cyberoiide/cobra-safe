# /projects/gs15_projet_cobra/cobra.py

import random
import os

def serpent_sbox(input_value, sbox_number):
    if not (0 <= input_value < 16):
        raise ValueError("Input value must be a 4-bit integer (0-15).")
    if not (0 <= sbox_number <= 7):
        raise ValueError("S-box number must be between 0 and 7.")

    # Define the Serpent S-boxes
    sboxes = [
        [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],  # S-box 0
        [15, 12, 2, 7, 9, 0, 5, 10, 11, 14, 6, 13, 1, 8, 4, 3],   # S-box 1
        [8, 6, 7, 9, 3, 12, 10, 15, 2, 4, 5, 0, 11, 14, 1, 13],  # S-box 2
        [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],  # S-box 3
        [13, 3, 11, 0, 10, 6, 5, 12, 1, 14, 4, 7, 15, 9, 8, 2], # Inverse S-box 0
        [5, 12, 2, 15, 14, 6, 10, 3, 13, 4, 7, 8, 1, 11, 9, 0], # Inverse S-box 1
        [11, 14, 8, 4, 9, 10, 1, 2, 0, 3, 6, 12, 5, 15, 13, 7], # Inverse S-box 2
        [0, 9, 10, 7, 11, 14, 6, 13, 3, 5, 12, 2, 4, 8, 15, 1]   # Inverse S-box 3
    ]
    
    # Perform the substitution
    return sboxes[sbox_number][input_value]

def substitution(block, sbox_index):
    #Apply S-box substitution to a 128-bit block.
    substituted = 0
    for i in range(32):  # 32 4-bit chunks
        nibble = (block >> (4 * i)) & 0xF
        substituted |= (serpent_sbox(nibble, sbox_index) << (4 * i))
    return substituted

def reverse_substitution(block, sbox_index):
    # Apply inverse S-box substitution to a 128-bit block.
    restored = 0
    for i in range(32):  # 32 4-bit chunks
        nibble = (block >> (4 * i)) & 0xF
        restored |= (serpent_sbox(nibble, sbox_index) << (4 * i))
    return restored



def function_in_feistel(R):
    R_blocks = [(R >> (j * 8)) & 0xFF for j in range(8)]
    Z_blocks = []
    for byte in R_blocks:
        reversed_bits = int(f'{byte:08b}'[::-1], 2)
        try:
            f_value = pow((reversed_bits + 1), -1, 257)  # f(x) = ((x+1)^-1 mod 257)
        except ValueError:
            f_value = 0  # Gestion des cas non inversibles
        Z_blocks.append(f_value)

    Z = sum((Z_blocks[j] << (8 * j)) for j in range(8))
    
    perm = [41, 1, 63, 17, 51, 13, 2, 39, 60, 40, 55, 30, 34, 54, 43, 5, 53, 4, 26, 27, 58, 9, 44, 45, 57, 29, 16, 0, 31, 14, 11, 25, 15, 24, 48, 23, 20, 46, 7, 8, 37, 22, 35, 36, 12, 21, 10, 32, 50, 49, 18, 61, 42, 38, 52, 6, 33, 56, 62, 47, 28, 59, 3, 19]
    Z_permuted = int(''.join(f'{Z:064b}'[p] for p in perm), 2)
    
    R_block_F = [(Z_permuted >> (j * 8)) & 0xFF for j in range(8)]
    #print(R_block_F)
    R_random = []
    for seed in R_block_F:
        random.seed(seed)  # Set the seed
        random_value = random.randint(0, 255)  # Generate a random 8-bit value
        R_random.append(random_value)
    
    #print(R_random)
    R_random_g = sum((R_random[j] << (8 * j)) for j in range(8))

    return R_random_g

def feistel(block, key):
    """
    A custom Feistel function for the cipher.
    
    Parameters:
        block (int): A 128-bit integer.
        key (int): A 128-bit key.
        
    Returns:
        int: The transformed block.
    """
    #L, R = int(block[:64], 2), int(block[64:], 2)
    L, R = (block >> 64) & 0xFFFFFFFFFFFFFFFF, block & 0xFFFFFFFFFFFFFFFF

    L_list = []
    R_list = []

    rounds = 3 
    for i in range(rounds):
        #Kn = keys[i]

        L_list.append(R)
        
        
        #print("avant fct",hex(R)) 
        R_random_g = function_in_feistel(R)
        key = key & 0xFFFFFFFFFFFFFFFF
        Final_Z = key ^ R_random_g
        
        R1 = L ^ Final_Z
        R_list.append(R1)
        R = R_list[i]
        L = L_list[i]

    

    block_return= ((L << 64) | R)
    return block_return

def reverse_feistel(block, key):
    L, R = (block >> 64) & 0xFFFFFFFFFFFFFFFF, block & 0xFFFFFFFFFFFFFFFF
    L_list = []
    R_list = []
    rounds = 3 
    for i in range(rounds):
        
        #print(hex(R))
        R_list.append(L)

        
        R_random_g = function_in_feistel(L)
        key = key & 0xFFFFFFFFFFFFFFFF
        Final_Z = key ^ R_random_g
        
        L1 = R ^ Final_Z
        L_list.append(L1)
        R = R_list[i]
        L = L_list[i]
    
    block_return= ((L << 64) | R)
    return block_return



def rotate_left(value, shift, bits=32):
    """Perform a left bitwise rotation on x by n positions."""
    rotated = ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF
    return rotated

def rotate_right(value, shift, bits=32):
    """Perform a right bitwise rotation on x by n positions."""
    rotated = ((value >> shift) | (value << (bits - shift))) & 0xFFFFFFFF
    return rotated

def transfo_lineaire(text):
    A,B,C,D = (text >> 96) & 0xFFFFFFFF, (text >> 64) & 0xFFFFFFFF, (text >> 32) & 0xFFFFFFFF, text & 0xFFFFFFFF
    A = rotate_left(A, 13)
    C = rotate_left(C, 3)
    B = B ^ A ^ C
    D = D ^ C ^ rotate_left(A,3)
    B = rotate_left(B, 1)
    D = rotate_left(D, 7)
    A = A ^ B ^ D
    C = C ^ D ^ rotate_left(B,7)
    A = rotate_left(A, 5)
    C = rotate_left(C, 22)
    return (A << 96) | (B << 64) | (C << 32) | D

def reverse_transfo_lineaire(text):
    A,B,C,D = (text >> 96) & 0xFFFFFFFF, (text >> 64) & 0xFFFFFFFF, (text >> 32) & 0xFFFFFFFF, text & 0xFFFFFFFF

    C = rotate_right(C, 22)
    A = rotate_right(A, 5)
    C = C ^ D ^ rotate_left(B,7)
    A = A ^ B ^ D
    D = rotate_right(D, 7)
    B = rotate_right(B, 1)
    D = D ^ C ^ rotate_left(A,3)
    B = B ^ A ^ C
    C = rotate_right(C, 3)
    A = rotate_right(A, 13)
    return (A << 96) | (B << 64) | (C << 32) | D



def key_expansion(key, rounds=32):
    """
    Expansions des clés pour l'algorithme Serpent.
    
    :param key: Clé d'entrée (bytes), de taille 128, 192 ou 256 bits.
    :param rounds: Nombre de tours (par défaut 32).
    :return: Liste des sous-clés générées (132 blocs de 32 bits).
    """
    # Étape 1 : Initialisation de la clé
    key = key.ljust(32, b'\x00')  # Complète avec des zéros à droite pour obtenir 32 octets
    blocks = []  # Contient les 8 blocs de 32 bits
    for i in range(8):  # Diviser en 8 blocs
        block = int.from_bytes(key[i * 4:(i + 1) * 4], byteorder='big')
        blocks.append(block)
        

    # Étape 2 : Itérations de l’expansion de clé :
    sub_keys = blocks[:]
    yo= sub_keys
    phi = 0x9E3779B9  # Nombre d'or 
    total_keys = 132  # 132 sous-clés de 32 bits
    #print(sub_keys)
    # Génération des 132 sous-clés
    for i in range(8, total_keys):
        new_key = (sub_keys[i - 8] ^ sub_keys[i - 5] ^ sub_keys[i - 3] ^ sub_keys[i - 1] ^ phi ^ i)
        # Rotation circulaire gauche de 11 bits
        new_key = ((new_key << 11) | (new_key >> (32 - 11))) & 0xFFFFFFFF
        sub_keys.append(new_key)
    
    # Organiser les sous-clés transformées en clés de tour de 128 bits
    round_keys = []
    for i in range(0, len(sub_keys), 4):
        round_key = (sub_keys[i] << 96) | (sub_keys[i + 1] << 64) | \
                    (sub_keys[i + 2] << 32 ) | sub_keys[i + 3]
        #round_keys.append(round_key.to_bytes(16, byteorder='big'))
        round_keys.append(round_key)
        
    
    perm_key = []
    for i in range(len(round_keys)):
        chunks = [(round_keys[i] >> (4 * i)) & 0xF for i in range(32)]  # 32 chunks of 4 bits

        # Apply the S-box to each chunk
        substituted_chunks = [serpent_sbox(chunk, 0) for chunk in chunks]

        # Reassemble the key
        reassembled_key = 0
        for i, chunk in enumerate(substituted_chunks):
            reassembled_key |= (chunk << (4 * i))
        perm_key.append(reassembled_key)
    

    return round_keys



def serpent_chiffrer(plaintext, round_keys, rounds=32):
    """
    Encrypts a 128-bit plaintext using Serpent.
    
    Parameters:
        plaintext (int): 128-bit plaintext.
        key (int): 128-bit encryption key.
        rounds (int): Number of rounds (default is 32).
        
    Returns:
        int: Encrypted ciphertext.
    """
    # Generate round keys
    

    # Initial permutation
    ciphertext = plaintext
    #round_num = 0
    for round_num in range(rounds):
        # Add Round Key
        ciphertext = ciphertext ^ round_keys[round_num]  
        # Substitution
        ciphertext = substitution(ciphertext, round_num // 8) 
        # Feistel de Réré
        ciphertext =  feistel(ciphertext, round_keys[round_num])
        # Transformation linéaire
        ciphertext = transfo_lineaire(ciphertext)
    return ciphertext

def serpent_dechiffrer(plaintext, round_keys, rounds=32):
    # Initial permutation
    ciphertext = plaintext
    round_num = 0

    for round_num in range(31, -1, -1):
        #Transformation linéaire
        ciphertext = reverse_transfo_lineaire(ciphertext)
        # Feistel de Réré
        ciphertext =  reverse_feistel(ciphertext, round_keys[round_num])
        # Substitution
        ciphertext = reverse_substitution(ciphertext, 4 + (round_num // 8))
        # Add Round Key
        ciphertext = ciphertext ^ round_keys[round_num]
    return ciphertext


# def test_cobra_encryption(shared_secret, plaintext):
#     """
#     Fonction de test pour l'intégration avec COBRA.
#     Utilise un secret partagé comme clé pour chiffrer/déchiffrer.
#     """
#     print("[INFO] Test du chiffrement COBRA avec la clé symétrique.")
#     # Convertir la clé partagée en 256 bits
#     key = shared_secret.ljust(32, b'\x00')
#     if len(shared_secret) > 32:
#         raise ValueError("La clé symétrique partagée dépasse 256 bits.")

    
#     # Exemple de texte clair
#     # plaintext = 0xabcdef0123456789abcdef0123456789
#     print(f"[DEBUG] Texte clair : {hex(plaintext)}")

#     # Expansion des clés
#     round_keys = key_expansion(key)

#     # Chiffrement
#     ciphertext = serpent_chiffrer(plaintext, round_keys)
#     print(f"[INFO] Texte chiffré : {hex(ciphertext)}")

#     # Déchiffrement
#     decrypted_text = serpent_dechiffrer(ciphertext, round_keys)
#     print(f"[INFO] Texte déchiffré : {hex(decrypted_text)}")

#     # Vérification
#     if plaintext == decrypted_text:
#         print("[SUCCESS] Test COBRA réussi : le texte déchiffré correspond au texte clair.")
#     else:
#         print("[ERROR] Échec du test COBRA.")

def test_cobra_encryption(shared_secret, plaintext):
    """
    Fonction de test pour l'intégration avec COBRA.
    Utilise un secret partagé comme clé pour chiffrer/déchiffrer.
    """
    print("[INFO] Test du chiffrement COBRA avec la clé symétrique.")

    # Convertir la clé partagée en 256 bits
    key = shared_secret.ljust(32, b'\x00')
    if len(shared_secret) > 32:
        raise ValueError("La clé symétrique partagée dépasse 256 bits.")

    # Taille de bloc pour Serpent (16 bytes = 128 bits)
    block_size = 16

    # Découper le texte en blocs
    plaintext_bytes = plaintext.encode('utf-8')
    blocks = [plaintext_bytes[i:i + block_size] for i in range(0, len(plaintext_bytes), block_size)]

    # Ajouter du padding au dernier bloc si nécessaire
    if len(blocks[-1]) < block_size:
        padding_length = block_size - len(blocks[-1])
        blocks[-1] += bytes([padding_length] * padding_length)

    print(f"[DEBUG] Texte clair (blocs) : {[block.hex() for block in blocks]}")

    # Expansion des clés
    round_keys = key_expansion(key)

    ciphertext_blocks = []
    decrypted_blocks = []

    # Chiffrement et déchiffrement bloc par bloc
    for block in blocks:
        block_int = int.from_bytes(block, byteorder='big')
        ciphertext_int = serpent_chiffrer(block_int, round_keys)
        ciphertext_blocks.append(ciphertext_int.to_bytes(block_size, byteorder='big'))

        decrypted_int = serpent_dechiffrer(ciphertext_int, round_keys)
        decrypted_blocks.append(decrypted_int.to_bytes(block_size, byteorder='big'))

    # Retirer le padding du dernier bloc déchiffré
    decrypted_blocks[-1] = decrypted_blocks[-1][:-decrypted_blocks[-1][-1]]

    # Reconstituer les textes
    ciphertext = b''.join(ciphertext_blocks)
    decrypted_text = b''.join(decrypted_blocks).decode('utf-8')

    print(f"[INFO] Texte chiffré (hex) : {ciphertext.hex()}")
    print(f"[INFO] Texte déchiffré : {decrypted_text}")

    # Vérification
    if plaintext == decrypted_text:
        print("[SUCCESS] Test COBRA réussi : le texte déchiffré correspond au texte clair.")
    else:
        print("[ERROR] Échec du test COBRA.")


        

def cobra_encrypt_file(input_path, output_path, key, block_size=16):
    """
    Chiffre un fichier en utilisant COBRA (par blocs).
    
    :param input_path: Chemin du fichier à chiffrer.
    :param output_path: Chemin pour sauvegarder le fichier chiffré.
    :param key: Clé symétrique pour le chiffrement.
    :param block_size: Taille des blocs en octets (par défaut 16 pour 128 bits).
    """
    # Expansion de la clé pour les rondes
    round_keys = key_expansion(key.ljust(32, b'\x00'))

    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        while chunk := infile.read(block_size):
            print(f"[DEBUG] Chunk original (hex) : {chunk.hex()}")

            # Ajouter du padding si le chunk est incomplet
            padding_len = block_size - len(chunk)
            if padding_len > 0:
                chunk += bytes([padding_len]) * padding_len
                print(f"[DEBUG] Chunk avec padding (hex) : {chunk.hex()}")

            # Chiffrement
            plaintext = int.from_bytes(chunk, byteorder='big')
            ciphertext = serpent_chiffrer(plaintext, round_keys)

            # Écrire le chunk chiffré
            outfile.write(ciphertext.to_bytes(block_size, byteorder='big'))
            print(f"[DEBUG] Chunk chiffré (hex) : {ciphertext.to_bytes(block_size, byteorder='big').hex()}")

    print(f"[INFO] Fichier chiffré sauvegardé dans {output_path}.")



def cobra_decrypt_file(input_path, output_path, key, block_size=16):
    """
    Déchiffre un fichier en utilisant COBRA (par blocs).
    
    :param input_path: Chemin du fichier à déchiffrer.
    :param output_path: Chemin pour sauvegarder le fichier déchiffré.
    :param key: Clé symétrique pour le déchiffrement.
    :param block_size: Taille des blocs en octets (par défaut 16 pour 128 bits).
    """
    # Expansion de la clé pour les rondes
    round_keys = key_expansion(key.ljust(32, b'\x00'))

    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        while chunk := infile.read(block_size):
            print(f"[DEBUG] Chunk chiffré lu (hex) : {chunk.hex()}")

            # Déchiffrement
            ciphertext = int.from_bytes(chunk, byteorder='big')
            plaintext = serpent_dechiffrer(ciphertext, round_keys)

            # Convertir le résultat en bytes
            decrypted_block = plaintext.to_bytes(block_size, byteorder='big')
            print(f"[DEBUG] Chunk déchiffré (avec padding) (hex) : {decrypted_block.hex()}")

            # Retirer le padding du dernier bloc
            if infile.peek(1):  # Pas le dernier bloc
                outfile.write(decrypted_block)
            else:
                padding_len = decrypted_block[-1]
                print(f"[DEBUG] Padding détecté : {padding_len}")
                outfile.write(decrypted_block[:-padding_len])  # Supprimer le padding

    print(f"[INFO] Fichier déchiffré sauvegardé dans {output_path}.")





# Exemple d'utilisation
key_128 = b"1234567890abcdef"  # Clé de 128 bits
key_192 = b"1234567890abcdef12345678"  # Clé de 192 bits
key_256 = b"1234567890abcdef1234567890abcdef"  # Clé de 256 bits

print("Sous-clés pour clé de 128 bits :")
text = 0xabcdef0123456789abcdef0123456789
key = key_expansion(key_256)
a = serpent_chiffrer(text, key)
print(hex(a))
print(hex(serpent_dechiffrer(a, key)))