# DESCRIPTION DE BASE DU PROJET

## BON A SAVOIR 
- backend/README.md
- frontend/README.md
- ./README.md

-----

## 🛠️ Prérequis

### Outils Logiciels

  * **Éditeur de Code** : [**VS Code**](https://code.visualstudio.com/) est recommandé.
  * **Node.js** : Version 18+ ([**nodejs.org**](https://nodejs.org/)).
  * **Python** : Version 3.8+ ([**python.org**](https://www.python.org/)).
  * **Git** : Pour la gestion de version ([**git-scm.com**](https://git-scm.com/)).
  * **Docker Desktop** : Pour le déploiement ([**docker.com**](https://www.docker.com/products/docker-desktop/)).

### Connaissances Requises

  * Connaissances de base en **React**, **TypeScript** et **Python**.
  * Familiarité avec la **ligne de commande** (terminal).
  * Notions de base de **Git** (clone, pull, push).

-----

## 💻 Technologies utilisées

| Catégorie | Technologie | Description |
| :--- | :--- | :--- |
| **Frontend** | React, TypeScript, Vite | Pour une interface utilisateur moderne, rapide et robuste. |
| | Tailwind CSS, CodeMirror | Pour le design et l'édition de code avancée. |
| **Backend** | Python, Flask | Pour l'interpréteur du langage et l'API. |
| **Déploiement** | Docker, Git | Pour conteneuriser et versionner l'application. |

## ⚙️ Installation et Lancement

### Lancement en Local

Pour travailler en local, vous devrez lancer le backend et le frontend dans deux terminaux séparés.

#### **1. Backend (Terminal 1)**

```bash
# Naviguez dans le dossier du backend
cd backend/

# Créez et activez un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt

# Lancez le serveur
python app.py
```

▶️ Le backend est maintenant accessible sur `http://localhost:5000`.

#### **2. Frontend (Terminal 2)**

```bash
# Naviguez dans le dossier du frontend
cd frontend/

# Installez les dépendances
npm install

# Lancez le serveur de développement
npm run dev
```

▶️ Le frontend est maintenant accessible sur `http://localhost:5173`.

### Déploiement sur un Serveur

Le déploiement se fait via Git et Docker.

1.  **Envoyez vos modifications sur Git** (depuis votre machine locale) :

    ```bash
    git add .
    git commit -m "Description des changements"
    git push
    ```

2.  **Connectez-vous à votre serveur en SSH** et mettez à jour le projet :

    ```bash
    # Se connecter au serveur
    ssh utilisateur@ip_du_serveur

    # Naviguer dans le dossier du projet
    cd chemin/vers/le/projet

    # Récupérer les dernières modifications
    git pull
    ```

3.  **Redéployez le conteneur Docker** :

    ```bash
    # Naviguer dans le dossier frontend
    cd frontend/

    # Reconstruire l'image avec les modifications
    docker build -t monoscript-frontend .

    # Arrêter et supprimer l'ancien conteneur
    docker stop monoscript-app && docker rm monoscript-app

    # Lancer le nouveau conteneur
    docker run -d -p 80:80 --restart always --name monoscript-app monoscript-frontend
    ```

▶️ L'application est maintenant à jour et accessible via l'adresse IP du serveur.

-----

````markdown
## 💻 Utilisation de l'IDE web

L'interface web propose :
- **Éditeur de code** : Zone de texte pour écrire vos programmes.
- **Bouton "Exécuter"** : Lance l'interprétation du code.
- **Zone de résultats** : Affiche la sortie et l'état des variables.
- **Exemples prédéfinis** : Boutons pour charger des exemples.

### Étapes d'utilisation
1. Écrivez votre programme dans l'éditeur.
2. Cliquez sur "Exécuter le Code".
3. Si votre programme contient des entrées utilisateur (`lire()` ou `input()`), une interface apparaîtra pour saisir les valeurs.
4. Consultez les résultats et l'état des variables.

---
## 📚 Référence du langage

### Variables et affectations

```monoscript
# Déclaration avec valeur initiale
variable nom = "Alice"
variable age = 25
variable actif = vrai

# Affectation à une variable existante
age = 26
nom = "Bob"
````

### Types de données

  - **Nombres** : `42`, `3.14`, `-10`
  - **Chaînes** : `"Bonjour"`, `"Hello World"`
  - **Booléens** : `vrai`, `faux`
  - **Tableaux** : `[1, 2, 3]`, `["a", "b", "c"]`
  - **Dictionnaires** : `{"nom": "Alice", "age": 25}`

### Opérateurs

#### Opérateurs arithmétiques

```monoscript
variable a = 10
variable b = 3
afficher a + b    # 13 (addition)
afficher a - b    # 7 (soustraction)
afficher a * b    # 30 (multiplication)
afficher a / b    # 3.333... (division)
```

#### Opérateurs unaires

```monoscript
variable x = 5
afficher -x      # -5 (négation)
afficher +x      # 5 (positif, pas de changement)
afficher -(-x)   # 5 (double négation)
```

#### Opérateurs de comparaison

```monoscript
variable a = 10
variable b = 5
afficher a > b    # vrai
afficher a < b    # faux
afficher a >= b   # vrai
afficher a <= b   # faux
afficher a == b   # faux
afficher a != b   # vrai
```

#### Opérateurs logiques

```monoscript
variable x = vrai
variable y = faux
afficher x et y   # faux
afficher x ou y   # vrai
afficher non x    # faux
```

### Structures de contrôle

#### Conditions

```monoscript
si age >= 18
    afficher "Majeur"
sinon
    afficher "Mineur"
fin_si

# Conditions imbriquées
si note >= 16
    afficher "Très bien"
sinon
    si note >= 14
        afficher "Bien"
    sinon
        afficher "Assez bien"
    fin_si
fin_si
```

#### Boucles

```monoscript
variable i = 0
tant_que i < 5
    afficher "Itération " + i
    i = i + 1
fin_tant_que
```

### Fonctions utilisateur

```monoscript
# Définition
fonction calculer_carre(nombre)
    retour nombre * nombre
fin_fonction

# Appel
variable resultat = calculer_carre(5)
afficher resultat  # 25
```

### Collections

#### Tableaux

```monoscript
variable nombres = [1, 2, 3, 4, 5]
afficher nombres[0]      # 1
nombres[2] = 99
afficher nombres         # [1, 2, 99, 4, 5]
```

#### Dictionnaires

```monoscript
variable personne = {"nom": "Alice", "age": 25}
afficher personne["nom"]   # Alice
personne["ville"] = "Paris"
afficher personne          # {"nom": "Alice", "age": 25, "ville": "Paris"}
```

### Entrées utilisateur

Le langage supporte deux fonctions pour saisir des données utilisateur : `lire(prompt)` et `input(prompt)`.

```monoscript
variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom + ", vous avez " + age + " ans"
```

**Fonctionnalités avancées :**

  - **Conversion automatique** : Les entrées numériques sont automatiquement converties en nombres.
  - **Interface interactive** : Dans l'IDE web, une interface apparaît automatiquement pour saisir les valeurs.
  - **Support des fonctions mathématiques** : Les entrées peuvent être utilisées directement avec `sqrt()`, `sin()`, `cos()`, etc.

#### Exemples avec conversion automatique

```monoscript
# L'utilisateur tape "3.14" → automatiquement converti en nombre
variable pi = input("Entrez π: ")
afficher "Racine de π: " + sqrt(pi)  # Fonctionne directement !

# L'utilisateur tape "25" → automatiquement converti en entier
variable age = lire("Votre âge: ")
si age >= 18
    afficher "Vous êtes majeur"
fin_si
```

#### Gestion des erreurs

```monoscript
variable nombre = input("Entrez un nombre: ")
# Si l'utilisateur tape "abc", une erreur sera levée pour les fonctions mathématiques
afficher "Valeur: " + nombre      # OK pour l'affichage
afficher "Racine: " + sqrt(nombre)  # Erreur si ce n'est pas un nombre
```

-----

## 🔧 Fonctions built-in

### Mathématiques

```monoscript
afficher sqrt(16)          # 4.0
afficher sin(0)            # 0.0
afficher cos(0)            # 1.0
afficher tan(0)            # 0.0
afficher abs(-5)           # 5
afficher round(3.7)        # 4
afficher round(3.14159, 2) # 3.14

# Avec des entrées utilisateur (conversion automatique)
variable nombre = input("Entrez un nombre: ")
afficher "Racine: " + sqrt(nombre)
afficher "Sinus: " + sin(nombre)
afficher "Cosinus: " + cos(nombre)
afficher "Absolu: " + abs(nombre)
afficher "Arrondi: " + round(nombre)
```

### Manipulation de chaînes

```monoscript
variable texte = "Bonjour le monde"
afficher maj(texte)        # BONJOUR LE MONDE
afficher min(texte)        # bonjour le monde
afficher len(texte)        # 16
```

### Utilitaires

```monoscript
variable liste = [1, 2, 3, 4, 5]
afficher len(liste)        # 5
afficher random()          # nombre aléatoire entre 0 et 1

# Saisie utilisateur (interactive en web)
variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom + ", vous avez " + age + " ans"
```

### Date et heure

```monoscript
afficher date()            # 2025-10-08
afficher heure()           # 15:18:58
afficher annee()           # 2025
afficher mois()            # 10
afficher jour()            # 8
```

-----

## 📖 Exemples pratiques

### Calculatrice simple

```monoscript
fonction addition(a, b)
    retour a + b
fin_fonction

fonction soustraction(a, b)
    retour a - b
fin_fonction

variable x = 10
variable y = 5
afficher "Addition: " + addition(x, y)
afficher "Soustraction: " + soustraction(x, y)
```

### Gestion d'une liste

```monoscript
variable notes = [15, 12, 18, 14, 16]
variable somme = 0
variable i = 0

tant_que i < len(notes)
    somme = somme + notes[i]
    i = i + 1
fin_tant_que

variable moyenne = somme / len(notes)
afficher "Moyenne: " + moyenne
```

### Jeu de devinette

```monoscript
variable nombre_secret = round(random() * 100)
variable tentative = 0
variable trouve = faux

tant_que non trouve
    variable proposition = lire("Devinez le nombre (0-100): ")
    tentative = tentative + 1
    
    si proposition == nombre_secret
        afficher "Bravo ! Trouvé en " + tentative + " tentatives"
        trouve = vrai
    sinon si proposition < nombre_secret
        afficher "Plus grand !"
    sinon
        afficher "Plus petit !"
    fin_si
fin_tant_que
```

### Programme interactif complet

```monoscript
# Programme de saisie et calcul
afficher "=== Programme de saisie ==="

variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
variable ville = lire("Votre ville: ")

afficher "Bonjour " + nom + " !"
afficher "Vous avez " + age + " ans"
afficher "Vous habitez à " + ville

# Calcul avec l'âge
variable age_prochain = age + 1
afficher "L'année prochaine, vous aurez " + age_prochain + " ans"

# Condition basée sur l'âge
si age >= 18
    afficher "Vous êtes majeur(e)"
sinon
    afficher "Vous êtes mineur(e)"
fin_si
```

### Calculatrice scientifique interactive

```monoscript
# Programme avec fonctions mathématiques et entrées utilisateur
afficher "=== Calculatrice Scientifique ==="

variable x = input("Entrez x: ")
variable y = input("Entrez y: ")

afficher "x + y = " + (x + y)
afficher "x * y = " + (x * y)
afficher "Racine de x = " + sqrt(x)
afficher "Racine de y = " + sqrt(y)
afficher "Sinus de x = " + sin(x)
afficher "Cosinus de y = " + cos(y)
afficher "Valeur absolue de (x-y) = " + abs(x - y)
```

### Programme de validation d'entrées

```monoscript
# Exemple de gestion d'erreurs avec les entrées
variable nombre = input("Entrez un nombre pour calculer sa racine: ")

# Le système convertit automatiquement en nombre si possible
afficher "Vous avez entré: " + nombre
afficher "Type détecté: " + type(nombre)

# Calculs mathématiques (fonctionnent si c'est un nombre)
afficher "Racine carrée: " + sqrt(nombre)
afficher "Carré: " + (nombre * nombre)
afficher "Arrondi: " + round(nombre)
```

```
```# Projet_MicroScript-
