
# huggingface_deployment.py
import os
import json
from pathlib import Path

def create_huggingface_config():
    """Crée la configuration pour Hugging Face Spaces"""

    config = {
        "app_file": "streamlit_app.py",
        "requirements": ["streamlit", "requests", "duckduckgo-search", "pandas"],
        "sdk": "streamlit"
    }

    # Créer README pour Hugging Face
    readme_content = """
---
title: Assistant Ollama Cloud
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
app_file: streamlit_app.py
pinned: false
---

# 🤖 Assistant Ollama Cloud

Assistant IA personnel avec support multi-modèles Ollama.

## Features
- 💬 Chat intelligent
- 🔄 Multi-modèles
- 🌐 Interface web
- 💾 Conversations persistantes

## Configuration
Configurez l'URL de votre instance Ollama dans l'interface.
"""

    with open("README.md", "w") as f:
        f.write(readme_content)

    with open("huggingface.json", "w") as f:
        json.dump(config, f, indent=2)

    print("""
🎯 CONFIGURATION HUGGING FACE SPACES TERMINÉE!

Étapes:
1. 🌐 Allez sur: https://huggingface.co/spaces
2. ➕ Cliquez sur "Create new Space"
3. ⚙️ Configurez:
   - SDK: Streamlit
   - Repository name: votre-nom
   - Visibility: Public ou Private

4. 📤 Uploader tous les fichiers:
   - streamlit_app.py
   - requirements.txt
   - README.md

5. 🚀 Le déploiement est automatique!

🔗 Votre application sera disponible sur:
   https://huggingface.co/spaces/votre-utilisateur/votre-espace
""")

if __name__ == "__main__":
    create_huggingface_config()
