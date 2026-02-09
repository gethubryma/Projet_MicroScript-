# 🤝 Guide de contribution

Merci de votre intérêt pour contribuer à ce projet ! Ce guide vous aidera à comprendre comment contribuer efficacement.

## 📋 Table des matières

- [🚀 Démarrage rapide](#-démarrage-rapide)
- [🏗️ Architecture du projet](#️-architecture-du-projet)
- [🔧 Développement](#-développement)
- [🧪 Tests](#-tests)
- [📝 Documentation](#-documentation)
- [🔄 Workflow de contribution](#-workflow-de-contribution)
- [📋 Standards de code](#-standards-de-code)

## 🚀 Démarrage rapide

### Prérequis
- Python 3.11+
- Git
- Navigateur web moderne
- Docker (optionnel, pour le déploiement)

### Installation
```bash
# Cloner le projet
git clone <url-du-repo>
cd ProjetIT

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
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
├── tests/              # Tests unitaires (à créer)
├── docs/               # Documentation technique (à créer)
└── requirements.txt    # Dépendances Python
```

### Flux d'exécution
1. **Lexer** : Convertit le code source en tokens
2. **Parser** : Construit un AST (Arbre de Syntaxe Abstraite)
3. **Interpréteur** : Exécute l'AST et produit les résultats
4. **Web** : Affiche les résultats dans l'interface

## 🔧 Développement

### Structure des modules

#### `lexer.py`
- **Responsabilité** : Tokenisation du code source
- **Classes principales** : `Lexer`
- **Méthodes importantes** : `tokeniser()`, `_analyser_token()`

#### `parser.py`
- **Responsabilité** : Construction de l'AST
- **Classes principales** : `Parser`
- **Méthodes importantes** : `parser_programme()`, `parser_instruction()`

#### `interpreteur.py`
- **Responsabilité** : Exécution de l'AST
- **Classes principales** : `Interpreteur`
- **Méthodes importantes** : `executer()`, `evaluer()`

#### `syntaxe.py`
- **Responsabilité** : Définition de la grammaire
- **Classes principales** : `SyntaxeFr`
- **Constantes importantes** : `MOTS_CLES`, `FONCTIONS_BUILTIN`

### Ajout de nouvelles fonctionnalités

#### 1. Nouvelle fonction built-in
```python
# Dans syntaxe.py
FONCTIONS_BUILTIN = {
    # ... fonctions existantes ...
    'nouvelle_fonction': 'nouvelle_fonction'
}

# Dans interpreteur.py
def _executer_fonction_builtin(self, nom, args):
    # ... code existant ...
    elif nom == 'nouvelle_fonction':
        # Implémentation de la fonction
        return resultat
```

#### 2. Nouveau mot-clé
```python
# Dans syntaxe.py
MOTS_CLES = {
    # ... mots-clés existants ...
    'nouveau_mot_cle': 'nouveau_mot_cle'
}

# Dans parser.py
def parser_instruction(self):
    # ... code existant ...
    elif token['valeur'] == 'nouveau_mot_cle':
        return self.parser_nouveau_mot_cle()
```

#### 3. Nouvelle structure de contrôle
```python
# Dans parser.py
def parser_nouvelle_structure(self):
    # Analyser la condition
    condition = self.parser_expression()
    
    # Analyser le corps
    self._consommer('alors')
    corps = self.parser_bloc()
    
    return NoeudNouvelleStructure(condition, corps)
```

## 🧪 Tests

### Structure des tests (à implémenter)
```
tests/
├── test_lexer.py
├── test_parser.py
├── test_interpreteur.py
├── test_api.py
└── fixtures/
    ├── programmes_simples.py
    └── programmes_complexes.py
```

### Exemple de test
```python
import unittest
from lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_tokenisation_simple(self):
        lexer = Lexer('afficher "Hello"')
        tokens = lexer.tokeniser()
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0]['type'], 'MOT_CLE')
        self.assertEqual(tokens[0]['valeur'], 'afficher')
```

### Lancer les tests
```bash
# Tests unitaires
python -m unittest discover tests/

# Tests avec couverture
pip install coverage
coverage run -m unittest discover tests/
coverage report
coverage html  # Génère un rapport HTML
```

## 📝 Documentation

### Standards de documentation
- **Docstrings** : Utiliser le format Google pour toutes les fonctions publiques
- **Commentaires** : Expliquer la logique complexe
- **README** : Maintenir à jour avec les nouvelles fonctionnalités
- **Changelog** : Documenter toutes les modifications

### Exemple de docstring
```python
def executer_programme(self, code_source):
    """Exécute un programme complet.
    
    Args:
        code_source (str): Le code source à exécuter
        
    Returns:
        dict: Résultat de l'exécution avec sortie et variables
        
    Raises:
        Exception: En cas d'erreur de syntaxe ou d'exécution
    """
```

## 🔄 Workflow de contribution

### 1. Fork et clone
```bash
# Fork le projet sur GitHub
# Puis cloner votre fork
git clone https://github.com/votre-username/ProjetIT.git
cd ProjetIT
```

### 2. Créer une branche
```bash
git checkout -b feature/nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

### 3. Développer
- Écrire le code
- Ajouter des tests
- Mettre à jour la documentation
- Vérifier que tout fonctionne

### 4. Tester
```bash
# Tests unitaires
python -m unittest discover tests/

# Test manuel de l'interface
python app.py
# Ouvrir http://localhost:5000 et tester
```

### 5. Commit et push
```bash
git add .
git commit -m "feat: ajouter nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

### 6. Pull Request
- Créer une PR sur GitHub
- Décrire les changements
- Attendre la review

## 📋 Standards de code

### Python
- **PEP 8** : Respecter les conventions de style Python
- **Type hints** : Utiliser les annotations de type
- **Noms** : Variables et fonctions en snake_case, classes en PascalCase

### JavaScript
- **ES6+** : Utiliser les fonctionnalités modernes
- **Noms** : Variables et fonctions en camelCase
- **Commentaires** : JSDoc pour les fonctions

### HTML/CSS
- **Sémantique** : Utiliser les balises appropriées
- **Accessibilité** : Respecter les standards WCAG
- **Responsive** : Design adaptatif

### Messages de commit
Utiliser le format [Conventional Commits](https://www.conventionalcommits.org/) :
```
feat: ajouter nouvelle fonctionnalité
fix: corriger bug dans le parser
docs: mettre à jour la documentation
test: ajouter tests pour les fonctions mathématiques
refactor: simplifier la logique du lexer
```

## 🐛 Signaler un bug

### Template de bug report
```markdown
**Description du bug**
Description claire et concise du problème.

**Étapes pour reproduire**
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

**Comportement attendu**
Description de ce qui devrait se passer.

**Comportement actuel**
Description de ce qui se passe réellement.

**Environnement**
- OS: [ex: Windows 10, macOS 12, Ubuntu 20.04]
- Python: [ex: 3.11.0]
- Navigateur: [ex: Chrome 95, Firefox 94]

**Code de reproduction**
```python
# Code qui reproduit le bug
```

**Logs d'erreur**
```
Traceback (most recent call last):
  ...
```

## 💡 Proposer une fonctionnalité

### Template de feature request
```markdown
**Description de la fonctionnalité**
Description claire de la fonctionnalité souhaitée.

**Problème résolu**
Explication du problème que cette fonctionnalité résoudrait.

**Solution proposée**
Description détaillée de la solution.

**Alternatives considérées**
Autres solutions envisagées.

**Contexte supplémentaire**
Toute information utile (captures d'écran, exemples, etc.).
```

## 📞 Support

- **Issues GitHub** : Pour les bugs et demandes de fonctionnalités
- **Discussions** : Pour les questions générales
- **Email** : [votre-email@example.com] pour les questions privées

## 📄 Licence

En contribuant à ce projet, vous acceptez que vos contributions soient sous la même licence que le projet.

---

Merci de contribuer à ce projet éducatif ! 🎉

