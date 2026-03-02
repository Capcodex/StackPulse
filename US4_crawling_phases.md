# Plan d'exécution : US.4 Crawler n8n

Voici la réorganisation des sous-tâches générées par l'orchestrateur (depuis `tasks_to_code.md`) en plusieurs phases logiques. Chaque phase dépend de la précédente.

### Légende
- 🤖 **Automatisable par l'Agent** : L'IA peut générer le code, exécuter les scripts, modifier les fichiers locaux.
- 🧑‍💻 **INTERVENTION HUMAINE REQUISE** : Actions nécessaires de votre côté dans une interface (Dashboard Supabase, n8n UI, etc.) ou validation requise.

---

## 🏗️ Phase 1 : Infrastructures et Base de Données (Fondations)
*Objectif : Mettre en place les tables, les politiques d'accès (RLS) et les types TypeScript nécessaires pour accueillir les futures données.*

- [ ] 🤖 Proposer le modèle de données détaillé (GitHub, Arxiv, Blogs).
- [ ] 🤖 Définir et implémenter le schéma de base de données unifié (`content_items`), ainsi que les tables d'ingestion avec contraintes UNIQUE pour l'upsert.
- [ ] 🤖 Implémenter les migrations SQL correspondantes et générer les types TypeScript.
- [ ] 🤖 Créer les politiques RLS (Row Level Security) :
  - Accès Read-only pour les utilisateurs (public / authentifiés).
  - Accès en écriture sans restriction pour le rôle "service_role" (utilisé par n8n).
- [ ] 🤖 Configurer le rôle et le schéma spécifiques à `n8n` dans Supabase.
- [ ] 🧑‍💻 **INTERVENTION HUMAINE** : Exécuter les migrations SQL dans le dashboard Supabase (ou via la CLI si connectée) et valider la création des tables.

---

## ⚙️ Phase 2 : Configuration n8n et Connectivité
*Objectif : Lancer l'environnement n8n et le connecter de manière sécurisée à Supabase et aux autres APIs.*

- [ ] 🤖 Créer / Vérifier le fichier `docker-compose.yml` incluant n8n et Redis.
- [ ] 🤖 Créer la documentation (`docs/architecture/N8N_SUPABASE_POLICY.md`) expliquant les modalités de connexion sécurisée n8n -> Supabase.
- [ ] 🤖 Définir les variables d'environnement nécessaires pour n8n.
- [ ] 🧑‍💻 **INTERVENTION HUMAINE** :
  - Démarrer les conteneurs Docker (`docker-compose up -d`).
  - Mettre en place la gestion sécurisée des identifiants (GitHub PAT, clés proxy, identifiants base de données) directement **dans l'interface UI de n8n** (Credentials).
  - Configurer les nœuds de connexion Supabase (PostgreSQL node) dans n8n.

---

## 🕷️ Phase 3 : Workflows de Crawling
*Objectif : Créer les logiques de récupération et de nettoyage des données.*

- [ ] 🤖 Établir la stratégie d'ingestion des données depuis n8n vers la base de données (upsert, détection des doublons).
- [ ] 🤖 Mettre au point la logique (JSON/Scripts) du workflow n8n pour le crawling **Arxiv** (articles, abstracts, auteurs).
- [ ] 🤖 Mettre au point la logique (JSON/Scripts) du workflow n8n pour le crawling **GitHub** (dépôts pertinents).
- [ ] 🤖 Implémenter les étapes de transformation et de normalisation des données au sein de n8n pour matcher le schéma unifié (Phase 1).
- [ ] 🧑‍💻 **INTERVENTION HUMAINE** :
  - Importer les fichiers JSON des workflows générés dans l'interface de n8n.
  - Tester les workflows manuellement en UI et vérifier l'insertion dans Supabase.

---

## 🛡️ Phase 4 : Monitoring, Error Handling et Alerting
*Objectif : S'assurer que les workflows tournent correctement et être alerté des problèmes.*

- [ ] 🤖 Concevoir la stratégie de gestion des erreurs pour les workflows n8n.
- [ ] 🤖 Créer la table `system_health_logs`.
- [ ] 🤖 Créer une Edge Function `notify-slack` qui gère les alertes.
- [ ] 🤖 Configurer le Database Webhook de Supabase pour déclencher la fonction `notify-slack` lors d'une insertion (ERREUR) dans `system_health_logs`.
- [ ] 🤖 Implémenter le wrapper Supabase avec gestion d'erreurs automatique dans `lib/supabase-client.ts` (déjà partiellement fait, à consolider).
- [ ] 🧑‍💻 **INTERVENTION HUMAINE** : Déployer l'Edge Function `notify-slack` et ajouter le webhook de votre Slack dans les secrets Supabase.

---

## 💾 Phase 5 : Sauvegarde et Maintenance (Optionnel MVP)
*Objectif : Assurer la pérennité temporelle des workflows n8n et le respect des quotas.*

- [ ] 🤖 Définir la structure du schéma pour les backups de workflows (`backups` et `backup_logs`).
- [ ] 🤖 Développer une Edge Function (TypeScript) pour exporter les workflows au format JSON depuis l'API n8n.
- [ ] 🤖 Configurer le déclencheur CRON et la logique de nettoyage automatique.
- [ ] 🧑‍💻 **INTERVENTION HUMAINE** : Déployer ces Edge Functions de backup et planifier le cron (via pg_cron ou le dashboard d'Edge Functions).

---

## 🟢 Prochaine étape recommandée

Si cette découpe vous convient, je peux commencer immédiatement par la **Phase 1 (Modélisation et Base de données)**.
Voulez-vous que je vide `tasks_to_code.md` pour éviter les doublons avec ce nouveau document clair ?
Puis-je attaquer la création du schéma unifié ?
