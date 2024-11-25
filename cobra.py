# Vérification basique de Python dans VS Code
print("✅ Python fonctionne dans VS Code!")

# Vérification des bibliothèques intégrées
import math
print(f"La racine carrée de 16 est : {math.sqrt(16)}")

# Utilisation des bibliothèques tierces si elles sont installées
try:
    import numpy as np
    array = np.array([1, 2, 3, 4])
    print(f"Array NumPy : {array}")
except ImportError:
    print("❌ NumPy n'est pas installé. Vous pouvez l'installer avec : pip install numpy")

# Test de boucle et conditions
for i in range(5):
    print(f"Test de boucle : {i}")

print("🚀 Tout est prêt pour coder !")