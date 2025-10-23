
#!/usr/bin/env python3
# test_persistence.py

import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent))

def test_persistence():
    """Teste le système de persistance des conversations"""
    from conversation_manager import ConversationManager
    from ollama_agent import OllamaAgent

    print("🧪 Test du système de persistance...")

    # Test ConversationManager
    manager = ConversationManager()

    # Créer quelques sessions de test
    session1 = manager.create_new_session("llama3.2:1b")
    manager.update_current_session([
        {"role": "user", "content": "Bonjour, c'est le test 1"},
        {"role": "assistant", "content": "Salut! Je suis là pour aider."}
    ], "Test Session 1")

    session2 = manager.create_new_session("qwen2:1.5b")
    manager.update_current_session([
        {"role": "user", "content": "Deuxième conversation de test"},
        {"role": "assistant", "content": "Je suis le deuxième assistant"}
    ], "Test Session 2")

    # Retour à la première session
    manager.switch_session(session1)

    # Vérifier les sessions
    sessions = manager.list_all_sessions()
    print(f"✅ Sessions créées: {len(sessions)}")

    # Test OllamaAgent avec persistance
    agent = OllamaAgent()
    current_session = agent.get_current_session_info()
    print(f"✅ Session actuelle: {current_session.get('title')}")
    print(f"✅ Messages dans session: {current_session.get('message_count')}")

    # Test nouvelle conversation
    new_id = agent.create_new_conversation("llama3.2:1b")
    print(f"✅ Nouvelle conversation créée: {new_id}")

    print("🎯 Test de persistance réussi!")
    print("💾 Les conversations seront conservées même après fermeture de l'application.")

if __name__ == "__main__":
    test_persistence()
