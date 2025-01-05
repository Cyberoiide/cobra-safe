import random

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



def key_expansion(key_bytes, rounds=32):
    """
    Expansion de la clé pour l'algorithme Serpent.
    :param key_bytes: Clé d'entrée (bytes), de taille 16, 24 ou 32 octets (128, 192, 256 bits).
    :param rounds: Nombre de tours (32 par défaut).
    :return: Liste des sous-clés générées (132 sous-clés).
    """
    if not isinstance(key_bytes, (bytes, bytearray)):
        raise ValueError("La clé doit être en bytes.")

    # On s'assure d'avoir 32 octets en padding si la clé est plus courte
    key_bytes = key_bytes.ljust(32, b'\x00')
    
    # On divise en 8 blocs de 4 octets => 32 bits
    blocks = []
    for i in range(8):
        block = int.from_bytes(key_bytes[i*4:(i+1)*4], byteorder='big')
        blocks.append(block)

    phi = 0x9E3779B9
    total_keys = 132
    sub_keys = blocks[:]  # on recopie

    for i in range(8, total_keys):
        new_key = (sub_keys[i - 8] 
                   ^ sub_keys[i - 5] 
                   ^ sub_keys[i - 3] 
                   ^ sub_keys[i - 1] 
                   ^ phi ^ i)
        # Rotation circulaire gauche de 11 bits
        new_key = ((new_key << 11) | (new_key >> (32 - 11))) & 0xFFFFFFFF
        sub_keys.append(new_key)

    # Organiser les sous-clés en blocs de 128 bits
    round_keys = []
    for i in range(0, len(sub_keys), 4):
        round_key = ((sub_keys[i] << 96)
                     | (sub_keys[i+1] << 64)
                     | (sub_keys[i+2] << 32)
                     | sub_keys[i+3])
        round_keys.append(round_key)

    return round_keys




def serpent_chiffrer(plaintext: int, round_keys: list[int], rounds=32) -> int:
    """
    Encrypts a 128-bit plaintext using Serpent.
    
    Parameters:
        plaintext (int): 128-bit plaintext.
        key (int): 128-bit encryption key.
        rounds (int): Number of rounds (default is 32).
        
    Returns:
        int: Encrypted ciphertext.
    """
    # # Generate round keys
    # round_keys = key_expansion(key_bytes)

    # Initial permutation
    ciphertext = plaintext
    for round_num in range(rounds):
        ciphertext ^= round_keys[round_num]
        ciphertext = substitution(ciphertext, round_num // 8)
        ciphertext = feistel(ciphertext, round_keys[round_num])
        ciphertext = transfo_lineaire(ciphertext)
    return ciphertext

def serpent_dechiffrer(ciphertext_int: int, round_keys: list[int], rounds=32) -> int:
    # Initial permutation

    # round_keys = key_expansion(key)
    
    plaintext = ciphertext_int
    # round_num = 0

    for round_num in range(31, -1, -1):
        plaintext = reverse_transfo_lineaire(plaintext)
        plaintext = reverse_feistel(plaintext, round_keys[round_num])
        plaintext = reverse_substitution(plaintext, 4 + (round_num // 8))
        plaintext ^= round_keys[round_num]
    return plaintext


BLOCK_SIZE = 16  # 128 bits

def cobra_encrypt_ecb(plaintext_bytes: bytes, key_bytes: bytes) -> bytes:
    """
    Chiffre plaintext_bytes (taille arbitraire) en mode ECB
    avec votre implémentation COBRA (Serpent modifié).
    """
    # 1) Padding
    padding_len = BLOCK_SIZE - (len(plaintext_bytes) % BLOCK_SIZE)
    padding = bytes([padding_len] * padding_len)
    plaintext_bytes += padding

    # 2) Expansion de la clé
    round_keys = key_expansion(key_bytes)

    ciphertext_blocks = []

    # 3) Traitement bloc par bloc
    for i in range(0, len(plaintext_bytes), BLOCK_SIZE):
        block = plaintext_bytes[i:i + BLOCK_SIZE]
        block_int = int.from_bytes(block, 'big')

        # On passe round_keys directement
        encrypted_int = serpent_chiffrer(block_int, round_keys)
        encrypted_block = encrypted_int.to_bytes(BLOCK_SIZE, 'big')

        ciphertext_blocks.append(encrypted_block)

    return b''.join(ciphertext_blocks)

def cobra_decrypt_ecb(ciphertext_bytes: bytes, key_bytes: bytes) -> bytes:
    """
    Déchiffre ciphertext_bytes (taille multiple de 16) en mode ECB
    via COBRA (Serpent) et retire le padding.
    """
    # 1) Expansion de la clé
    round_keys = key_expansion(key_bytes)  # expansion une seule fois

    plaintext_blocks = []

    # 2) Déchiffrement bloc par bloc
    for i in range(0, len(ciphertext_bytes), BLOCK_SIZE):
        block = ciphertext_bytes[i : i + BLOCK_SIZE]
        block_int = int.from_bytes(block, 'big')

        # On passe la liste de sous-clés
        decrypted_int = serpent_dechiffrer(block_int, round_keys)
        decrypted_block = decrypted_int.to_bytes(BLOCK_SIZE, 'big')
        plaintext_blocks.append(decrypted_block)


    # 3) Retirer le padding sur le dernier bloc
    full_plaintext = b''.join(plaintext_blocks)
    padding_len = full_plaintext[-1]  # On suppose que le padding est correct
    return full_plaintext[:-padding_len]



# Exemple d'utilisation
"""key_128 = b"1234567890abcdef"  # Clé de 128 bits
key_192 = b"1234567890abcdef12345678"  # Clé de 192 bits
key_256 = b"1234567890abcdef1234567890abcdef"  # Clé de 256 bits
key_bin = 2168733696540266461650633951754762301768537109613915519
print("Sous-clés pour clé de 128 bits :")
text = 0xabcdef0123456789abcdef0123456789
text = "Test"
text = int.from_bytes(text.encode(), byteorder='big')
print(text)
key = key_expansion(key_bin)
a = serpent_chiffrer(text, key_bin)
print(hex(a))
print(hex(serpent_dechiffrer(a, key_bin)))"""
