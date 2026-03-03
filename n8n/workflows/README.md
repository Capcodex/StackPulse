# Workflows n8n pour StackPulse

Ce dossier contient les modèles de workflows d'ingestion (crawlers) pour le projet StackPulse.
L'objectif est d'extraire la donnée des sources sélectionnées (GitHub, Arxiv), de la normaliser pour correspondre au schéma `content_items` défini dans Supabase, puis de l'insérer avec une logique d'Upsert (mise à jour si existant, insertion sinon).

## 1. Modélisation attendue par Supabase (`content_items`)
Chaque noeud final de workflow (Nœud Postgres / Supabase) doit insérer un objet JSON avec cette structure :

| Champ Supabase | Type | Contenu Exemple |
| :--- | :--- | :--- |
| `source_platform` | TEXT | `'github'`, `'arxiv'`, ou `'blog'` |
| `source_id` | TEXT | ID unique fourni par l'API (ex: `repo.id` ou `entry.id`) |
| `type` | TEXT | `'repository'`, `'article'`, etc. |
| `url` | TEXT | L'URL canonique de la ressource |
| `title` | TEXT | Titre de l'article ou Nom du repo |
| `content` | TEXT | Description de repo ou Abstract Arxiv (Résumé) |
| `author` | JSONB | `{"name": "John Doe", "url": "..."}` |
| `tags` | TEXT[] | `{"machine-learning", "python"}` |
| `metadata` | JSONB | Données brutes utiles (ex: `{"stars": 1500, "forks": 200}`) |
| `published_at` | TIMESTAMPTZ | Date de publication / création originale |

*Note: La base de données gère l'unicité via la contrainte `(source_platform, source_id)`. Une tentative d'insertion d'un doublon lèvera soit une erreur (qu'on peut catch et logger), soit on utilise l'opération "Upsert" du noeud Postgres de n8n.*

---

## 2. Crawler GitHub (`01_github_crawler.json`)
⚠️ **Pré-requis :** Ajouter vos "Credentials" dans n8n (Header Auth `Authorization: Bearer VOTRE_PAT`).

**Fonctionnement (Etapes du Workflow) :**
1. **Schedule Trigger :** S'exécute tous les jours (ou déclenché manuellement/webhook).
2. **HTTP Request :** Interroge l'API GitHub Search `https://api.github.com/search/repositories?q=language:typescript+stars:>500+created:>LAST_WEEK&sort=stars&order=desc`.
3. **Item Lists :** Sépare le tableau `items` en plusieurs objets n8n distincts pour les itérer.
4. **Set (Normalize Data) :** Transforme le JSON GitHub en JSON `content_items`.
   - `source_platform` = `'github'`
   - `source_id` = `{{ $json.id.toString() }}`
   - `type` = `'repository'`
   - `url` = `{{ $json.html_url }}`
   - `title` = `{{ $json.full_name }}`
   - `content` = `{{ $json.description }}`
   - `published_at` = `{{ $json.created_at }}`
5. **Postgres Node (Supabase) :** Fait un "Upsert" dans la table `content_items`.

---

## 3. Crawler Arxiv (`02_arxiv_crawler.json`)
⚠️ **Pré-requis :** L'API export d'Arxiv renvoie du XML.

**Fonctionnement (Etapes du Workflow) :**
1. **Schedule Trigger :** S'exécute tous les jours.
2. **HTTP Request :** Requête API REST: `http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=lastUpdatedDate&sortOrder=descending&max_results=50`.
3. **XML Parser :** Convertit la réponse brute XML en objet JSON.
4. **Item Lists :** Sépare les entrées (`entry`).
5. **Set (Normalize Data) :**
   - `source_platform` = `'arxiv'`
   - `source_id` = `{{ $json.id }}`
   - `type` = `'article'`
   - `url` = `{{ $json.id }}`
   - `title` = `{{ $json.title }}`
   - `content` = `{{ $json.summary }}`
   - `published_at` = `{{ $json.published }}`
6. **Postgres Node (Supabase) :** "Upsert" vers `content_items`.

---

## 🛠️ Instructions d'Importation
Pour importer ces workflows dans votre instance n8n tournant sur `localhost:5678` :
1. Créez un nouveau workflow vide dans n8n.
2. Cliquez sur l'icône de menu (trois petits points) en haut à droite > **Import from File**.
3. Sélectionnez le fichier `.json` correspondant dans ce répertoire.
4. **Configurez les Credentials** : n8n vous demandera d'assigner vos credentials Postgres (Supabase) aux noeuds finaux. Sélectionnez ou créez un compte `Postgres`.
5. Activez (bouton toggle en haut à droite) et Sauvegardez le workflow !
