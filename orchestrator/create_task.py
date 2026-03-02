import os
from dotenv import load_dotenv
from notion_client import Client

# Charger les variables d'environnement depuis orchestrator/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

RAW_DB_ID = os.getenv("NOTION_DATABASE_ID", "")
DATABASE_ID = RAW_DB_ID.split("/")[-1].split("?")[0] if RAW_DB_ID else ""
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ Erreur : Variables d'environnement manquantes.")
    exit(1)

notion = Client(auth=NOTION_TOKEN)

properties = {
    "Name": {"title": [{"text": {"content": "US.3.6: Mémorisation et visualisation de la Stack (Fingerprint)"}}]},
    "Status": {"select": {"name": "Todo"}},
    "Category": {"select": {"name": "Coder"}},
    "Priority": {"select": {"name": "High"}},
    "Description": {"rich_text": [{"text": {"content": "J'aimerais que lorsque l'on crée son profil lors de la connexion (Onboarding Persona), cela garde en mémoire la stack technique par défaut et qu'on puisse la visualiser/modifier ensuite sur la page Dashboard > Stack Fingerprint.\n\nActions:\n1. S'assurer que les tags par défaut du métier sont insérés dans la table `user_stacks` lors du choix du Persona.\n2. Fetcher et afficher ces tags pré-remplis sur la page `/stack-fingerprint`."}}]}
}

try:
    notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
    print("✅ Tâche créée avec succès dans Notion !")
except Exception as e:
    print(f"❌ Erreur lors de la création : {e}")
