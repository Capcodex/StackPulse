# StackPulse Orchestrator

Bienvenue dans l'Orchestrateur StackPulse ! Ce module en Python est le cerveau asynchrone du projet. Il connecte votre gestionnaire de tâches (Notion) avec des agents IA (Gemini) et un exécuteur local (Antigravity) pour un développement 100% autonome.

## 🧠 Comment fonctionne la logique des Agents ?

Le principe repose sur une délégation en cascade ("Chain of Command") entre différents rôles spécialisés :

1. **Le Planner (PM)** : Il scrute Notion à la recherche de nouvelles "Epic" (tâches lourdes et vagues sans catégorie technique définie). Dès qu'il en trouve une, il la découpe en *sous-tâches atomiques* et utilise le tag XML `<DELEGATE>` pour attribuer ces tâches à l'Architecte ou au Coder.
2. **L'Architect (Concepteur)** : Lorsqu'il reçoit une sous-tâche nécessitant de la modélisation (ex: "Créer la base de données"), il rédige les schémas techniques (Prisma, SQL, Flow) puis délègue l'implémentation au Coder via `<DELEGATE>`.
3. **Le Coder (Développeur)** : Son rôle est de produire le code final. Mais comme il tourne dans le cloud (Gemini via le script Python), il rédige une instruction ultra-précise et la place dans une balise `<ANTIGRAVITY_TASK>`.

### Interaction avec l'Environnement Local

Lorsque le script Python intercepte une balise `<ANTIGRAVITY_TASK>` générée par le **Coder**, il extrait le contenu et l'écrit physiquement dans le fichier local `tasks_to_code.md` situé à la racine du projet. 
C'est cette "boîte de réception" qui permet à l'agent local (Antigravity/Cursor/Autopilot) de lire les consignes et de venir modifier vos fichiers locaux (Next.js, Supabase, etc.).

## 🔄 La boucle d'interaction avec Notion

1. **Poll (Lecture)** : Le script interroge la base de données Notion toutes les X secondes pour trouver les tâches ayant le status `Todo`.
2. **Routing** : Il vérifie la colonne `Catégorie` de la tâche sur Notion pour savoir à qui l'assigner (`planner`, `architect`, `coder`).
3. **Processing** : L'IA Gemini prend le relais en lisant la description de la tâche et les fichiers `.txt` de prompts liés à son rôle (situés dans `orchestrator/agents/`).
4. **Action (Écriture)** : 
    - Si l'IA sort un `<DELEGATE>`, le script Python *crée de nouvelles lignes* dans le Notion et passe la tâche parente en `In Progress` ou `Completed`.
    - Si l'IA sort un `<ANTIGRAVITY_TASK>`, la tâche est marquée comme prête, et les instructions de code sont poussées sur votre ordinateur.

## 🛠️ Comment reproduire ce système pour d'autres projets

Ce système est agnostique au code et peut piloter n'importe quelle stack technique. Pour l'installer sur un tout nouveau projet "Projet B" :

### 1. Pré-requis sur Notion
Il vous faut une Base de données Notion (vue Tableau ou Kanban) avec au minimum les propriétés (colonnes) suivantes :
- `Name` (Titre)
- `Status` (Statut avec a minima : `Todo`, `In Progress`, `Completed`)
- `Catégorie` (Select ou Texte : `planner`, `architect`, `coder`)

### 2. Variables d'Environnement (`.env`)
Dans le même dossier que le script orchestrateur, créez un fichier `.env` ou instanciez ces variables dans votre terminal :
```ini
NOTION_TOKEN="secret_votre_token_integration_notion"
NOTION_DATABASE_ID="l_id_de_votre_board"
GEMINI_API_KEY="AIzaSy_votre_cle_api_gemini"
```
*(Pour obtenir un Notion Token, rendez-vous sur [Notion Integrations](https://www.notion.so/my-integrations) et pensez à "Connecter" l'intégration au layout de votre base de données en cliquant sur les `...` en haut à droite).*

### 3. Adaptation des Prompts
Si le nouveau projet est en Python/Django ou en Rust, vous devrez simplement Modifier le fichier `orchestrator/agents/coder.txt` pour lui indiquer le contexte technique. La logique des balises (`<DELEGATE>` et `<ANTIGRAVITY_TASK>`) **doit impérativement rester intacte**.

### 4. Lancement
Il ne vous reste plus qu'à faire tourner le script en tâche de fond pour qu'il surveille votre board Trello/Notion et agisse comme un chef de projet fantôme invisible :
```bash
python3 stackpulse_orchestrator.py
```
