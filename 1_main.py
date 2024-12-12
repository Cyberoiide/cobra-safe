from key_management import create_user
from zkp import authenticate_with_schnorr
from dh_key_exchange import start_dh_exchange

def verify_certificate(username):
    print(f"[INFO] Vérification du certificat pour {username}.")
    # Simulated certificate verification
    return True

def post_auth_menu(username):
    while True:
        print(f"Bienvenue {username}, que souhaitez-vous faire ?")
        print("1. Échange de clés (Diffie-Hellman)")
        print("2. Accéder au coffre-fort")
        print("3. Chiffrer/Déchiffrer un fichier")
        print("4. Quitter")
        option = input("Choisissez une option : ")

        if option == "1":
            start_dh_exchange()
        elif option == "2":
            access_vault(username)
        elif option == "3":
            print("[INFO] Fonction non encore implémentée.")
        elif option == "4":
            print("Au revoir !")
            break
        else:
            print("[ERROR] Option invalide, veuillez réessayer.")

def access_vault(username):
    print(f"[INFO] Accès au coffre-fort pour l'utilisateur {username}.")
    # Placeholder for vault functionality

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
            print("Démarrage de l'échange Diffie-Hellman...")
            shared_secret = start_dh_exchange()
            print(f"Le secret partagé est : {shared_secret}")

        else:
            print("[ERROR] Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
