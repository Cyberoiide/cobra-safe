# cobra-safe

# Coffre-Fort Numérique

## Description
Le **Coffre-Fort Numérique** est une application sécurisée permettant de gérer des utilisateurs, d'effectuer des échanges de clés via Diffie-Hellman, d'utiliser un mécanisme de dérivation de clé sécurisé (KDF), et d'authentifier les utilisateurs via le protocole de Schnorr Zero-Knowledge Proof (ZKP). Ce projet combine des principes cryptographiques fondamentaux pour offrir une solution de sécurité robuste.

---

## Fonctionnalités principales
1. **Création de comptes utilisateurs :**
   - Génération de clés publiques et privées pour chaque utilisateur.
   - Stockage sécurisé des clés dans des fichiers dédiés.

2. **Authentification utilisateur (Schnorr ZKP) :**
   - Authentification sans révélation de la clé privée.
   - Vérification basée sur une preuve mathématique.

3. **Échange de clés (Diffie-Hellman) :**
   - Génération de clés publiques/privées.
   - Calcul d'un secret partagé sécurisé avec un pair.

4. **Dérivation de clés (KDF) :**
   - Utilisation de SHA-256 pour dériver une clé à partir d'un mot de passe.
   - Transformation sécurisée répétée pour protéger les mots de passe faibles.

5. **Gestion des utilisateurs :**
   - Création et gestion de plusieurs comptes utilisateurs avec stockage des clés associées.

---

## Structure des fichiers
- **`1_main.py`** : Point d'entrée principal. Gère la navigation dans les menus et les actions principales du projet. 
- **`dh_key_exchange.py`** : Implémente l'échange de clés Diffie-Hellman. 
- **`kdf.py`** : Gère la dérivation de clés à partir de mots de passe via SHA-256. 
- **`key_management.py`** : Crée les utilisateurs et génère leurs clés publiques et privées. 
- **`utils.py`** : Fournit des outils comme l'exponentiation modulaire rapide et la génération de nombres premiers. 
- **`zkp.py`** : Implémente l'authentification utilisateur avec le protocole Schnorr ZKP. 

---

## Prérequis
- **Python 3.10 ou supérieur**
- Bibliothèques standard Python (aucune dépendance externe requise)

---

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Cyberoiide/cobra-safe.git
   cd cobra-safe
   ```

2. Assurez-vous d'utiliser Python 3.10 ou supérieur.

3. Lancez le programme principal :
   ```bash
   python3 1_main.py
   ```

---

## Utilisation
1. **Créer un compte :**
   - Suivez le menu pour créer un utilisateur avec un nom d'utilisateur et un mot de passe.

2. **Authentification :**
   - Entrez vos identifiants pour vous connecter via Schnorr ZKP.

3. **Échange de clés Diffie-Hellman :**
   - Génération de clés et calcul d'un secret partagé.

4. **Personnalisation :**
   - Modifiez les paramètres des clés dans `utils.py` pour ajuster la taille des clés ou la sécurité.

---

## Notes techniques
- **Authentification ZKP :** Basée sur Schnorr, vérifie l'identité d'un utilisateur sans révéler sa clé privée.
- **Échange Diffie-Hellman :** Les paramètres `p` (nombre premier) et `g` (générateur) sont modifiables dans `dh_key_exchange.py`.
- **KDF sécurisé :** SHA-256 est utilisé avec 10 000 itérations pour une protection accrue contre les attaques par force brute.