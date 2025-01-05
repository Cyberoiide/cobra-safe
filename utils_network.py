# utils_network.py
import struct

def send_full_msg(sock, data_bytes):
    """
    Envoie un message avec un préfixe indiquant sa longueur.
    """
    size = len(data_bytes)
    sock.sendall(struct.pack('>I', size))  # Envoyer la taille sur 4 octets (big-endian)
    sock.sendall(data_bytes)              # Envoyer les données

def recv_full_msg(sock):
    """
    Reçoit un message avec un préfixe de longueur.
    """
    # Lire la taille du message
    header = sock.recv(4)
    if len(header) < 4:
        raise ConnectionError("Erreur lors de la lecture de la taille.")
    size = struct.unpack('>I', header)[0]

    # Lire les données
    chunks = []
    received = 0
    while received < size:
        chunk = sock.recv(min(4096, size - received))  # Lire en morceaux de 4 Ko max
        if not chunk:
            raise ConnectionError("Connexion interrompue.")
        chunks.append(chunk)
        received += len(chunk)

    return b''.join(chunks)
