import os
import re
from dotenv import load_dotenv
from notion_client import Client

# Charger les variables d'environnement
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
PAGE_ID = "3170ee90d76480a79b21e08b7b3a82f6"

if not NOTION_TOKEN:
    print("❌ No NOTION_TOKEN found.")
    exit(1)

notion = Client(auth=NOTION_TOKEN)

# 1. Lire le Walkthrough local
walkthrough_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WALKTHROUGH.md")
if not os.path.exists(walkthrough_path):
    print("❌ WALKTHROUGH.md introuvable.")
    exit(1)

with open(walkthrough_path, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Convertir Markdown vers liste de blocs Notion
def parse_markdown_to_blocks(md_text):
    blocks = []
    lines = md_text.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        
        # Gérer le nettoyage basique pour le texte enrichi (Notion gère le markdown dans le text content, mais limitons les parasites)
        clean_text = line.replace('**', '').replace('`', '')
        
        # Parser
        if stripped_line.startswith('### '):
            blocks.append({
                "object": "block", "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": clean_text.replace('### ', '', 1).strip()}}]}
            })
        elif stripped_line.startswith('## '):
            blocks.append({
                "object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": clean_text.replace('## ', '', 1).strip()}}]}
            })
        elif stripped_line.startswith('# '):
            blocks.append({
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": clean_text.replace('# ', '', 1).strip()}}]}
            })
        elif stripped_line.startswith('- '):
            blocks.append({
                "object": "block", "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": clean_text.replace('- ', '', 1).strip()}}]}
            })
        else:
            blocks.append({
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": clean_text.strip()}}]}
            })
            
    return blocks

new_blocks = parse_markdown_to_blocks(content)

# 3. Supprimer les anciens blocs de la page
print("🗑️ Nettoyage de l'ancienne page...")
try:
    has_more = True
    start_cursor = None
    while has_more:
        response = notion.blocks.children.list(block_id=PAGE_ID, start_cursor=start_cursor)
        for child in response.get('results', []):
            try:
                notion.blocks.delete(block_id=child['id'])
            except Exception:
                pass # ignorer si un bloc ne peut pas être supprimé
        has_more = response.get('has_more', False)
        start_cursor = response.get('next_cursor')
except Exception as e:
    print(f"⚠️ Erreur lors du nettoyage : {e}")

# 4. Pousser les nouveaux blocs (par paquets de 100 max)
print(f"⬆️ Poussée de {len(new_blocks)} blocs sur Notion...")
try:
    for i in range(0, len(new_blocks), 100):
        chunk = new_blocks[i:i+100]
        notion.blocks.children.append(block_id=PAGE_ID, children=chunk)
        
    print("✅ Walkthrough synchronisé sur Notion avec succès !")
except Exception as e:
    print(f"❌ Erreur lors de l'ajout des blocs : {e}")
