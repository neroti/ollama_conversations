
#!/usr/bin/env python3
# fix_duplicate_sessions.py

import json
from pathlib import Path
import uuid

def fix_duplicate_sessions():
    """Corrige les sessions avec des IDs dupliqués"""
    history_file = Path.home() / "ollama_conversations" / "session_history.json"

    if not history_file.exists():
        print("✅ Aucun fichier d'historique trouvé - rien à corriger")
        return

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # Vérifier les doublons
        session_ids = set()
        duplicates_found = False

        for session in history.get("sessions", []):
            session_id = session["session_id"]
            if session_id in session_ids:
                # Doublon détecté - générer un nouvel ID
                new_id = f"session_{uuid.uuid4().hex[:8]}_fixed"
                print(f"🔧 Correction du doublon: {session_id} -> {new_id}")
                session["session_id"] = new_id
                duplicates_found = True
            else:
                session_ids.add(session_id)

        if duplicates_found:
            # Sauvegarder l'historique corrigé
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print("✅ Doublons corrigés avec succès!")
        else:
            print("✅ Aucun doublon détecté")

    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")

if __name__ == "__main__":
    fix_duplicate_sessions()
