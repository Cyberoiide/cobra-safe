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


def key_expansion(key, rounds=32):
    """
    Expansions des clés pour l'algorithme Serpent.
    
    :param key: Clé d'entrée (bytes), de taille 128, 192 ou 256 bits.
    :param rounds: Nombre de tours (par défaut 32).
    :return: Liste des sous-clés générées (132 blocs de 32 bits).
    """
    # Étape 1 : Initialisation de la clé
    #key = key.ljust(32, b'\x00')  # Complète avec des zéros à droite pour obtenir 32 octets
    binary_representation = bin(key)[2:]  # Remove "0b" prefix
    binary_representation = binary_representation + '0' * (256 - len(binary_representation))
    print(binary_representation)
    # Convert binary string to bytes
    key = int(binary_representation, 2).to_bytes(32, byteorder='big') 

    blocks = []  # Contient les 8 blocs de 32 bits
    for i in range(8):  # Diviser en 8 blocs
        block = int.from_bytes(key[i * 4:(i + 1) * 4], byteorder='big')
        blocks.append(block)
        

    # Étape 2 : Itérations de l’expansion de clé :
    sub_keys = blocks[:]
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

# Exemple d'utilisation
key_128 = b"1234567890abcdef"  # Clé de 128 bits
key_192 = b"1234567890abcdef12345678"  # Clé de 192 bits
key_256 = b"1234567890abcdef1234567890abcdef"  # Clé de 256 bits

print("Sous-clés pour clé de 128 bits :")
text = 0xabcdef0123456789abcdef0123456789
key = key_expansion(2168733696540266461650633951754762301768537109613915519)
print(key[1].bit_length())