import socket
import random
from dh_key_exchange_server import dh_exchange
from cobra import serpent_chiffrer, serpent_dechiffrer

session_key = None

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an IP address and port
server_socket.bind(('localhost', 12345))

# Listen for incoming connections
server_socket.listen(1)
print("Server listening on port 12345...")

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
    
while True:
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
    elif message == "send_data":
        # Si le message est "send_data", attendre les données chiffrées
        print("[INFO] Attente des données chiffrées")
        data = client_socket.recv(1024)
        print(f"[INFO] Données chiffrées reçues: {int(data.decode())}")
        client_socket.sendall(b"Recu")
        text = serpent_dechiffrer(int(data.decode()), session_key)

        byte_length = (text.bit_length() + 7) // 8  # Determine the number of bytes needed
        text_as_bytes = text.to_bytes(byte_length, byteorder='big')
        decoded_text = text_as_bytes.decode()
        print(f"[INFO] Données déchiffrées: {(decoded_text)}")

    else:
        # Si le message n'est pas "dh", envoyer une réponse générique
        client_socket.sendall(b"Message non reconnu")
    


# Close the connection
client_socket.close()
server_socket.close()
