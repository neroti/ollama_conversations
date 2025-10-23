
# deploy_all.py
import os
import sys
import subprocess
from pathlib import Path

class CloudDeployer:
    def __init__(self):
        self.deployments = {
            "1": ("Streamlit Cloud", self.deploy_streamlit),
            "2": ("Hugging Face", self.deploy_huggingface),
            "3": ("Ngrok (Local->Cloud)", self.deploy_ngrok),
            "4": ("Railway", self.deploy_railway)
        }

    def deploy_streamlit(self):
        """Déploie sur Streamlit Community Cloud"""
        print("🚀 Déploiement Streamlit Cloud...")
        subprocess.run([sys.executable, "deploy_streamlit_cloud.py"])

    def deploy_huggingface(self):
        """Déploie sur Hugging Face Spaces"""
        print("🤗 Déploiement Hugging Face...")
        subprocess.run([sys.executable, "huggingface_deployment.py"])

    def deploy_ngrok(self):
        """Déploie avec Ngrok"""
        print("🔗 Déploiement Ngrok...")
        subprocess.run(["chmod", "+x", "deploy_with_ngrok.sh"])
        subprocess.run(["./deploy_with_ngrok.sh"])

    def deploy_railway(self):
        """Déploie sur Railway"""
        print("🛤️  Déploiement Railway...")
        # Configuration Railway
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"
            }
        }

        with open("railway.json", "w") as f:
            import json
            json.dump(railway_config, f, indent=2)

        print("""
🎯 RAILWAY CONFIGURÉ!

Étapes:
1. 🌐 Allez sur: https://railway.app
2. 🔗 Connectez votre GitHub
3. 📁 Sélectionnez ce dépôt
4. 🚀 Le déploiement est automatique!

🔧 Railway détectera automatiquement la configuration.
""")

    def show_menu(self):
        """Affiche le menu de déploiement"""
        print("\n" + "="*50)
        print("🌍 MENU DE DÉPLOIEMENT CLOUD")
        print("="*50)

        for key, (name, _) in self.deployments.items():
            print(f"{key}. {name}")

        print("\n0. Quitter")
        print("="*50)

    def run(self):
        """Exécute le déployeur cloud"""
        while True:
            self.show_menu()
            choice = input("\n🎯 Choisissez une option: ").strip()

            if choice == "0":
                print("👋 À bientôt!")
                break
            elif choice in self.deployments:
                name, method = self.deployments[choice]
                print(f"\n🚀 Lancement du déploiement: {name}")
                try:
                    method()
                except Exception as e:
                    print(f"❌ Erreur: {e}")
            else:
                print("❌ Option invalide")

if __name__ == "__main__":
    deployer = CloudDeployer()
    deployer.run()
