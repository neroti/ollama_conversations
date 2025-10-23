
import requests
import subprocess
import json
from pathlib import Path

class ModelManager:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"

    def get_installed_models(self):
        """Récupère tous les modèles installés"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get('models', []):
                    model_info = {
                        'name': model['name'],
                        'size': model.get('size', 0),
                        'modified': model.get('modified_at', '')
                    }
                    # Récupérer les détails du modèle
                    details = self.get_model_details(model['name'])
                    if details:
                        model_info.update({
                            'parameters': details.get('parameter_size', 'N/A'),
                            'quantization': details.get('quantization_level', 'N/A'),
                            'family': details.get('model_family', 'N/A')
                        })
                    models.append(model_info)
                return models
            return []
        except Exception as e:
            print(f"Erreur récupération modèles: {e}")
            return []

    def get_model_details(self, model_name):
        """Récupère les détails d'un modèle spécifique"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/show",
                json={"name": model_name},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur détails modèle {model_name}: {e}")
            return None

    def pull_model(self, model_name):
        """Télécharge un nouveau modèle"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )

            # Suivre la progression
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'status' in data:
                        yield data['status']
                    if 'completed' in data and 'total' in data:
                        progress = (data['completed'] / data['total']) * 100
                        yield f"Progression: {progress:.1f}%"

            yield "✅ Téléchargement terminé"

        except Exception as e:
            yield f"❌ Erreur: {str(e)}"

    def delete_model(self, model_name):
        """Supprime un modèle"""
        try:
            response = requests.delete(
                f"{self.ollama_url}/api/delete",
                json={"name": model_name},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur suppression {model_name}: {e}")
            return False

    def get_recommended_models(self):
        """Retourne une liste de modèles recommandés"""
        return [
            "llama3.2:1b",
            "llama3.2:3b",
            "qwen2.5:0.5b",
            "qwen2.5:1.5b",
            "phi3:mini",
            "mistral:7b",
            "mixtral:8x7b"
        ]

if __name__ == "__main__":
    manager = ModelManager()
    models = manager.get_installed_models()
    print("📚 Modèles installés:")
    for model in models:
        print(f"  - {model['name']} ({model.get('parameters', 'N/A')})")
