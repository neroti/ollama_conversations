
import json
import os
import datetime
from pathlib import Path
import shutil
import uuid  # Ajout pour générer des IDs uniques

class ConversationManager:
    def __init__(self):
        self.base_dir = Path.home() / "ollama_conversations"
        self.saves_dir = self.base_dir / "sauvegardes"
        self.exports_dir = self.base_dir / "exports"
        self.history_file = self.base_dir / "session_history.json"

        # Créer les dossiers
        self.saves_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

        # Initialiser l'historique de session
        self.initialize_session_history()

    def initialize_session_history(self):
        """Initialise ou charge l'historique des sessions"""
        if not self.history_file.exists():
            base_history = {
                "sessions": [],
                "current_session_id": None,
                "created_at": str(datetime.datetime.now()),
                "total_sessions": 0
            }
            self.save_session_history(base_history)

    def load_session_history(self):
        """Charge l'historique des sessions"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur chargement historique: {e}")
            return {"sessions": [], "current_session_id": None, "total_sessions": 0}

    def save_session_history(self, history_data):
        """Sauvegarde l'historique des sessions"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde historique: {e}")

    def create_new_session(self, model_name="llama3.2:1b"):
        """Crée une nouvelle session de conversation avec ID unique"""
        # Générer un ID unique avec UUID pour éviter les conflits
        session_id = f"session_{uuid.uuid4().hex[:8]}_{datetime.datetime.now().strftime('%H%M%S')}"

        session_data = {
            "session_id": session_id,
            "model_used": model_name,
            "created_at": str(datetime.datetime.now()),
            "last_activity": str(datetime.datetime.now()),
            "message_count": 0,
            "title": f"Conversation avec {model_name}",
            "messages": [],
            "is_active": True
        }

        history = self.load_session_history()
        history["sessions"].append(session_data)
        history["current_session_id"] = session_id
        history["total_sessions"] = len(history["sessions"])

        self.save_session_history(history)
        return session_id

    def get_current_session(self):
        """Récupère la session actuelle"""
        history = self.load_session_history()
        if not history["current_session_id"]:
            return self.create_new_session()

        for session in history["sessions"]:
            if session["session_id"] == history["current_session_id"]:
                return session

        # Si la session actuelle n'existe pas, en créer une nouvelle
        return self.create_new_session()

    def update_current_session(self, messages, title=None):
        """Met à jour la session actuelle avec les nouveaux messages"""
        history = self.load_session_history()
        current_id = history["current_session_id"]

        if not current_id:
            current_id = self.create_new_session()
            history = self.load_session_history()

        for session in history["sessions"]:
            if session["session_id"] == current_id:
                session["messages"] = messages
                session["last_activity"] = str(datetime.datetime.now())
                session["message_count"] = len(messages)
                if title and len(messages) >= 2:
                    session["title"] = title
                break

        self.save_session_history(history)

    def switch_session(self, session_id):
        """Change de session active"""
        history = self.load_session_history()
        history["current_session_id"] = session_id

        # Mettre à jour le statut actif
        for session in history["sessions"]:
            session["is_active"] = (session["session_id"] == session_id)

        self.save_session_history(history)
        return self.get_session_by_id(session_id)

    def get_session_by_id(self, session_id):
        """Récupère une session par son ID"""
        history = self.load_session_history()
        for session in history["sessions"]:
            if session["session_id"] == session_id:
                return session
        return None

    def list_all_sessions(self, limit=50):
        """Liste toutes les sessions par ordre d'activité"""
        history = self.load_session_history()
        sessions = sorted(
            history["sessions"],
            key=lambda x: x["last_activity"],
            reverse=True
        )
        return sessions[:limit]

    def delete_session(self, session_id):
        """Supprime une session"""
        history = self.load_session_history()
        history["sessions"] = [s for s in history["sessions"] if s["session_id"] != session_id]

        # Si on supprime la session actuelle, en créer une nouvelle
        if history["current_session_id"] == session_id:
            if history["sessions"]:
                history["current_session_id"] = history["sessions"][0]["session_id"]
            else:
                history["current_session_id"] = self.create_new_session()

        history["total_sessions"] = len(history["sessions"])
        self.save_session_history(history)

    def export_session_history(self):
        """Exporte tout l'historique des sessions"""
        history = self.load_session_history()
        export_file = self.exports_dir / f"full_history_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json"

        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        return export_file

    # Méthodes existantes conservées...
    def sauvegarder_conversation(self, messages, titre=None):
        """Sauvegarde une conversation avec métadonnées (existant)"""
        if not titre:
            titre = f"Conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        titre = "".join(c for c in titre if c.isalnum() or c in (' ', '-', '_')).rstrip()
        titre = titre.replace(' ', '_')

        conversation_data = {
            "metadata": {
                "id": str(datetime.datetime.now().timestamp()),
                "titre": titre,
                "date_creation": datetime.datetime.now().isoformat(),
                "model_utilise": os.getenv("OLLAMA_MODEL", "llama3.2:1b"),
                "nombre_messages": len(messages)
            },
            "messages": messages
        }

        fichier_sauvegarde = self.saves_dir / f"{titre}.json"
        with open(fichier_sauvegarde, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)

        return fichier_sauvegarde

    def lister_conversations(self):
        """Liste toutes les conversations sauvegardées (existant)"""
        conversations = []
        for fichier in self.saves_dir.glob("*.json"):
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conversations.append({
                        "fichier": fichier.name,
                        "titre": data["metadata"]["titre"],
                        "date": data["metadata"]["date_creation"],
                        "messages": data["metadata"]["nombre_messages"]
                    })
            except Exception as e:
                print(f"Erreur lecture {fichier}: {e}")
        return sorted(conversations, key=lambda x: x["date"], reverse=True)

# Test du module amélioré
if __name__ == "__main__":
    manager = ConversationManager()
    print("✅ ConversationManager avec UUID testé!")
    print(f"📁 Dossier: {manager.base_dir}")
    print(f"📊 Sessions totales: {manager.load_session_history().get('total_sessions', 0)}")
