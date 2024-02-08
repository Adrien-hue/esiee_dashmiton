# Dashmiton - Projet de Data Engineering

## Description du Projet
Dashmiton est un projet de data engineering axé sur l'extraction de données à partir du site Marmiton. Ce projet vise à collecter des informations sur les recettes culinaires disponibles sur Marmiton, puis à les visualiser dans un tableau de bord interactif.

## Étapes d'Installation

1. **Téléchargement du Projet :**
   Utilisez la commande suivante pour cloner le projet à partir du dépôt GitHub :
   ```bash
   git clone https://github.com/Adrien-hue/esiee_dashmiton.git
   ```

2. **Démarrage de Docker :**
   Assurez-vous que Docker est installé sur votre machine, puis démarrez Docker.

3. **Lancement du Scrapping et du Dashboard :**
   Utilisez la commande suivante pour démarrer le scrapping et le dashboard en utilisant Docker Compose :
   ```bash
   docker compose up
   ```

4. **Accès au Dashboard :**
   Une fois le processus terminé, accédez au tableau de bord en ouvrant votre navigateur et en naviguant vers [http://localhost:5000](http://localhost:5000).

## Structure du Projet

Le projet est organisé de la manière suivante :
- **`scraper/` :** Contient les scripts de scrapping pour extraire les données de Marmiton.
- **`dashboard/` :** Contient les fichiers nécessaires à la création du tableau de bord interactif.
- **`compose.yaml` :** Fichier de configuration Docker Compose pour orchestrer le déploiement.


## Auteurs

- [Adrien Hue](https://github.com/Adrien-hue)
- [Thibault BLANCHARD](https://github.com/Hellferno36)

Merci d'avoir choisi Dashmiton pour votre exploration de données culinaires! Bon appétit! 🍲