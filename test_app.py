
#!/usr/bin/env python3
import sys
from pathlib import Path

# Ajouter le chemin
sys.path.append(str(Path(__file__).parent))

def tester_modules():
    """Teste tous les modules"""
    try:
        # Test ConversationManager
        from conversation_manager import ConversationManager
        manager = ConversationManager()
        print("✅ ConversationManager: OK")

        # Test OllamaAgent
        from ollama_agent import OllamaAgent
        agent = OllamaAgent()
        print("✅ OllamaAgent: OK")

        # Test structure dossiers
        dossiers = [
            manager.base_dir,
            manager.saves_dir,
            manager.exports_dir
        ]
        for dossier in dossiers:
            if dossier.exists():
                print(f"✅ Dossier {dossier}: OK")
            else:
                print(f"❌ Dossier {dossier}: MANQUANT")

        # Test Ollama
        import requests
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Service Ollama: OK")
            else:
                print("❌ Service Ollama: ERREUR")
        except:
            print("❌ Service Ollama: HORS LIGNE")

        print("\n🎯 TEST TERMINÉ - Application prête!")

    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

    return True

if __name__ == "__main__":
    tester_modules()
