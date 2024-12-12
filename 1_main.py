from key_management import create_user
from zkp import authenticate_with_schnorr
from dh_key_exchange import start_dh_exchange
from cobra import serpent_chiffrer, serpent_dechiffrer
import socket
print("1. Échange de clés (Diffie-Hellman)")
session_key = None
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect(('localhost', 12345))

def verify_certificate(username):
    print(f"[INFO] Vérification du certificat pour {username}.")
    # Simulated certificate verification
    return True

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
    session_key = pow(B,a,p)
    print(f"La clé de session est {session_key}")

    while True:
        print(f"Bienvenue {username}, que souhaitez-vous faire ?")
        print("1. Échange de clés (Diffie-Hellman)")
        print("2. Envoyer un message au coffre-fort")
        print("3. Récuperer le message du coffre-fort")
        print("4. Quitter")
        option = input("Choisissez une option : ")

        if option == "1":
            print("[INFO] Démarrage de l'échange Diffie-Hellman...")	
        elif option == "2":
            print("[INFO] Envoi d'un message au coffre-fort.")
            text = 0xabcdef0123456789abcdef0123456789
            text = input("Entrez ce que vous voulez envoyer au coffre-fort : ")
            text = int.from_bytes(text.encode(), byteorder='big')
            ciphertext = serpent_chiffrer(text, session_key)
            messages = ["send_data",str(ciphertext)]
            for data in messages:
                client_socket.sendall(data.encode())
                retour = client_socket.recv(1024)
            print(f"[INFO] Message chiffré envoyé : {ciphertext}")
        elif option == "3":
            print("[INFO] Fonction non encore implémentée.")
        elif option == "4":
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
