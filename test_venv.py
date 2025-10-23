
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

def tester_venv():
    """Teste si l'environnement virtuel est correctement configuré"""

    print("🔍 Test de l'environnement virtuel...")

    # Vérifier si on est dans un venv
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"✅ Dans un environnement virtuel: {in_venv}")

    # Vérifier le chemin Python
    python_path = sys.executable
    print(f"✅ Python exécutable: {python_path}")

    # Vérifier les dépendances
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit: NON INSTALLÉ")
        return False

    try:
        import requests
        print(f"✅ Requests: {requests.__version__}")
    except ImportError:
        print("❌ Requests: NON INSTALLÉ")
        return False

    # Vérifier la structure des dossiers
    dossiers = ['sauvegardes', 'exports']
    for dossier in dossiers:
        if Path(dossier).exists():
            print(f"✅ Dossier {dossier}: OK")
        else:
            print(f"⚠️  Dossier {dossier}: CRÉATION")
            Path(dossier).mkdir(exist_ok=True)

    # Test Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Service Ollama: ACTIF")
        else:
            print("⚠️  Service Ollama: ERREUR DE CONNEXION")
    except:
        print("❌ Service Ollama: HORS LIGNE")

    print("\n🎯 ENVIRONNEMENT PRÊT!")
    return True

if __name__ == "__main__":
    tester_venv()
