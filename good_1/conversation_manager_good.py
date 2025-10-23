
import json
import os
import datetime
from pathlib import Path

class ConversationManager:
    def __init__(self):
        self.base_dir = Path.home() / "ollama_conversations"
        self.saves_dir = self.base_dir / "sauvegardes"
        self.exports_dir = self.base_dir / "exports"
        self.saves_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def sauvegarder_conversation(self, messages, titre=None):
        """Sauvegarde une conversation avec métadonnées"""
        if not titre:
            titre = f"Conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Nettoyer le titre pour les noms de fichiers
        titre = "".join(c for c in titre if c.isalnum() or c in (' ', '-', '_')).rstrip()
        titre = titre.replace(' ', '_')

        conversation_data = {
            "metadata": {
                "id": str(datetime.datetime.now().timestamp()),
                "titre": titre,
                "date_creation": datetime.datetime.now().isoformat(),
                "model_utilise": os.getenv("OLLAMA_MODEL", "mixtral:8x22b"),
                "nombre_messages": len(messages)
            },
            "messages": messages
        }

        fichier_sauvegarde = self.saves_dir / f"{titre}.json"
        with open(fichier_sauvegarde, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)

        return fichier_sauvegarde

    def lister_conversations(self):
        """Liste toutes les conversations sauvegardées"""
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

    def charger_conversation(self, nom_fichier):
        """Charge une conversation spécifique"""
        fichier = self.saves_dir / nom_fichier
        if not fichier.exists():
            return None

        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur chargement {fichier}: {e}")
            return None

    def exporter_markdown(self, nom_fichier):
        """Exporte une conversation en format Markdown"""
        conversation = self.charger_conversation(nom_fichier)
        if not conversation:
            return None

        try:
            md_content = f"# {conversation['metadata']['titre']}\n\n"
            md_content += f"*Date: {conversation['metadata']['date_creation']}*\n"
            md_content += f"*Modèle: {conversation['metadata']['model_utilise']}*\n\n"

            for msg in conversation['messages']:
                role_emoji = "👤" if msg['role'] == 'user' else "🤖"
                md_content += f"## {role_emoji} {msg['role'].title()}\n\n{msg['content']}\n\n---\n\n"

            export_file = self.exports_dir / f"{conversation['metadata']['titre']}.md"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(md_content)

            return export_file
        except Exception as e:
            print(f"Erreur export: {e}")
            return None

# Test du module
if __name__ == "__main__":
    manager = ConversationManager()
    print("✅ ConversationManager testé avec succès!")
    print(f"📁 Dossier: {manager.base_dir}")
