from key_management import create_user,create_rsa
from zkp import authenticate_with_schnorr
from dh_key_exchange import start_dh_exchange
from cobra import cobra_decrypt_ecb, cobra_encrypt_ecb
import socket
from utils_network import send_full_msg, recv_full_msg




# print("1. Échange de clés (Diffie-Hellman)")
session_key = None
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect(('localhost', 12345))

def verify_certificate(username):
    print(f"[INFO] Vérification du certificat pour {username}.")
    # Simulated certificate verification
    return True

# def decrypt(ciphertext, d, n):
#     decrypted_int = pow(ciphertext, d, n)
#     decrypted_message = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode('utf-8')
#     return decrypted_message

def encrypt_message_with_cobra(plaintext: str, session_key_bytes: bytes) -> bytes:
    """
    Chiffre une chaîne de caractères (plaintext) avec COBRA.
    """
    plaintext_bytes = plaintext.encode('utf-8')
    return cobra_encrypt_ecb(plaintext_bytes, session_key_bytes)

def decrypt_message_with_cobra(ciphertext: bytes, session_key_bytes: bytes) -> str:
    """
    Déchiffre un ciphertext en bytes avec COBRA et retourne une chaîne UTF-8.
    """
    plaintext_bytes = cobra_decrypt_ecb(ciphertext, session_key_bytes)
    return plaintext_bytes.decode('utf-8')




def post_auth_menu(username):
    #Echange de clé de session dès l'authentification
    A, a, p, g = start_dh_exchange()
    messages = [b"dh",str(A).encode(),str(p).encode(),str(g).encode()]
    for data in messages:
        client_socket.sendall(data)
        retour = client_socket.recv(1024)
    # Receive data from the server
    data = client_socket.recv(1024)
    B = int(data.decode())
    session_key = pow(B, a, p)
    session_key_bytes = session_key.to_bytes((session_key.bit_length() + 7) // 8, byteorder='big')
    print(f"[INFO] La clé de session en bytes : {session_key_bytes.hex()}")

    while True:
        print(f"Bienvenue {username}, que souhaitez-vous faire ?")
        # print("1. Échange de clés (Diffie-Hellman)")
        print("1. Envoyer un message au coffre-fort")
        print("2. Récuperer le message du coffre-fort")
        print("3. Quitter")
        option = input("Choisissez une option : ")

        if option == "1":
            print("[INFO] Envoi d'un message au coffre-fort.")
            text = input("Entrez ce que vous voulez envoyer au coffre-fort : ")

            # Chiffrer le texte avec COBRA
            ciphertext = encrypt_message_with_cobra(text, session_key_bytes)

            # Envoyer la commande "send_data"
            client_socket.sendall(b"send_data")
            ack = client_socket.recv(1024)

            # Envoyer le message chiffré
            send_full_msg(client_socket, ciphertext)
            ack = client_socket.recv(1024)

            # Envoyer le nom d'utilisateur
            send_full_msg(client_socket, username.encode())
            ack = client_socket.recv(1024)

            print("[INFO] Message chiffré envoyé.")


        elif option == "2":
            print("[INFO] Récupération d'un message depuis le coffre-fort.")

            # Envoyer la commande "recup_msg"
            client_socket.sendall(b"recup_msg")
            ack = client_socket.recv(1024)

            # Envoyer le nom d'utilisateur
            send_full_msg(client_socket, username.encode())
            ack = client_socket.recv(1024)

            # Envoyer l'ID du message
            message_id = input("Quel message_id voulez-vous récupérer ? ")
            send_full_msg(client_socket, message_id.encode())
            ack = client_socket.recv(1024)

            # Charger la clé privée locale
            private_key_path = f"users/{username}/rsa_private_key.txt"
            print(f"[DEBUG] Chargement de la clé privée depuis : {private_key_path}")
            try:
                with open(private_key_path, "r") as priv_file:
                    d = int(priv_file.readline())
                    n = int(priv_file.readline())
            except FileNotFoundError:
                print(f"[ERROR] Clé privée non trouvée pour l'utilisateur {username}.")
                return

            # Recevoir les blocs RSA chiffrés avec COBRA
            plaintext_blocks = []
            while True:
                cobra_ciphertext = recv_full_msg(client_socket)

                # Vérifier si c'est le signal de fin
                if cobra_ciphertext == b"FIN":
                    print("[INFO] Fin de la transmission des blocs.")
                    break

                # Déchiffrer le bloc avec COBRA
                session_key_bytes = session_key.to_bytes((session_key.bit_length() + 7) // 8, byteorder="big")
                rsa_block_bytes = cobra_decrypt_ecb(cobra_ciphertext, session_key_bytes)
                rsa_block = rsa_block_bytes.decode("utf-8")

                print(f"[DEBUG] Bloc déchiffré avec COBRA : {rsa_block}")

                # Déchiffrer avec RSA
                rsa_block_int = int(rsa_block)
                decrypted_block_int = pow(rsa_block_int, d, n)
                decrypted_block = decrypted_block_int.to_bytes((decrypted_block_int.bit_length() + 7) // 8, byteorder="big")
                plaintext_blocks.append(decrypted_block)

            # Reconstituer le message complet
            plaintext_bytes = b"".join(plaintext_blocks)
            plaintext = plaintext_bytes.decode("utf-8")

            print(f"[INFO] Message déchiffré : {plaintext}")

        elif option == "3":
            print("Au revoir !")
            break
        else:
            print("[ERROR] Option invalide, veuillez réessayer.")


def main():
    while True:
        print("Bienvenue dans le Coffre-Fort Numérique")
        print("1. Créer un compte")
        print("2. Authentification")
        print("3. Quitter")
        option = input("Choisissez une option : ")

        if option == "1":
            username = input("Entrez votre nom d'utilisateur : ")
            password = input("Entrez un mot de passe : ")
            create_user(username, password)
            e,n = create_rsa(username)
            messages = ["info_rsa",username, str(e),str(n)]
            for data in messages:
                client_socket.sendall(data.encode())
                retour = client_socket.recv(1024)
            print(f"Compte créé avec succès pour l'utilisateur {username}.")


        elif option == "2":
            username = input("Entrez votre nom d'utilisateur : ")
            password = input("Entrez votre mot de passe : ")

            if not verify_certificate(username):
                print("[ERROR] Échec de la vérification du certificat.")
                continue

            if authenticate_with_schnorr(username, password):
                post_auth_menu(username)


        elif option == "3":
            client_socket.close()

        else:
            print("[ERROR] Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
