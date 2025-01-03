import os
from key_management import create_user
from zkp import authenticate_with_schnorr
from dh_key_exchange import start_dh_exchange
from certificate import verify_certificate
from cobra import cobra_encrypt_file, cobra_decrypt_file, test_cobra_encryption

def access_vault(username):
    print(f"[INFO] Accès au coffre-fort pour l'utilisateur {username}.")
    # Placeholder pour le coffre-fort

def post_auth_menu(username, shared_secret):
    while True:
        print(f"Bienvenue {username}, que souhaitez-vous faire ?")
        print("1. Accéder au coffre-fort")
        print("2. Chiffrer un fichier")
        print("3. Déchiffrer un fichier")
        print("5. Test de l'algorithme COBRA.")
        print("4. Quitter")
        option = input("Choisissez une option : ")

        if option == "1":
            access_vault(username)
        elif option == "2":
            filepath = input("Entrez le chemin du fichier à chiffrer : ")
            if not os.path.isfile(filepath):
                print("[ERROR] Le fichier spécifié n'existe pas.")
                continue
            output_path = input("Entrez le chemin du fichier chiffré : ")
            try:
                cobra_encrypt_file(filepath, output_path, shared_secret)
                print(f"[INFO] Fichier chiffré avec succès et enregistré sous : {output_path}")
            except Exception as e:
                print(f"[ERROR] Une erreur est survenue lors du chiffrement : {e}")

        elif option == "3":
            filepath = input("Entrez le chemin du fichier à déchiffrer : ")
            if not os.path.isfile(filepath):
                print("[ERROR] Le fichier spécifié n'existe pas.")
                continue
            output_path = input("Entrez le chemin du fichier déchiffré : ")
            try:
                cobra_decrypt_file(filepath, output_path, shared_secret)
                print(f"[INFO] Fichier déchiffré avec succès et enregistré sous : {output_path}")
            except Exception as e:
                print(f"[ERROR] Une erreur est survenue lors du déchiffrement : {e}")

            
        elif option == "5":
            plaintext = input("Entrez le msg a chiffrer : ")
            # plaintext_bytes = plaintext.encode('utf-8')
            # print(f"après encodage : {plaintext_bytes}")
            # plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')
            # print(f"après int : {plaintext_int}")
            test_cobra_encryption(shared_secret, plaintext)  # Passer le secret partagé
            
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

            # Étape 1 : Vérification du certificat
            if not verify_certificate(username):
                print("[ERROR] Échec de la vérification du certificat. Arrêt.")
                continue

            # Étape 2 : Authentification via ZKP
            if authenticate_with_schnorr(username, password):
                print("[INFO] Authentification réussie. Génération de la clé de session...")
                shared_secret = start_dh_exchange()
                print(f"[DEBUG] Clé de session générée : {shared_secret.hex()}")    
                post_auth_menu(username, shared_secret)
            else:
                print("[ERROR] Échec de l'authentification.")
        elif option == "3":
            print("Au revoir !")
            break
        else:
            print("[ERROR] Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
