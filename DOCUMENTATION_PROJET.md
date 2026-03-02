# StackPulse - Documentation Projet V1 MVP

## 1. Vision Générale (Cahier des Charges - Livrable 8)
**Projet :** StackPulse (V1 MVP)
**Stack Technologique :** Next.js / Tailwind / Supabase / CrewAI / n8n

### A. Le Profil "Digital Twin"
- **Onboarding :** Connexion via Supabase Auth (Magic Link ou GitHub).
- **Saisie de la Stack :** Sélection rapide par tags (ex: *Snowflake, dbt, Python*).
- **Import Contextuel :** Upload de `requirements.txt`/`package.json` ou connexion Google Drive API.

### B. Le Skill-Gap Analyzer (Priorité n°1)
- L'utilisateur définit un rôle cible (ex: *"Passer de Data Engineer à AI Architect"*).
- Un agent CrewAI compare la stack actuelle à l'objectif.
- Visualisation via un Graphe radar (5 axes : Infra, Code, IA, Data Ops, Stratégie).
- Plan d'action avec 3 technos prioritaires à apprendre.

### C. Le Dashboard de Veille Agentique
- **Le "Radar" :** Flux de cartes taguées (*🔥 Disruptif, ✅ Mature, ⚠️ Risqué*).
- **Le "Bench Flash" :** Comparaison immédiate avec la stack actuelle de l'utilisateur (via n8n orchestrant CrewAI).
- **Filtres intelligents :** "Utile pour mon job" vs "Utile pour mon plan de carrière".

### Direction Artistique (UI/UX)
- **Style :** "Engineering Aesthetic" (Fond noir `#000000`, accents `Geist Sans`, bordures `gray-800`).
- **Composants :** Shadcn/ui.
- **Interactions :** Framer Motion pour les loaders et transitions IA.

---

## 2. Backlog de User Stories (Livrable 9)

### 🏗️ Epic 1 : Configuration du "Digital Twin"
- **US.1 :** Sélection par tags (filtre des news).
- **US.2 :** Connexion API (GitHub/Drive) pour extraction manuelle.
- **US.3 :** Définition du Persona (Builder vs Leader).

### 🧠 Epic 2 : Le Moteur d'Intelligence (CrewAI & n8n)
- **US.4 :** Crawler n8n (GitHub, Arxiv, Blogs).
- **US.5 :** Calcul de l'"Impact Score" personnalisé (CrewAI).
- **US.6 :** Tableau comparatif Pros/Cons (Perf, Coût, Effort).

### 💻 Epic 3 : Le Dashboard Adaptatif (UI React)
- **US.7 :** Flux de news ordonné par pertinence (skeleton, infinite scroll).
- **US.8 :** Vue "Strategic Snapshot" (graphique maturité + résumé IA pour Décideurs).
- **US.9 :** Sauvegarde (Bookmark / Backlog d'apprentissage).

### 📈 Epic 4 : Actionnabilité & Pilotage (Stratégie)
- **US.10 :** Export synthèse "Briefing" (PDF/Link).
- **US.11 :** Visualisation "Skill-Gap" (Radar + Recos).
- **US.12 :** Score de conformité AI Act (Badge + Alertes).

---

---

## 4. Cahier des Charges Techniques (Livrable 10)

### Architecture de la Stack
- **Front-end & API :** Next.js 15+ (App Router), Server Actions (Supabase), Route Handlers (n8n).
- **Styling :** Tailwind CSS + Shadcn/ui.
- **Back-end & DB :** Supabase (PostgreSQL) avec RLS et Vaults (API Keys).
- **Intelligence Agentique :**
  - **Orchestration :** n8n (workflows asynchrones).
  - **Agents :** CrewAI.
  - **Context :** Protocoles MCP (connexion aux docs live comme GitHub/Slack).
- **Déploiement :** Vercel (Front) et Docker/Railway (n8n/Python).

### Schéma de la Base de Données (Supabase)
- **`profiles` :** `id` (uuid, PK), `email`, `persona`, `onboarding_completed`.
- **`user_stacks` :** `id` (uuid), `user_id` (FK), `tech_id` (string), `category` (string), `version` (string).
- **`news_insights` :** `id` (uuid), `source_url`, `title`, `raw_content`, `embedding` (vector text).
- **`custom_analyses` :** `id` (uuid), `user_id` (FK), `insight_id` (FK), `impact_score` (int), `analysis_json` (Pros/Cons), `status`.

### Architecture des Flux de Données
1. **Ingestion :** n8n scanne les sources (RSS, Twitter, MCP GitHub).
2. **Filtrage :** CrewAI compare les mots-clés de la news avec les technos globales.
3. **Analyse :** Si match, n8n récupère la stack utilisateur et CrewAI ("Senior Architect") rédige le rapport.
4. **Notification :** Mise à jour Supabase et Realtime Update sur le front React.

### Protocoles de Sécurité & API
- **Auth :** Supabase Auth (OAuth GitHub/LinkedIn).
- **Data Privacy :** Chiffrement des tokens (Notion/Drive) via Supabase Vaults.
- **Performances & IA :**
  - Vercel AI SDK pour le streaming UI.
  - Extension `pgvector` pour la recherche sémantique basée sur l'historique utilisateur.
  - Protocoles MCP pour sourcer les limites techniques réelles depuis les repos.

---

---

## 5. Spécifications UI/UX (Livrable 11)

### Le Design System
- **Couleurs :** Fond `#000000`, Bordures `gray-800`.
- **Accents :** `indigo-500` (Primaire), `emerald-500` (Succès/Gain), `amber-500` (Risque).
- **Typographie :** Geist Sans (ou Inter).
- **Composants (Shadcn/ui) :** 
  - Cartes : `bg-gray-900/50` + backdrop-blur.
  - Table (Comparatifs), Sheet (Vue Deep Dive), Badge (Scores), Tabs (Persona).

### Écrans Principaux
1. **Le Dashboard "Radar" (Vue 1) :**
   - **Sidebar :** Navigation + Indicateur Agent "CrewAI scanning...".
   - **Feed Grid :** Cartes d'actu (Bento/Liste) contenant Titre, Meta (Temps lecture AI), et Impact Score circulaire.
   - **Filtres :** "All", "My Stack Only", "Career Boost".
2. **La Vue "Deep Dive" / Bench (Vue 2) :**
   - Panel `Sheet` ouvert latéralement via clic sur une news.
   - **Anatomie :** Context ("Replaces / Augments"), Synthèse IA (3 bullets), Tableau Comparatif Pros/Cons, CTAs d'action.
3. **Le Profil "Digital Twin" (Vue 3) :**
   - Visualiseur de stack (Graph Node type React Flow).
   - Zone Drag&Drop pour upload de `requirements.txt` / `docker-compose.yml`.
   - Animation de scan IA générant les tags automatiquement.

### UX "Agentique" (2026 Vibes)
- Skeletons `shimmer` très fins pendant le chargement IA.
- Toasts de notification proactifs des agents (ex: "Agent found 15% cost saving").
- Raccourci `CMD+K` (Focus mode) pour recherche/bench direct.

---

---

## 6. Roadmap MVP (Jalons & Périmètre) - Livrable 12

### 🟢 Jalon 1 : Version Alpha "Foundations" (Mois 1)
**Objectif :** Valider la chaîne technique complète (End-to-End) avec saisie manuelle.
- **Périmètre :**
  - **Auth :** Login/Signup Supabase.
  - **Profil :** Saisie manuelle de la stack via tags.
  - **Moteur :** Scraping simple (n8n via RSS) + DB.
  - **UI :** Dashboard minimaliste (liste filtrée).
- **Priorités :** Persistance DB et pertinence du filtrage.

### 🟡 Jalon 2 : Version Beta "Intelligence" (Mois 2)
**Objectif :** Délivrer la valeur ajoutée (Pros/Cons) à un groupe restreint.
- **Périmètre :**
  - **IA :** Intégration CrewAI (Impact Score, rapports).
  - **UI/UX :** Side-sheet (deep dive) et animations.
  - **Feedback :** Boutons "Pertinent / Non Pertinent".
  - **Notifs :** Alertes Email pour "Impact Fort".
- **Priorités :** Qualité de synthèse IA et latence (< 15s).

### 🔵 Jalon 3 : Version 1.0 "Market Ready" (Mois 3)
**Objectif :** Automatiser l'onboarding et cibler les décideurs.
- **Périmètre :**
  - **Connecteurs :** GitHub (MCP), Google Drive.
  - **Skill-Gap :** Lancement dashboard carrière.
  - **Vue Stratégique :** Dashboard CDO (ROI, Risques).
  - **Export :** Génération de Briefing (MD/Notion).
  - **Landing Page :** Go-to-market.
- **Priorités :** "Digital Twin" 100% automatique et robustesse.

---

---

## 7. Backlog Exécutable (Sprint 1 & 2) - Livrable 13

### 🏃 Sprint 1 : Foundations & Data Ingestion
**Objectif :** Avoir un environnement fonctionnel (stockage de stack + news brutes).
- [ ] **T1.1 (DevOps):** Initialisation Next.js 15 + Tailwind + Shadcn/ui. *(Effort: 1)* - **(En cours/Fait)**
- [ ] **T1.2 (Backend):** Setup projet Supabase + Création tables `profiles`, `user_stacks`. *(Effort: 2)*
- [ ] **T1.3 (Auth):** Implémentation Supabase Auth (Magic Link) + Redirection. *(Effort: 2)*
- [ ] **T1.4 (Frontend):** Création formulaire "Stack Fingerprint" (Multi-select/Tags). *(Effort: 3)*
- [ ] **T1.5 (n8n):** Workflow d'ingestion (RSS $\rightarrow$ Nettoyage $\rightarrow$ DB `news_insights`). *(Effort: 4)*
- [ ] **T1.6 (Backend):** Vue SQL/Fonction filtrage `get_relevant_news(uid)`. *(Effort: 3)*

### 🏗️ SPIKE TECHNIQUE (Avant Sprint 2)
**"Interfaçage n8n $\leftrightarrow$ CrewAI via Docker"**
- Valider le pont entre n8n et l'environnement Python de CrewAI (via *"Execute Command"* ou micro-service FastAPI) pour éviter de bloquer le Sprint 2.

### 🏃 Sprint 2 : Agentic Intelligence & UI
**Objectif :** Faire tourner CrewAI pour les premiers rapports d'impact (Pros/Cons).
- [ ] **T2.1 (AI):** Config Agent CrewAI "Architect" (Prompt engineering & Scoring). *(Effort: 5)*
- [ ] **T2.2 (n8n/AI):** Workflow: Trigger news $\rightarrow$ Analyse CrewAI $\rightarrow$ DB `custom_analyses`. *(Effort: 4)*
- [ ] **T2.3 (Frontend):** Dev du Feed React (Cartes + Impact Score). *(Effort: 3)* - **(En cours/Fait)**
- [ ] **T2.4 (Frontend):** Implémentation "Deep Dive Sheet" (Détail Markdown). *(Effort: 3)* - **(En cours/Fait)**
- [ ] **T2.5 (Backend):** Setup Supabase Realtime pour modif UI au push d'analyse. *(Effort: 2)*
- [ ] **T2.6 (UX/QA):** Bug hunting (Skeletons, erreurs LLM). *(Effort: 3)*

---

## 8. Architecture du MVP (Codebase & CI/CD) - Livrable 15

### Structure du Projet (Next.js 15+ App Router)
Pour une scalabilité maximale, on adopte une structure modulaire :
- `/app` : Routes, Layouts et Server Actions.
- `/components/ui` : Composants atomiques (Shadcn/ui).
- `/components/features` : Blocs métier (Dashboard, StackSelector, AI-DeepDive).
- `/hooks` : Logique Supabase (ex: `useStack.ts`, `useNews.ts`).
- `/lib` : Utilitaires (API clients, formatage de données).
- `/services` : Logique métier complexe (Appels n8n, Parsing).

### Pipeline CI/CD automatisé (GitHub Actions)
1. **Build & Lint :** Vérification Typescript/Tailwind au Push.
2. **Staging (Vercel Preview) :** Création d'environnement par branche pour QA.
3. **Production :** Déploiement Vercel automatique au merge sur `main`.
4. **Database :** Synchronisation automatique des schémas Supabase (Migrations SQL).

### Flow de Données "Agentic"
1. **Trigger :** n8n récupère une news $\rightarrow$ DB Supabase.
2. **Analyse :** n8n appelle CrewAI (via Docker/FastAPI) $\rightarrow$ Génération JSON.
3. **Push :** Supabase Webhook/Realtime $\rightarrow$ Next.js.
4. **Display :** Affichage live côté client (badge "New Insight").

---

## 9. Cahier de Recette (QA) - Livrable 16

Pour garantir un MVP robuste, chaque fonctionnalité doit passer ces tests :

| **ID** | **Fonctionnalité** | **Action Test** | **Résultat Attendu** |
| --- | --- | --- | --- |
| **QA.1** | Auth Flow | Connexion via Magic Link. | Redirection vers le Dashboard avec profil chargé. |
| **QA.2** | Stack Fingerprint | Sélectionner 3 technos et sauvegarder. | Technos apparaissent dans `user_stacks` (DB). |
| **QA.3** | News Filtering | Simuler une news sur "dbt". | News visible uniquement pour le profil "dbt". |
| **QA.4** | AI Analysis | Ouvrir le Side-sheet d'une news. | Tableau Pros/Cons rempli et lisible (Markdown). |
| **QA.5** | Realtime | Ajouter une news en DB manuellement. | La carte apparaît sur le Dashboard sans F5. |
| **QA.6** | Mobile UX | Ouvrir le Dashboard sur mobile. | Sidebar devient menu burger, grille 1 colonne. |

### 🛠️ Résilience IA (Focus QA.4)
**Criticité :** Le point de défaillance majeur est le formatage du JSON renvoyé par CrewAI brisant l'UI React.
**Solution (Zod) :** Utilisation obligatoire de schémas **Zod** pour valider strictement le payload JSON sortant de n8n/CrewAI avant l'insertion dans Supabase. Si la validation échoue, déclencher une logique de "Retry" sur l'agent.

---

## 10. Plan d'Action Actuel
- Focus technique sur le **Sprint 1 (Fondations)**.
- Les bases UI du Sprint 2 (T2.3, T2.4) sont déjà partiellement mockées pour visualiser le MVP.
- Prochaine étape critique technique : **T1.2 (Setup Supabase)** et intégration des schémas de validation **Zod**.
