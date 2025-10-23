
#!/bin/bash
# Sauvegarde de l'environnement
source venv_assistant/bin/activate
pip freeze > requirements_backup.txt
echo "✅ Dépendances sauvegardées dans requirements_backup.txt"

# Sauvegarde des conversations
cp -r sauvegardes sauvegardes_backup
cp -r exports exports_backup
echo "✅ Conversations sauvegardées"
