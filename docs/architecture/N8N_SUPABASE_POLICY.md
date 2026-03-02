# Politique de Connexion Sécurisée : n8n -> Supabase

Ce document encadre les bonnes pratiques et la politique de sécurité pour la connexion entre l'instance n8n (Crawler) et notre base de données Supabase, comme défini dans l'US.4 du MVP StackPulse.

## 1. Topologie de Connexion
L'instance n8n utilise Supabase de deux manières distinctes :
1. **Stockage Interne de n8n** : n8n utilise la vue Postgres de Supabase pour stocker ses workflows, ses identifiants (Credentials) et son historique d'exécution. Pour cela, on utilise le schéma dédié `n8n` créé via la migration `00005`.
2. **Postgres Node (Supabase Ingestion)** : Les workflows n8n utilisent le Node "Postgres" ou "HTTP Request" (via API REST Supabase) pour l'ingestion de la donnée crawlé (Arxiv, GitHub, Blogs).

## 2. Accès et Droits (Role Based Access Control)
Pour des raisons de sécurité, nous utilisons la gestion des rôles (RLS - Row Level Security) de Supabase pour restreindre les droits d'écriture.

### 2.1 Rôle d'Ingestion
- **Rôle recommandé :** `service_role` (via le Service Role Key) ou un rôle customisé `n8n_ingestor`.
- **Méthode d'Authentification :** Les workflows n8n doivent inclure le token d'autorisation `Bearer <SERVICE_ROLE_KEY>` dans les en-têtes (headers) HTTP lors de l'appel à l'API REST de Supabase, **ou** utiliser des requêtes SQL directes via le nœud Postgres branché sur le rôle `postgres` (si n8n est hébergé de manière ultra-sécurisée).
- **Politique RLS :**
  ```sql
  CREATE POLICY "Service role can manage content items" 
  ON public.content_items FOR ALL 
  USING (current_setting('request.jwt.claims', true)::jsonb ->> 'role' = 'service_role');
  ```
  Cela garantit que l'insertion (upsert) dans `content_items` est exclusivement réservée à n8n (ou à nos Edge Functions). Le client web normal ne peut y accéder qu'en "Read-only".

## 3. Gestion des Identifiants (Credentials) au sein de n8n
n8n gère un portefeuille centralisé et chiffré des clés API :
- Les clés de connexion Supabase (`Project Ref`, `Service Role Key`, `Anon Key`).
- Les Personal Access Tokens GitHub (`GitHub PAT`) pour éviter le rate-limiting du crawler.
- Les identifiants proxy si applicables.

**Bonnes Pratiques :**
- **Ne jamais hardcoder** de clés (tokens, passwords) dans les workflows JSON n8n.
- Utiliser un `N8N_ENCRYPTION_KEY` aléatoire très fort (ex. `openssl rand -hex 24`), déclaré dans le fichier `.env` du docker-compose. Si cette clé est perdue, tous les credentials stockés seront inaccessibles.
- Limiter les scopes des PATs GitHub strictement à `read:user`, `repo` et `read:org`.

## 4. Ségrégation du Trafic (Webhook & Polling)
L'orchestration des données n8n peut être déclenchée :
- **Par Cron (Polling) :** n8n interroge périodiquement les apis cibles.
- **Par Webhook :** Supabase (via Database Webhook) ou GitHub envoient un signal sur un endpoint Webhook sécurisé de n8n. Le nœud Webhook de n8n doit toujours inclure une authentification par Header ou par authentification basique pour ne pas être déclenché publiquement.

## 5. System Health Logs
Pour assurer une observabilité complète :
- Les workflows n8n qui rencontrent une exception (nœud "Error Trigger") doivent s'achever par une insertion dans la table `system_health_logs` de Supabase.
- Une Edge Function Supabase (`notify-slack`) se charge alors d'écouter les insertions `system_health_logs` (où status = 'error' ou 'critical') via un Database Webhook, et pousse l'alerte sur Slack.
