# LAXA MONOSCRIPT IDE (Frontend) 🚀

Ce dépôt contient le code source du frontend pour **MONOSCRIPT IDE**, un environnement de développement web conçu pour le langage de programmation personnalisé MONOSCRIPT. L'application est construite avec React, TypeScript et Tailwind CSS, et intègre un éditeur de code avancé avec coloration syntaxique sur mesure.

## ✨ Fonctionnalités

  * **IDE Web Complet** : Une interface utilisateur moderne et réactive.
  * **Éditeur de Code Avancé** : Intégration de CodeMirror avec coloration syntaxique personnalisée.
  * **Fenêtres Interactives** : L'éditeur et le terminal peuvent être fermés, minimisés, maximisés et restaurés.
  * **Barre d'Outils ("Dock")** : Un dock latéral pour gérer la visibilité des fenêtres.
  * **Communication API** : Prêt à communiquer avec un backend pour l'exécution du code.
  * **Déploiement Dockerisé** : Un `Dockerfile` optimisé pour un déploiement facile avec Nginx.

-----

## 💻 Technologies utilisées

| Technologie    | Description                                             |
| :------------- | :------------------------------------------------------ |
| **React** | Bibliothèque pour construire l'interface utilisateur.      |
| **TypeScript** | Pour un code robuste et typé.                           |
| **Vite** | Outil de build et serveur de développement ultra-rapide.  |
| **Tailwind CSS**| Framework CSS pour un design rapide et moderne.         |
| **CodeMirror** | Éditeur de code avancé avec coloration syntaxique.      |
| **Docker** | Pour conteneuriser l'application pour le déploiement.      |

-----

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils et les connaissances de base suivants.

### Outils Logiciels

  * **Éditeur de Code** : Un éditeur moderne comme [**VS Code**](https://code.visualstudio.com/).
  * **Node.js** : Version 18 ou supérieure. Vous pouvez le télécharger sur [**nodejs.org**](https://nodejs.org/).
  * **Git** : Pour la gestion de version et le clonage du projet. À installer depuis [**git-scm.com**](https://git-scm.com/).
  * **Docker Desktop** : Nécessaire pour construire et lancer l'application en conteneur (localement ou pour le déploiement). À installer depuis [**docker.com**](https://www.docker.com/products/docker-desktop/).

### Connaissances Requises

  * Des connaissances de base en **React** et **TypeScript**.
  * Une familiarité avec l'utilisation de la **ligne de commande** (terminal).
  * Des notions de base de **Git** (clone, add, commit, push).

-----

## ⚙️ Lancement en Local

Pour lancer le projet sur votre machine :

1.  **Clonez le projet** et naviguez dans le dossier `frontend`.

2.  **Installez les dépendances** :

    ```bash
    npm install
    ```

3.  **(Une seule fois) Compilez la grammaire** :
    Ce projet utilise une grammaire personnalisée. Vous devez la compiler au moins une fois :

    ```bash
    npm run build:grammar
    ```

    *Relancez cette commande si vous modifiez le fichier `src/monoscript.grammar`.*

4.  **Lancez le serveur de développement** :

    ```bash
    npm run dev
    ```

    L'application sera accessible sur `http://localhost:5173`.

-----

## 🐳 Déploiement

Le projet est conçu pour être déployé facilement avec Docker.

### 1\. Déploiement en Local avec Docker

Pour tester l'image de production sur votre machine locale :

1.  **Construisez l'image Docker :**

    ```bash
    docker build -t monoscript-frontend .
    ```

2.  **Lancez le conteneur :**

    ```bash
    docker run -d -p 8080:80 --name monoscript-local monoscript-frontend
    ```

    L'application sera accessible sur `http://localhost:8080`.

### 2\. Déploiement sur un Serveur de Production

Pour déployer ou mettre à jour l'application sur votre serveur :

1.  **Envoyez vos modifications sur Git** (depuis votre machine locale) :

    ```bash
    git add .
    git commit -m "Description de vos changements"
    git push
    ```

2.  **Connectez-vous à votre serveur en SSH** :

    ```bash
    ssh utilisateur@ip_du_serveur
    ```

3.  **Sur le serveur, mettez à jour le code et redéployez** :

    ```bash
    # Naviguez dans le dossier du projet
    cd chemin/vers/votre/projet/frontend

    # Récupérez les dernières modifications depuis Git
    git pull

    # Reconstruisez l'image Docker
    docker build -t monoscript-frontend .

    # Arrêtez et supprimez l'ancien conteneur
    docker stop monoscript-app && docker rm monoscript-app

    # Lancez le nouveau conteneur
    docker run -d -p 80:80 --restart always --name monoscript-app monoscript-frontend
    ```

    L'application est maintenant à jour et accessible via l'adresse IP de votre serveur.

-----

## 📄 Licence

Ce projet est sous licence MIT.