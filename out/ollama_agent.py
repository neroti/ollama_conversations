
import requests
import json
import datetime
from conversation_manager import ConversationManager

class OllamaAgent:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/chat"
        self.conv_manager = ConversationManager()
        self.current_conversation = []

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

    def envoyer_message(self, message_utilisateur):
        """Envoie un message à Ollama avec gestion de conversation"""

        # Ajouter le message utilisateur à l'historique
        self.current_conversation.append({"role": "user", "content": message_utilisateur})

        # Préparer la requête
        payload = {
            "model": "llama3.2:1b",  # Modèle plus léger pour test
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

            return reponse_assistant

        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            self.current_conversation.append({"role": "assistant", "content": error_msg})
            return error_msg

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
            return {"status": "success", "message": f"Conversation chargée: {nom_fichier}"}
        return {"status": "error", "message": "Conversation non trouvée"}

    def exporter_conversation(self, nom_fichier):
        """Exporte une conversation en Markdown"""
        return self.conv_manager.exporter_markdown(nom_fichier)

# Test du module
if __name__ == "__main__":
    agent = OllamaAgent()
    print("✅ OllamaAgent testé avec succès!")
