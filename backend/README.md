# 🐍 Mon Langage de Programmation Français

Un langage de programmation simple en français avec interpréteur et IDE web intégré. Parfait pour apprendre les concepts de base de la programmation et comprendre comment fonctionnent les langages de programmation.

## 📋 Table des matières

- [🚀 Installation et lancement](#-installation-et-lancement)
- [💻 Utilisation de l'IDE web](#-utilisation-de-lide-web)
- [📚 Référence du langage](#-référence-du-langage)
- [🔧 Fonctions built-in](#-fonctions-built-in)
- [📖 Exemples pratiques](#-exemples-pratiques)
- [🐳 Déploiement avec Docker](#-déploiement-avec-docker)
- [🏗️ Architecture du projet](#️-architecture-du-projet)
- [❓ Dépannage](#-dépannage)

## 🚀 Installation et lancement

### Prérequis
- Python 3.11+ (ou Docker)
- Navigateur web moderne

### Lancement rapide

**Option 1 : Python local**
```bash
cd /Users/yanlangwana/Documents/ProjetIT
source venv/bin/activate
python app.py
```
→ Ouvrez http://localhost:5000

**Option 2 : Docker**
```bash
cd /Users/yanlangwana/Documents/ProjetIT
docker-compose up --build
```
→ Ouvrez http://localhost:3000

## 💻 Utilisation de l'IDE web

L'interface web propose :
- **Éditeur de code** : Zone de texte pour écrire vos programmes
- **Bouton "Exécuter"** : Lance l'interprétation du code
- **Zone de résultats** : Affiche la sortie et l'état des variables
- **Exemples prédéfinis** : Boutons pour charger des exemples

### Étapes d'utilisation
1. Écrivez votre programme dans l'éditeur
2. Cliquez sur "Exécuter le Code"
3. Si votre programme contient des entrées utilisateur (`lire()` ou `input()`), une interface apparaîtra pour saisir les valeurs
4. Consultez les résultats et l'état des variables

## 📚 Référence du langage

### Variables et affectations

```python
# Déclaration avec valeur initiale
variable nom = "Alice"
variable age = 25
variable actif = vrai

# Affectation à une variable existante
age = 26
nom = "Bob"
```

### Types de données

- **Nombres** : `42`, `3.14`, `-10`
- **Chaînes** : `"Bonjour"`, `"Hello World"`
- **Booléens** : `vrai`, `faux`
- **Tableaux** : `[1, 2, 3]`, `["a", "b", "c"]`
- **Dictionnaires** : `{"nom": "Alice", "age": 25}`

### Opérateurs

#### Opérateurs arithmétiques
```python
variable a = 10
variable b = 3
afficher a + b    # 13 (addition)
afficher a - b    # 7 (soustraction)
afficher a * b    # 30 (multiplication)
afficher a / b    # 3.333... (division)
```

#### Opérateurs unaires
```python
variable x = 5
afficher -x       # -5 (négation)
afficher +x       # 5 (positif, pas de changement)
afficher -(-x)    # 5 (double négation)
```

#### Opérateurs de comparaison
```python
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
```python
variable x = vrai
variable y = faux
afficher x et y   # faux
afficher x ou y   # vrai
afficher non x    # faux
```

### Structures de contrôle

#### Conditions
```python
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
```python
variable i = 0
tant_que i < 5
    afficher "Itération " + i
    i = i + 1
fin_tant_que
```

### Fonctions utilisateur

```python
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
```python
variable nombres = [1, 2, 3, 4, 5]
afficher nombres[0]        # 1
nombres[2] = 99
afficher nombres           # [1, 2, 99, 4, 5]
```

#### Dictionnaires
```python
variable personne = {"nom": "Alice", "age": 25}
afficher personne["nom"]   # Alice
personne["ville"] = "Paris"
afficher personne          # {"nom": "Alice", "age": 25, "ville": "Paris"}
```

### Entrées utilisateur

Le langage supporte deux fonctions pour saisir des données utilisateur :

#### `lire(prompt)` et `input(prompt)`
```python
variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom + ", vous avez " + age + " ans"
```

**Fonctionnalités avancées :**
- **Conversion automatique** : Les entrées numériques sont automatiquement converties en nombres
- **Interface interactive** : Dans l'IDE web, une interface apparaît automatiquement pour saisir les valeurs
- **Support des fonctions mathématiques** : Les entrées peuvent être utilisées directement avec `sqrt()`, `sin()`, `cos()`, etc.

#### Exemples avec conversion automatique
```python
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
```python
variable nombre = input("Entrez un nombre: ")
# Si l'utilisateur tape "abc", une erreur sera levée pour les fonctions mathématiques
afficher "Valeur: " + nombre  # OK pour l'affichage
afficher "Racine: " + sqrt(nombre)  # Erreur si ce n'est pas un nombre
```

## 🔧 Fonctions built-in

### Mathématiques
```python
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
```python
variable texte = "Bonjour le monde"
afficher maj(texte)        # BONJOUR LE MONDE
afficher min(texte)        # bonjour le monde
afficher len(texte)        # 16
```

### Utilitaires
```python
variable liste = [1, 2, 3, 4, 5]
afficher len(liste)        # 5
afficher random()          # nombre aléatoire entre 0 et 1

# Saisie utilisateur (interactive en web)
variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom + ", vous avez " + age + " ans"
```

### Date et heure
```python
afficher date()            # 2024-10-06
afficher heure()           # 14:30:25
afficher annee()           # 2024
afficher mois()            # 10
afficher jour()            # 6
```

## 📖 Exemples pratiques

### Calculatrice simple
```python
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
```python
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
```python
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
```python
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
```python
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
```python
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

## 🛠️ Développement

### Commandes utiles

**Lancement en mode développement**
```bash
# Lancer l'application avec rechargement automatique
python app.py

# Ou avec un port spécifique
python -c "import app; app.app.run(debug=True, host='0.0.0.0', port=5001)"
```

**Docker en mode développement**
```bash
# Lancer avec Docker Compose
docker-compose up --build

# En arrière-plan
docker-compose up -d --build
```

## 🐳 Déploiement avec Docker

### Déploiement local
```bash
# Construire et démarrer
docker-compose up --build

# En arrière-plan
docker-compose up -d --build

# Arrêter
docker-compose down
```

### Déploiement sur serveur
```bash
# 1. Copier les fichiers
scp -r . user@serveur:/path/to/project/

# 2. Sur le serveur
cd /path/to/project
docker-compose up -d --build
```

### Configuration pour un domaine
Modifiez `nginx.conf` :
```nginx
server_name votre-domaine.com;
```

### Commandes Docker utiles
```bash
# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart app

# Mettre à jour
docker-compose down && docker-compose up --build -d

# Nettoyer
docker system prune -a
```

## 🏗️ Architecture du projet

```
ProjetIT/
├── app.py              # Serveur Flask principal
├── lexer.py            # Analyseur lexical (tokens)
├── parser.py           # Analyseur syntaxique (AST)
├── interpreteur.py     # Interpréteur (exécution)
├── syntaxe.py          # Définition de la grammaire
├── templates/
│   └── index.html      # Interface web
├── Dockerfile          # Image Docker
├── docker-compose.yml  # Orchestration
├── nginx.conf          # Configuration Nginx
└── requirements.txt    # Dépendances Python
```

### Flux d'exécution
1. **Lexer** : Convertit le code source en tokens
2. **Parser** : Construit un AST (Arbre de Syntaxe Abstraite)
3. **Interpréteur** : Exécute l'AST et produit les résultats
4. **Web** : Affiche les résultats dans l'interface

### API Backend
- `GET /` : Page d'accueil de l'IDE
- `POST /executer` : Exécute le code et retourne les résultats

**Format de la requête POST /executer :**
```json
{
  "code": "variable nom = lire(\"Votre nom: \")\nafficher \"Bonjour \" + nom",
  "entrees": ["Alice"]
}
```

**Format de la réponse :**
```json
{
  "success": true,
  "resultat": ["[ENTRÉE REQUISE: Votre nom: ]", "Bonjour Alice"],
  "entrees_requises": ["Votre nom: "],
  "variables": {"nom": "Alice"},
  "tokens": [...]
}
```

## ❓ Dépannage

### Port déjà utilisé
```bash
# Erreur: Port 3000 is already in use
# Solution: Changer le port dans docker-compose.yml
ports:
  - "8080:80"  # Utiliser le port 8080
```

### Erreurs de syntaxe
- Vérifiez que vous n'utilisez pas "alors" dans `si` ou `tant_que`
- Entourez les chaînes avec des guillemets `"`
- Déclarez les variables avec `variable nom = valeur`
- Utilisez `lire()` ou `input()` pour les entrées utilisateur (pas `lire` sans parenthèses)

### Erreurs d'entrées utilisateur
```bash
# Erreur: "Impossible de convertir 'entrée_simulée' en nombre"
# Solution: Le système gère automatiquement cette conversion maintenant

# Erreur: "must be real number, not str"
# Solution: Les entrées numériques sont automatiquement converties
```

### Problèmes de conversion de types
- Les entrées utilisateur sont automatiquement converties en nombres si possible
- Pour les fonctions mathématiques, assurez-vous d'entrer des valeurs numériques
- Les chaînes non-numériques restent des chaînes pour l'affichage

### Problèmes Docker
```bash
# Reconstruire complètement
docker-compose down
docker system prune -f
docker-compose up --build
```

### Accès depuis l'extérieur
- Vérifiez que le port est ouvert sur le serveur
- Testez avec : `curl http://IP_DU_SERVEUR:PORT`

### Tests de l'API
```bash
# Test simple
curl -X POST http://localhost:5001/executer \
  -H "Content-Type: application/json" \
  -d '{"code": "afficher \"Hello World\""}'

# Test avec entrées utilisateur
curl -X POST http://localhost:5001/executer \
  -H "Content-Type: application/json" \
  -d '{"code": "variable nom = lire(\"Votre nom: \")\nafficher \"Bonjour \" + nom", "entrees": ["Alice"]}'

# Test avec fonctions mathématiques
curl -X POST http://localhost:5001/executer \
  -H "Content-Type: application/json" \
  -d '{"code": "variable x = input(\"Entrez x: \")\nafficher \"Racine: \" + sqrt(x)", "entrees": ["16"]}'
```

---

## 🎯 Objectifs pédagogiques

Ce projet permet d'apprendre :
- **Compilation** : Lexer, Parser, AST
- **Interprétation** : Exécution d'arbres syntaxiques
- **Développement web** : Flask, HTML, JavaScript
- **Déploiement** : Docker, Nginx
- **Architecture logicielle** : Séparation des responsabilités
- **Gestion d'entrées utilisateur** : Interface interactive, conversion de types
- **APIs REST** : Communication frontend/backend
- **Gestion d'erreurs** : Validation et conversion de données

## 🆕 Nouvelles fonctionnalités

### Système d'entrées interactives
- **Fonctions `lire()` et `input()`** : Saisie utilisateur avec prompts personnalisés
- **Interface web dynamique** : Champs de saisie automatiques dans l'IDE
- **Conversion automatique** : Les entrées numériques sont converties en nombres
- **Support complet** : Compatible avec toutes les fonctions mathématiques

### Améliorations techniques
- **Gestion robuste des types** : Conversion intelligente des données utilisateur
- **API étendue** : Support des entrées dans les requêtes POST
- **Interface utilisateur** : Expérience interactive fluide
- **Gestion d'erreurs** : Messages d'erreur clairs et informatifs

## 📝 Licence

Projet éducatif - Libre d'utilisation pour l'apprentissage.

---

*Développé avec ❤️ pour l'apprentissage de la programmation*