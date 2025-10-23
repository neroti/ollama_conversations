
# ollama_web_agent.py
import requests
import json
import datetime
from conversation_manager import ConversationManager

class OllamaWebAgent:
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

        # Préparer la requête avec les outils disponibles
        payload = {
            "model": "mixtral:8x22b",
            "messages": [
                {
                    "role": "system",
                    "content": f"""Tu es un assistant avec accès à des outils de gestion de conversations.
                    Outils disponibles: {json.dumps(self.tools, ensure_ascii=False)}

                    Tu PEUX:
                    - Sauvegarder la conversation actuelle
                    - Lister les conversations existantes
                    - Charger une conversation précédente

                    Utilise les outils quand c'est pertinent."""
                }
            ] + self.current_conversation,
            "tools": self.tools,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response_data = response.json()

            # Vérifier si le modèle veut utiliser un outil
            if 'tool_calls' in response_data.get('message', {}):
                for tool_call in response_data['message']['tool_calls']:
                    resultat = self.executer_outil(tool_call)
                    # Rappeler l'API avec le résultat de l'outil
                    self.current_conversation.append(response_data['message'])
                    self.current_conversation.append({
                        "role": "tool",
                        "content": json.dumps(resultat, ensure_ascii=False),
                        "tool_call_id": tool_call['id']
                    })

                    # Rappeler pour avoir la réponse finale
                    response = requests.post(self.ollama_url, json={
                        "model": "mixtral:8x22b",
                        "messages": payload['messages'] + self.current_conversation[-2:]
                    })
                    response_data = response.json()

            # Ajouter la réponse à l'historique
            reponse_assistant = response_data['message']['content']
            self.current_conversation.append({"role": "assistant", "content": reponse_assistant})

            return reponse_assistant

        except Exception as e:
            return f"Erreur: {str(e)}"

    def executer_outil(self, tool_call):
        """Exécute les outils de gestion de conversation"""
        nom_fonction = tool_call['function']['name']
        parametres = json.loads(tool_call['function']['arguments'])

        if nom_fonction == "sauvegarder_conversation":
            fichier = self.conv_manager.sauvegarder_conversation(
                self.current_conversation,
                parametres['titre']
            )
            return {"status": "success", "fichier": str(fichier), "message": "Conversation sauvegardée"}

        elif nom_fonction == "lister_conversations":
            conversations = self.conv_manager.lister_conversations()
            return {"status": "success", "conversations": conversations}

        elif nom_fonction == "charger_conversation":
            conversation = self.conv_manager.charger_conversation(parametres['nom_fichier'])
            if conversation:
                self.current_conversation = conversation['messages']
                return {"status": "success", "message": f"Conversation '{parametres['nom_fichier']}' chargée"}
            else:
                return {"status": "error", "message": "Conversation non trouvée"}

    def sauvegarder_auto(self):
        """Sauvegarde automatique"""
        if len(self.current_conversation) >= 2:
            titre_auto = f"auto_save_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
            return self.conv_manager.sauvegarder_conversation(self.current_conversation, titre_auto)
