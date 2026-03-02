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
    "Name": {"title": [{"text": {"content": "US.4: Crawler n8n (GitHub, Arxiv, Blogs) & stockage DB"}}]},
    "Status": {"select": {"name": "Todo"}},
    "Category": {"select": {"name": "Planner"}},
    "Priority": {"select": {"name": "High"}},
    "Description": {"rich_text": [{"text": {"content": "L'objectif de cette tâche est d'implémenter l'ingestion de données avec n8n.\nOn doit pouvoir récupérer des sources depuis GitHub, Arxiv ou des blogs techniques, crawler leur contenu et le stocker proprement dans la base vectorielle ou relationnelle de Supabase."}}]}
}

try:
    notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
    print("✅ Tâche créée avec succès dans Notion !")
except Exception as e:
    print(f"❌ Erreur lors de la création : {e}")
