import socket
import os
from dh_key_exchange_server import dh_exchange
from cobra import cobra_encrypt_ecb, cobra_decrypt_ecb
from utils_network import send_full_msg, recv_full_msg

session_key = None

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an IP address and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections
server_socket.listen(1)
print("Server listening on port 12345...")


def receive_data():
    data = client_socket.recv(1024)
    client_socket.sendall(b"Recu")
    return data.decode()



# Accept a connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")
def dh():
    # Recevoir la clé publique A
    data = client_socket.recv(1024)
    A = int(data.decode())
    client_socket.sendall(b"Recu")
    # Recevoir le paramètre p
    data = client_socket.recv(1024)
    p = int(data.decode())
    client_socket.sendall(b"Recu")
    # Recevoir le paramètre g
    data = client_socket.recv(1024)
    g = int(data.decode())
    client_socket.sendall(b"Tout recu")
    print(f"[INFO] Vos paramètres DH : p = {p}, g = {g}, clé publique du Client = {A}")
    key, B = dh_exchange(A, p, g)
    client_socket.sendall(str(B).encode())
    return key
    
def encrypt_rsa(message, e, n):
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    if message_int >= n:
        raise ValueError("Message is too large for the key size.")
    return pow(message_int, e, n)

while True:
    username = None
    data = client_socket.recv(1024)  # Taille du tampon de 1024 octets
    client_socket.sendall(b"Recu")
    if not data:
        # Si aucune donnée n'est reçue, cela signifie que le client a fermé la connexion
        break

    message = data.decode()
    if message == "dh":
        # Si le message est "dh", attendre les paramètres DH
        print("[INFO] Début de l'échange DH")
        session_key = dh()
        print(f"[INFO] Clé de session {session_key}")
        # Répondre au client  

    # elif message == "send_data":
    #     # Si le message est "send_data", attendre les données chiffrées
    #     print("[INFO] Attente des données chiffrées")
    #     data = client_socket.recv(1024)
    #     print(f"[INFO] Données chiffrées reçues: {int(data.decode())}")
    #     client_socket.sendall(b"Recu")
    #     text = serpent_dechiffrer(int(data.decode()), session_key)

    #     byte_length = (text.bit_length() + 7) // 8  # Determine the number of bytes needed
    #     text_as_bytes = text.to_bytes(byte_length, byteorder='big')
    #     decoded_text = text_as_bytes.decode()
    #     print(f"[INFO] Données déchiffrées: {(decoded_text)}")
    #     username = receive_data()
    
    #     try:
    #     # Charger les clés publiques et privées
    #         with open(f"users/{username}/rsa_public_key.txt", "r") as pub_file:
    #             e = int(pub_file.readline())
    #             n = int(pub_file.readline())
    #     except FileNotFoundError:
    #         print(f"[ERROR] User {username} introuvable.")
    #     print(f"[INFO] Paramètres RSA: e = {e}, n = {n}")
    #     rsa_msg = encrypt_rsa(decoded_text, e, n)
    #     os.makedirs(f"users/{username}", exist_ok=True)
    #     with open(f"users/{username}/coffre-fort.txt", "a") as priv_file:
    #         priv_file.write(f"{rsa_msg}\n")


    elif message == "send_data":
        print("[INFO] Attente des données chiffrées.")

        try:
            # Recevoir les données chiffrées avec COBRA
            ciphertext = recv_full_msg(client_socket)
            client_socket.sendall(b"Recu")  # Ack

            # Déchiffrer avec COBRA
            session_key_bytes = session_key.to_bytes((session_key.bit_length() + 7) // 8, byteorder='big')
            plaintext_bytes = cobra_decrypt_ecb(ciphertext, session_key_bytes)
            plaintext = plaintext_bytes.decode('utf-8')
            print(f"[INFO] Données déchiffrées : {plaintext}")

            # Recevoir le username
            username_bytes = recv_full_msg(client_socket)
            client_socket.sendall(b"Recu")  # Ack
            username = username_bytes.decode()
            print(f"[INFO] Nom d'utilisateur : {username}")

            # Charger les clés publiques pour RSA
            try:
                with open(f"users/{username}/rsa_public_key.txt", "r") as pub_file:
                    e = int(pub_file.readline())
                    n = int(pub_file.readline())
            except FileNotFoundError:
                print(f"[ERROR] Clé publique pour {username} introuvable.")
                send_full_msg(client_socket, b"ERREUR : Cle publique introuvable.")
                continue

            # Diviser en segments d'octets pour RSA
            plaintext_segments = [plaintext_bytes[i:i + 100] for i in range(0, len(plaintext_bytes), 100)]
            user_dir = f"users/{username}/coffre-fort"
            os.makedirs(user_dir, exist_ok=True)

            # Charger ou initialiser `last_message_id`
            last_id_path = f"{user_dir}/last_message_id.txt"
            try:
                with open(last_id_path, "r") as id_file:
                    last_message_id = int(id_file.read().strip())
            except FileNotFoundError:
                last_message_id = 0

            # Chiffrer et stocker chaque segment dans un fichier
            for segment in plaintext_segments:
                last_message_id += 1
                rsa_msg = pow(int.from_bytes(segment, 'big'), e, n)
                message_path = f"{user_dir}/message_{last_message_id}.txt"
                with open(message_path, "w") as message_file:
                    message_file.write(str(rsa_msg))
                print(f"[INFO] Segment enregistré dans {message_path}.")

            # Mettre à jour le `last_message_id`
            with open(last_id_path, "w") as id_file:
                id_file.write(str(last_message_id))

        except Exception as e:
            print(f"[ERROR] Erreur lors du traitement de `send_data` : {e}")
            send_full_msg(client_socket, b"ERREUR : Impossible de traiter le message.")





    elif message == "info_rsa":
        # Si le message est "info_rsa", attendre les paramètres RSA
        print("[INFO] Attente des paramètres RSA")
        username = receive_data()
        e = int(receive_data())
        n = int(receive_data())
        print(f"[INFO] Paramètres RSA reçus: e = {e}, n = {n}")
        os.makedirs(f"users/{username}", exist_ok=True)
        with open(f"users/{username}/rsa_public_key.txt", "w") as priv_file:
            priv_file.write(f"{e}\n{n}\n")

    # elif message == "recup_msg":
    #     # Si le message est "recup_msg", envoyer les données chiffrées
    #     print("[INFO] Envoi des données chiffrées")
    #     position = int(receive_data())
    #     username = receive_data()
    #     try:
    #         with open(f"users/{username}/coffre-fort.txt", "r") as priv_file:
    #             for i in range(position):
    #                 rsa_msg = priv_file.readline()
    #     except FileNotFoundError:
    #         print(f"[ERROR] User {username} introuvable.")
    #     print(f"[INFO] Données chiffrées: {rsa_msg}")
    #     client_socket.sendall(rsa_msg.encode())


    elif message == "recup_msg":
        print("[INFO] Envoi des données chiffrées demandées.")

        # Recevoir le username
        username_bytes = recv_full_msg(client_socket)
        client_socket.sendall(b"Recu")  # Ack
        username = username_bytes.decode()
        print(f"[INFO] Nom d'utilisateur : {username}")

        # Recevoir le message_id
        message_id_bytes = recv_full_msg(client_socket)
        client_socket.sendall(b"Recu")  # Ack
        message_id = message_id_bytes.decode()
        print(f"[INFO] Message ID demandé : {message_id}")

        # Lire le fichier chiffré RSA
        try:
            message_path = f"users/{username}/coffre-fort/message_{message_id}.txt"
            with open(message_path, "r") as file:
                rsa_msg = file.read().strip()
        except FileNotFoundError:
            print(f"[ERROR] Fichier message_{message_id}.txt introuvable.")
            send_full_msg(client_socket, b"ERREUR : Fichier introuvable.")
            continue

        # Envoyer le fichier chiffré RSA au client
        send_full_msg(client_socket, rsa_msg.encode())
        print("[INFO] Données chiffrées RSA envoyées.")




# Close the connection
client_socket.close()
server_socket.close()
