# 🚀 Déploiement de n8n sur un VPS Linux

Cette documentation vous guide pas à pas pour déployer de manière sécurisée et robuste le moteur d'ingestion `n8n` sur votre serveur Linux (Ubuntu/Debian) via GitHub et Docker.

> [!IMPORTANT]
> Assurez-vous d'être connecté à votre VPS en SSH (`ssh root@votre-ip-vps`) avant de commencer.

## Prérequis sur le serveur

Votre VPS doit avoir `git`, `docker` et `docker compose` installés. Si ce n'est pas le cas, exécutez ces commandes :

```bash
# Mettre à jour la liste des paquets
sudo apt update && sudo apt upgrade -y

# Installer Git
sudo apt install git -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installer Docker Compose
sudo apt install docker-compose-plugin -y
```

## Étape 1 : Récupérer le code depuis GitHub

Le moyen le plus propre et le plus simple est de cloner votre dépôt Git contenant la configuration exacte que nous venons de préparer ensemble.

```bash
# Placez-vous dans le répertoire de votre choix (ex: /opt)
cd /opt

# Clonez le répertoire (remplacez par votre URL de dépôt)
# Si votre dépôt est privé, GitHub vous demandera votre username et un Personal Access Token.
git clone https://github.com/Capcodex/StackPulse.git

# Entrez dans le dossier configuré pour le crawler
cd StackPulse/n8n
```

## Étape 2 : Configurer les identifiants (Le fichier .env)

Sur Git, le mot de passe de la base de données n'est (ou ne devrait jamais être) sauvegardé localement par sécurité (`.env` est souvent ignoré via `.gitignore`). Il faut donc créer le fichier d'environnement sur le serveur.

1. Copiez le template :
```bash
cp .env.example .env
```
2. Éditez le fichier pour insérer le mot de passe de votre base de données Supabase (`tEGkwqdLfKIpIfXL` dans notre cas) :
```bash
nano .env
```
Assurez-vous que les lignes suivantes sont bien renseignées :
```env
DB_POSTGRESDB_HOST=db.gxuoceuryofmiuyrkmfn.supabase.co
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_USER=postgres
DB_POSTGRESDB_PASSWORD="votre_mot_de_passe_supabase"
```
Quittez `nano` en faisant `Ctrl+X`, puis `Y` (ou `O`) et `Entrée`.

## Étape 3 : Lancer le conteneur n8n

Maintenant que Docker et la configuration sont prêts, lancez la machine autonome :

```bash
# Lancer les services (n8n + redis) en tâche de fond (-d pour detached)
docker compose up -d

# Visualiser les logs pour s'assurer que n8n se connecte bien à Supabase
docker compose logs -f n8n
```
Si vous voyez `n8n ready on ::, port 5678`, c'est gagné ! ✅ (Faites `Ctrl+C` pour quitter les logs).

## Étape 4 : Ouvrir les ports du serveur (Firewall)
Si votre VPS possède un pare-feu (ex: UFW sur Ubuntu), vous devez autoriser le port `5678` pour pouvoir accéder à l'interface depuis votre navigateur :

```bash
sudo ufw allow 5678/tcp
```

## Étape 5 : Importer les workflows

1. Depuis votre PC, ouvrez votre navigateur et tapez : `http://VOTRE_IP_VPS:5678`
2. Configurez votre compte administrateur (c'est une instance toute neuve sur le VPS).
3. Cliquez sur `...` > `Import from File`.
4. Sélectionnez les fichiers `01_github_crawler.json` et `02_arxiv_crawler.json` depuis le code source de votre ordinateur local.
5. Sur les nœuds `Postgres`, créez votre *Credential* avec l'URL directe de Supabase, le port 5432, le user `postgres` et son mot de passe, Activez et c'est parti ! 🚀
