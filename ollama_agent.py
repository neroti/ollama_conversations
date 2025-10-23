
import requests
import json
import datetime
from conversation_manager import ConversationManager

class OllamaAgent:
    def __init__(self, model_name="llama3.2:1b"):
        self.ollama_url = "http://localhost:11434/api/chat"
        self.conv_manager = ConversationManager()

        # Charger la session actuelle ou en créer une nouvelle
        current_session = self.conv_manager.get_current_session()
        self.current_conversation = current_session.get("messages", [])
        self.current_model = model_name
        self.current_session_id = current_session.get("session_id")

        # Définition des outils (functions)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "sauvegarder_conversation",
                    "description": "Sauvegarde la conversation actuelle avec un titre personnalisé",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "titre": {
                                "type": "string",
                                "description": "Titre descriptif pour la sauvegarde"
                            }
                        },
                        "required": ["titre"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "lister_conversations",
                    "description": "Liste toutes les conversations sauvegardées disponibles",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "charger_conversation",
                    "description": "Charge une conversation précédente par son nom",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "nom_fichier": {
                                "type": "string",
                                "description": "Nom du fichier de conversation à charger"
                            }
                        },
                        "required": ["nom_fichier"]
                    }
                }
            }
        ]

    def create_new_conversation(self, model_name=None):
        """Crée une nouvelle conversation vide"""
        if model_name:
            self.current_model = model_name

        new_session_id = self.conv_manager.create_new_session(self.current_model)
        self.current_conversation = []
        self.current_session_id = new_session_id

        return new_session_id

    def envoyer_message(self, message_utilisateur):
        """Envoie un message à Ollama avec sauvegarde automatique"""

        # Ajouter le message utilisateur à l'historique
        self.current_conversation.append({"role": "user", "content": message_utilisateur})

        # Préparer la requête
        payload = {
            "model": self.current_model,
            "messages": self.current_conversation,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            # Ajouter la réponse à l'historique
            reponse_assistant = response_data['message']['content']
            self.current_conversation.append({"role": "assistant", "content": reponse_assistant})

            # Sauvegarder automatiquement dans la session
            title = None
            if len(self.current_conversation) == 2:  # Premier échange
                title = message_utilisateur[:50] + "..." if len(message_utilisateur) > 50 else message_utilisateur

            self.conv_manager.update_current_session(self.current_conversation, title)

            return reponse_assistant

        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            self.current_conversation.append({"role": "assistant", "content": error_msg})

            # Sauvegarder même en cas d'erreur
            self.conv_manager.update_current_session(self.current_conversation)

            return error_msg

    def get_available_models(self):
        """Récupère la liste des modèles disponibles via l'API Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return sorted(models)
            return []
        except Exception as e:
            print(f"Erreur récupération modèles: {e}")
            return []

    def change_model(self, new_model):
        """Change le modèle actuel"""
        available_models = self.get_available_models()
        if new_model in available_models:
            self.current_model = new_model

            # Mettre à jour la session avec le nouveau modèle
            current_session = self.conv_manager.get_current_session()
            current_session["model_used"] = new_model
            self.conv_manager.update_current_session(self.current_conversation)

            return True
        return False

    def switch_to_session(self, session_id):
        """Change de session de conversation"""
        session = self.conv_manager.switch_session(session_id)
        if session:
            self.current_conversation = session.get("messages", [])
            self.current_session_id = session_id
            self.current_model = session.get("model_used", "llama3.2:1b")
            return True
        return False

    def get_current_session_info(self):
        """Retourne les informations de la session actuelle"""
        return self.conv_manager.get_current_session()

    def list_all_sessions(self):
        """Liste toutes les sessions disponibles"""
        return self.conv_manager.list_all_sessions()

    # Méthodes existantes conservées...
    def sauvegarder_conversation_actuelle(self, titre=None):
        """Sauvegarde la conversation actuelle"""
        if not self.current_conversation:
            return {"status": "error", "message": "Aucune conversation à sauvegarder"}

        fichier = self.conv_manager.sauvegarder_conversation(self.current_conversation, titre)
        return {"status": "success", "fichier": str(fichier)}

    def lister_conversations_sauvegardees(self):
        """Liste les conversations sauvegardées"""
        return self.conv_manager.lister_conversations()

    def charger_conversation_sauvegardee(self, nom_fichier):
        """Charge une conversation sauvegardée"""
        conversation = self.conv_manager.charger_conversation(nom_fichier)
        if conversation:
            self.current_conversation = conversation['messages']

            # Mettre à jour la session actuelle
            title = conversation["metadata"]["titre"]
            self.conv_manager.update_current_session(self.current_conversation, title)

            return {"status": "success", "message": f"Conversation chargée: {nom_fichier}"}
        return {"status": "error", "message": "Conversation non trouvée"}

# Test du module amélioré
if __name__ == "__main__":
    agent = OllamaAgent()
    print("✅ OllamaAgent avec persistance testé!")
    print(f"📚 Modèles disponibles: {agent.get_available_models()}")
    print(f"💬 Session actuelle: {agent.get_current_session_info().get('title', 'Nouvelle')}")
