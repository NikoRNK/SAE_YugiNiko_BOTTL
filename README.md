# SAE_YugiNiko_BOTTL
Bot télégram pour la SAE

https://www.canva.com/design/DAG7COKFTsE/c4LzgLoVFxi2GqNUO_0t6g/edit
https://github.com/NikoRNK/SAE_YugiNiko_BOTTL/
https://trello.com/b/f9dz16HI/sae-crypto-telegram

# SAETL – Bot Telegram avec IA & Ticketing Discord

Bot Telegram développé en Python pour analyser des informations, automatiser des commandes et logger automatiquement les erreurs dans un salon Discord sous forme de “tickets”.

> Projet réalisé dans le cadre de la SAE, à l’attention de monsieur M'LIK, enseignant à l'iut de Villetaneuse, sorbonne paris nord.

---

## 🚀 Fonctionnalités principales

- Bot Telegram basé sur `python-telegram-bot`
- Commandes dédiées (ex. `/help`, `/boom` de test)
- Gestion globale des erreurs avec un `error_handler` custom
- Envoi des exceptions vers Discord via **webhook** avec embeds
- Architecture modulaire : `handlers`, `services`, `error_handler`
- Préparation à l’intégration d’IA (analyse de marché, traitement de texte, etc.)

---

## ⚙️ Stack technique

- **Langage** : Python
- **Librairies clés** :
  - `python-telegram-bot` – gestion des commandes, updates et polling [web:1163]
  - `requests` – envoi des webhooks vers Discord [web:1169]
  - `logging`, `traceback`, `os` – logs, stacktraces, env
- **Intégrations** :
  - API Telegram (BotFather)
  - Webhook Discord pour le ticketing d’erreurs

---

## 🧩 Fonctionnement global

1. L’utilisateur envoie une commande sur Telegram (`/help`, `/boom`, etc.).
2. `python-telegram-bot` route la commande vers le handler correspondant.
3. Le handler exécute la logique métier.
4. En cas d’erreur :
   - l’exception remonte au `error_handler`,
   - l’erreur est loggée côté serveur,
   - un **embed** est envoyé dans un salon Discord via webhook (Update, Chat data, User data, Traceback).
5. Les développeurs suivent les erreurs directement dans Discord et peuvent les traiter comme des “tickets”.

---

## 💻 Installation & lancement

### 1. Cloner le dépôt

git clone https://github.com/NikoRNK/SAE_YugiNiko_BOTTL.git
cd SAE_YugiNiko_BOTTL

text

### 2. Créer et activer l’environnement virtuel

python -m venv .venv

Windows
.venv\Scripts\activate

Linux / macOS
source .venv/bin/activate

text

### 3. Installer les dépendances

pip install -r requirements.txt

text

### 4. Configurer les variables d’environnement

Créer un fichier `.env` à la racine :

BOT_TOKEN=TON_TOKEN_TELEGRAM_ICI
DISCORD_ERROR_WEBHOOK_URL=https://discord.com/api/webhooks/...

text

- `BOT_TOKEN` : récupéré via **BotFather** sur Telegram (`/newbot`) [web:1173]  
- `DISCORD_ERROR_WEBHOOK_URL` : créé dans les paramètres d’un salon Discord (Intégrations → Webhooks) [web:1175][web:1029]

### 5. Lancer le bot

python main.py

text

Tu dois voir dans la console :

Bot lancé. Ctrl+C pour arrêter.

text

---

## 📡 Commandes disponibles (exemples)

### `/help`

- Affiche la liste des commandes disponibles.
- Utilisé comme point d’entrée pour comprendre ce que le bot sait faire.

### `/boom`

- Commande de test pour la gestion des erreurs.
- Fait intentionnellement `1 / 0` pour provoquer une `ZeroDivisionError`.
- L’erreur est interceptée par `error_handler` et envoyée au salon Discord des logs.

---

## 🛑 Gestion des erreurs & logs Discord

Le fichier `bot/error_handler.py` centralise la gestion des exceptions :

- Log de l’erreur côté serveur (via `logging`).
- Récupération :
  - de l’`update` Telegram,
  - de `context.chat_data`,
  - de `context.user_data`,
  - de la stacktrace complète (`traceback.format_exception`).
- Envoi d’un **embed** formaté dans Discord avec :
  - Titre : `[SAETL Bot] Erreur Telegram`
  - Champs : Update, Chat data, User data, Traceback
  - Couleur rouge (`0xE74C3C`) pour signaler une erreur.

Cela permet de suivre tous les crashs dans un salon privé type `#logs-erreurs` sans spammer les utilisateurs.

---

## 👨‍💻 Ajouter une nouvelle commande

1. Créer un fichier dans `bot/handlers/`, par ex. `stats.py` :

from telegram import Update
from telegram.ext import ContextTypes

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
await update.message.reply_text("Statistiques en cours de dev...")

text

2. L’enregistrer dans `bot/handlers/__init__.py` (ou dans ta fonction `register_handlers`) :

from telegram.ext import CommandHandler
from .stats import stats

def register_handlers(app):
app.add_handler(CommandHandler("stats", stats))
# autres handlers...

text

3. Relancer le bot et tester `/stats` dans Telegram.

---

## 🔐 Sécurité & bonnes pratiques

- Les tokens, mots de passe et API keys **ne doivent jamais être committés** :
  - Ils sont placés dans `.env`
  - `.env` est listé dans `.gitignore`
- Le `.venv` n’est pas versionné (trop lourd, dépendant de la machine).
- Chaque personne qui utilise le bot doit **configurer son propre `.env`** avec ses clés.

---

## 🧠 Choix techniques & retours d’expérience

- **JS vs Python** :  
  On a hésité avec une version JS plus “jolie” côté apparence, mais Python s’est imposé pour :
  - la richesse d’outils (IA, data, automatisation),
  - la simplicité de gestion des handlers et de la logique backend.

- **Handlers automatiques** :  
  Pour éviter de répéter les commandes à la main dans `/help`, un système de handlers centralisés simplifie l’ajout de nouvelles fonctionnalités.

- **Git & merges** :  
  Après quelques galères (branches multiples, historiques différents), le workflow a été simplifié :
  - une branche principale `main`,
  - un remote clair,
  - et l’utilisation de `git reflog` au besoin pour récupérer une branche “perdue” [web:1136][web:1141].

---

## 🛠 Pistes d’amélioration

- Ajout d’une vraie base de données (état utilisateurs, historique, configs).
- Bot Discord complet pour réagir aux emojis sur les tickets d’erreurs.
- Intégration IA plus poussée (analyse de marché, résumés, scoring).
- Déploiement sur un hébergeur (Railway, Render, etc.) pour un bot 24/7 [web:1177].
- Ajout de tests (pytest) et pipeline CI simple.

---

## 👥 Contact / Crédit

- Développement : équipe SAETL  
- Repo : `https://github.com/NikoRNK/
