import os
import time
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client
from google import genai

# --- CONFIGURATION & ENV ---
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
RAW_DB_ID = os.getenv("NOTION_DATABASE_ID", "")
# Nettoyage si l'utilisateur a mis l'URL complète
DATABASE_ID = RAW_DB_ID.split("/")[-1].split("?")[0] if RAW_DB_ID else ""
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialisation des clients
notion = Client(auth=NOTION_TOKEN)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# --- PLACEHOLDER ANTIGRAVITY (Observabilité) ---
class AntigravityTracer:
    """Simule le wrapper Antigravity pour le monitoring"""
    def start_trace(self, agent_name, task_title):
        print(f"📡 [Antigravity] Trace démarrée : Agent {agent_name} sur '{task_title}'")
        return datetime.now()

    def end_trace(self, start_time, status="SUCCESS"):
        duration = datetime.now() - start_time
        print(f"✅ [Antigravity] Trace terminée en {duration.total_seconds()}s | Status: {status}")

tracer = AntigravityTracer()

# --- LOGIQUE NOTION ---
def get_todo_tasks():
    """Récupère les tâches 'Todo', et gère les échéances"""
    # 1. Polling des tâches TODO
    response = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Status", "select": {"equals": "Todo"}
        },
        sorts=[
            {
                "property": "Due Date",
                "direction": "ascending"
            }
        ]
    )
    return response.get("results")

def analyze_priority_and_routing(task):
    """Analyse les labels Trello/Notion et le texte pour déterminer la priorité et l'agent"""
    props = task["properties"]
    
    # Priorisation automatique (Urgent < 24h, High < 3j)
    priority = props.get("Priority", {}).get("select", {}).get("name", "Medium") if props.get("Priority", {}).get("select") else "Medium"
    due_date = props.get("Due Date", {}).get("date", {}).get("start") if props.get("Due Date", {}).get("date") else None
    
    if due_date:
        due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        delta = due - datetime.now(due.tzinfo)
        if delta.days < 1: priority = "Urgent"
        elif delta.days < 3: priority = "High"
        
    # Routage : Priorité à la Catégorie déjà assignée (si c'est une sous-tâche déléguée)
    category_prop = props.get("Category", {}).get("select")
    assigned_role = category_prop["name"] if category_prop else None
    
    # Par défaut, si non catégorisé, c'est le Planner qui découpe
    if not assigned_role:
        assigned_role = "Planner"
        
    return priority, assigned_role

def get_task_comments(page_id):
    """Récupère l'historique des commentaires de la tâche Notion"""
    try:
        response = notion.comments.list(block_id=page_id)
        comments = [ "".join([t["plain_text"] for t in c.get("rich_text", [])]) for c in response.get("results", []) ]
        return comments
    except Exception as e:
        return []

def update_task(page_id, status=None, agent=None, comment=None, description=None):
    """Met à jour le statut, l'agent, la description ou ajoute un commentaire dans Notion"""
    properties = {}
    if status:
        properties["Status"] = {"select": {"name": status}}
    
    if description:
        # La description est contenue sous le nom de propriété "Description" de type rich_text
        properties["Description"] = {"rich_text": [{"text": {"content": description}}]}
    
    # Optional logic: only update Category/Agent if the Notion property supports it
    if agent:
        properties["Category"] = {"select": {"name": agent}}
        
    try:
        if properties:
            notion.pages.update(page_id=page_id, properties=properties)
        
        if comment:
            notion.comments.create(parent={"page_id": page_id}, rich_text=[{"text": {"content": comment}}])
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la tâche {page_id}: {e}")

def get_system_prompt(role):
    """Charge le prompt système depuis le dossier agents"""
    try:
        with open(f"agents/{role.lower()}.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        # Fallback prompts if files are not found
        prompts = {
            "Architect": "Tu es un architecte logiciel expert en Data Stack. Analyse cette tâche et fournis une spec technique.",
            "Coder": "Tu es un développeur Senior Next.js/Supabase. Génère le code ou le plan d'implémentation pour cette tâche.",
            "Planner": "Tu es un Product Manager. Découpe cette feature en sous-tâches atomiques pour le backlog."
        }
        return prompts.get(role, prompts["Planner"])

def create_subtask(parent_id, title, category="Coder"):
    """Crée une sous-tâche dans Notion liée à une page parente"""
    properties = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Status": {"select": {"name": "Todo"}},
        "Category": {"select": {"name": category}},
    }
    try:
        notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
        print(f"  ↳ Sous-tâche créée : {title}")
    except Exception as e:
        print(f"❌ Erreur création sous-tâche : {e}")

def save_local_file(filepath, content):
    """Sauvegarde le code généré localement"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"💾 Fichier local sauvegardé : {filepath}")

# --- LOGIQUE AGENTIQUE (Gemini) ---
def run_agent_task(task_title, task_description, category):
    """Prépare le prompt et appelle Gemini"""
    role = category if category in ["Architect", "Coder", "Planner"] else "Planner"
    system_prompt = get_system_prompt(role)
    
    # Contextual enhancements for autonomous execution based on user workflow
    autonomous_instructions = """
    Tu es un agent autonome s'exécutant sur le terminal de l'utilisateur avec des droits avancés sur le système de Ticketing Notion. 
    Tu as la possibilité d'agir sur le système local ou de déléguer des tâches via des tags spécifiques dans ta réponse.
    
    --- GESTION DES SOUS-TÂCHES & DÉLÉGATION ---
    Pour déléguer des sous-tâches à d'autres agents, formatte ta réponse avec ce bloc exact:
    <DELEGATE>
    [Planner] Rédiger les User Stories pour l'Auth
    [Coder] Implémenter le middleware Supabase
    [Architect] Définir le schéma RLS
    </DELEGATE>
    
    --- DÉLÉGATION À ANTIGRAVITY (Gemini 3.1 Pro local) ---
    Si la tâche implique de coder, créer des fichiers, ou lancer des commandes dans le terminal, TU NE DOIS PAS LE FAIRE TOI-MÊME. 
    Rédige un **"Prompt d'Exécution Parfait"** destiné à ton collègue local Antigravity. 
    
    ATTENTION : Si la tâche nécessite une action QUE SEUL L'HUMAIN PEUT FAIRE (ex: Créer un projet sur Supabase, récupérer des clés d'API secrètes, s'inscrire sur un site), ajoute une section "INTERVENTION HUMAINE REQUISE".
    
    Formatte ta réponse avec ce bloc exact:
    <ANTIGRAVITY_TASK>
    # Contexte
    [Bref résumé de l'objectif]
    
    # 🧑‍💻 INTERVENTION HUMAINE REQUISE (Optionnel, si nécessaire)
    Pour accomplir cette tâche, le développeur humain doit d'abord faire ceci :
    1. Va sur [URL du service, ex: supabase.com]
    2. Clique sur 'Project Settings' > 'API'
    3. Copie l'URL et l'Anon Key
    4. Crée un fichier `.env.local` et colle : `NEXT_PUBLIC_SUPABASE_URL=...`
    (Explique EXACTEMENT où cliquer pour aider l'humain).
    
    # Instructions pour Antigravity (Le robot local)
    1. [Action détaillée 1 : ex. Installer le package @supabase/ssr]
    2. [Action détaillée 2 : ex. Créer le composant client avec le code suivant...]
    </ANTIGRAVITY_TASK>
    
    --- DEMANDE D'INFORMATION ---
    Si tu manques d'informations cruciales (ex: credentials API, précisions de design, architecture), arrête tout et pose la question:
    <NEED_INFO>
    Quels sont les identifiants Supabase ?
    </NEED_INFO>
    
    --- CHECKLIST ET RÉPONSE ---
    Si tu as utilisé <ANTIGRAVITY_TASK>, ne rajoute rien d'autre. Sinon, formule le reste de ta réponse sous forme de checklist "Prochaines étapes" ou explication de ta décision.
    """
    
    full_prompt = f"{system_prompt}\n\n{autonomous_instructions}\n\nContexte de la tâche : {task_description}"
    
    start_time = tracer.start_trace(role, task_title)
    
    models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-3-flash-preview', 'gemma-3-27b-it']
    last_error = None
    
    for model_name in models_to_try:
        try:
            print(f"  🤖 Tentative d'exécution avec le modèle : {model_name}...")
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )
            tracer.end_trace(start_time)
            return response.text, None
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"  ⚠️ Quota épuisé pour {model_name} (429). Bascule sur le modèle de secours...")
                last_error = error_msg
                continue
            else:
                # Other non-retryable error
                tracer.end_trace(start_time, status=f"ERROR: {error_msg}")
                return None, error_msg
                
    # Si tous les modèles de la liste échouent
    tracer.end_trace(start_time, status=f"ERROR: Fallback models exhausted")
    return None, last_error

# --- BOUCLE PRINCIPALE (Polling) ---
def main_orchestrator():
    print("🚀 Orchestrateur StackPulse démarré (Polling toutes les 30s)...")
    
    while True:
        try:
            tasks = get_todo_tasks()
            
            for task in tasks:
                page_id = task["id"]
                
                # Récupération sécurisée du titre
                title_prop = task.get("properties", {}).get("Name", {}).get("title", [])
                title = title_prop[0]["text"]["content"] if title_prop else "Nouvelle Tâche Sans Titre"
                
                # 1. Priorisation & Routage
                priority, assigned_agent = analyze_priority_and_routing(task)
                
                # Fetch comments to provide context and check for blocking issues
                comments = get_task_comments(page_id)
                if comments and comments[-1].startswith("❓ [Action Requise]"):
                    # The bot is waiting for a user reply. Skip processing.
                    continue
                
                # Optionnel : update de la priorité calculée dans Notion
                try: 
                    notion.pages.update(page_id=page_id, properties={"Priority": {"select": {"name": priority}}})
                except Exception: pass # Ignore if Priority col is missing
                
                description = f"Tâche : {title} | Priorité : {priority}"
                if comments:
                    description += "\n\n--- HISTORIQUE DES COMMENTAIRES (Réponses Utilisateur) ---\n"
                    description += "\n".join([f"- {c}" for c in comments])

                print(f"📦 Nouvelle tâche détectée : [{priority}] {title} -> {assigned_agent}")
                
                # 2. Dispatch : Passage en 'In Progress' et assignation (prise en charge autonome)
                update_task(page_id, status="In Progress", agent=assigned_agent)
                
                # 3. Exécution par Gemini
                result, error = run_agent_task(title, description, assigned_agent)
                
                if result:
                    import re
                    
                    # - Traitement d'un blocage NEED_INFO
                    info_match = re.search(r"<NEED_INFO>\n?(.*?)\n?</NEED_INFO>", result, re.DOTALL)
                    if info_match:
                        question = info_match.group(1).strip()
                        # On repasse en Todo pour que le flag "Agent Assigned : empty" soit potentiellement rechu, mais le commentaire bloque la boucle
                        update_task(page_id, status="Todo", description=f"ℹ️ Contexte manquant pour l'Agent :\n\n{question}", comment=f"❓ [Action Requise] L'agent {assigned_agent} a besoin d'aide. Lis la description.")
                        print(f"⏸️ Tâche '{title}' mise en pause (attente d'infos utilisateur).")
                        continue
                    
                    # - Traitement des délégations DELEGATE
                    subtasks_match = re.search(r"<DELEGATE>\n?(.*?)\n?</DELEGATE>", result, re.DOTALL)
                    if subtasks_match:
                        subtasks = [task.strip() for task in subtasks_match.group(1).split('\n') if task.strip()]
                        for subtask in subtasks:
                            # Parse format: [Role] Titre
                            m = re.match(r"\[(.*?)\] (.*)", subtask)
                            if m:
                                create_subtask(page_id, m.group(2).strip(), m.group(1).strip())
                            else:
                                create_subtask(page_id, subtask, "Coder")
                            
                    # - Traitement de la délégation à Antigravity
                    antigravity_match = re.search(r"<ANTIGRAVITY_TASK>\n?(.*?)\n?</ANTIGRAVITY_TASK>", result, re.DOTALL)
                    if antigravity_match:
                        prompt_content = antigravity_match.group(1).strip()
                        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        tasks_file = os.path.join(base_path, "tasks_to_code.md")
                        
                        # Append the task to the queue file
                        with open(tasks_file, "a", encoding="utf-8") as f:
                            f.write(f"\n\n---\n## Tâche Notion : {title}\n")
                            f.write(f"**Lien Notion:** https://notion.so/{page_id.replace('-', '')}\n")
                            f.write(f"{prompt_content}")
                            
                        print(f"📥 Tâche '{title}' transférée dans la boîte de réception locale (tasks_to_code.md)")
                        
                        # Update Notion task
                        update_task(
                            page_id, 
                            status="Review", # You can create a "Ready" column in Notion later and change this 
                            description=f"🤖 **Tâche déléguée à l'Agent Local (Antigravity) !**\n\nLe script Python a préparé le terrain. Demandez à Antigravity dans VSCode de lire le fichier `tasks_to_code.md` pour exécuter le code de cette tâche sur votre ordinateur.\n\n--- Prompt Généré ---\n{prompt_content[:1500]}", 
                            comment="🔔 Tâche en attente de validation manuelle via l'agent local Antigravity."
                        )
                        continue # On passe à la suivante car la clôture est gérée
                        
                    # Nettoyage du résultat pour le commentaire structure Notion
                    clean_result = re.sub(r"<DELEGATE>.*?</DELEGATE>", "[Sous-tâches déléguées créées]", result, flags=re.DOTALL)
                    clean_result = clean_result.strip()
                    if not clean_result: clean_result = "Tâche exécutée."
                    
                    # 4. Clôture autonome : Passage en 'Review' avec la checklist des prochaines étapes
                    # On inscrit la conclusion propre dans la 'Description' et on poste un commentaire de complétion court
                    desc_summary = clean_result[:1900]
                    update_task(page_id, status="Review", description=desc_summary, comment="✅ Intervention de l'agent terminée. Voir description.") 
                    print(f"✔️ Tâche '{title}' traitée de manière autonome et passée en Review.")
                else:
                    # Fallback d'erreur stricte : on ne reste jamais bloqué en "In Progress"
                    error_details = f"L'agent Gemini a craché ou renvoyé une erreur API.\n\nDétails techniques :\n{error}" if error else "Erreur silencieuse inconnue."
                    
                    if error and "429" in error:
                        # Erreur de quota API (Trop requêtes). On remet la tâche en Todo pour plus tard sans alerter (Silent Retry)
                        update_task(page_id, status="Todo")
                        print(f"⏳ Quota API dépassé (429). Tâche '{title}' remise en file d'attente (Todo). Pause de 60s...")
                        time.sleep(60)
                    else:
                        update_task(page_id, status="Ticketing", description=error_details, comment=f"⚠️ Erreur de l'agent {assigned_agent} pendant l'exécution. Action requise.")
                        print(f"🚨 Tâche '{title}' en échec, basculée dans Ticketing.")

        except Exception as e:
            print(f"🚨 Erreur lors du polling : {e}")

        time.sleep(30) # Délai entre deux sessions de polling

if __name__ == "__main__":
    main_orchestrator()
