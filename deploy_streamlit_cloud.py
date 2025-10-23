
# deploy_streamlit_cloud.py
import os
import subprocess
import webbrowser
from pathlib import Path

def setup_streamlit_cloud():
    """Configure le projet pour Streamlit Cloud"""

    # Créer le dépôt Git
    if not Path(".git").exists():
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial deployment to Streamlit Cloud"])

    # Instructions
    print("""
🎯 PRÊT POUR LE DÉPLOIEMENT STREAMLIT CLOUD!

Étapes à suivre:

1. 🌐 Allez sur: https://share.streamlit.io
2. 🔗 Connectez votre compte GitHub
3. 📁 Sélectionnez ce dépôt
4. ⚙️ Configuration:
   - Main file path: streamlit_app.py
   - Branch: main

5. 🚀 Cliquez sur "Deploy"

📋 Fichiers requis dans votre dépôt:
✅ streamlit_app.py    # Application principale
✅ requirements.txt    # Dépendances Python
✅ setup.sh           # Script d'installation (optionnel)

⚠️  IMPORTANT: Streamlit Cloud ne peut pas exécuter Ollama directement.
    Vous devrez configurer une instance Ollama séparée et mettre à jour l'URL dans l'application.
    """)

    # Ouvrir Streamlit Cloud dans le navigateur
    webbrowser.open("https://share.streamlit.io")

if __name__ == "__main__":
    setup_streamlit_cloud()
