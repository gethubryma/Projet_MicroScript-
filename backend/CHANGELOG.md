# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [2.0.0] - 2024-10-07

### 🆕 Nouvelles fonctionnalités
- **Système d'entrées interactives** : Ajout des fonctions `lire()` et `input()` pour la saisie utilisateur
- **Interface web dynamique** : Champs de saisie automatiques dans l'IDE
- **Conversion automatique des types** : Les entrées numériques sont automatiquement converties en nombres
- **Support des opérateurs unaires** : Implémentation de `+` et `-` comme opérateurs unaires
- **API étendue** : Support des entrées utilisateur dans les requêtes POST

### 🔧 Améliorations
- **Gestion robuste des types** : Conversion intelligente des données utilisateur
- **Fonctions mathématiques** : Support complet avec les entrées utilisateur
- **Gestion d'erreurs** : Messages d'erreur plus clairs et informatifs
- **Documentation** : README complet avec exemples et guide d'utilisation

### 🐛 Corrections
- **Conversion de types** : Résolution du problème "must be real number, not str"
- **Valeurs simulées** : Gestion correcte des valeurs "entrée_simulée" dans les fonctions mathématiques
- **Parser** : Correction de la gestion des fonctions built-in dans les expressions
- **Syntaxe** : `lire` et `input` correctement classés comme fonctions built-in

### 🔄 Changements techniques
- **Parser** : Modification de `parser_appel` pour accepter les fonctions built-in
- **Interpréteur** : Ajout de la méthode `_convertir_en_nombre` pour la conversion de types
- **API Flask** : Extension de la route `/executer` pour accepter les entrées utilisateur
- **Frontend** : Interface JavaScript pour la gestion des entrées interactives

## [1.0.0] - 2024-10-06

### 🎉 Version initiale
- **Langage de programmation français** : Syntaxe complète en français
- **Interpréteur** : Exécution complète des programmes
- **IDE web** : Interface utilisateur avec éditeur de code
- **Fonctions built-in** : Support des fonctions mathématiques, chaînes, et utilitaires
- **Collections** : Support des tableaux et dictionnaires
- **Structures de contrôle** : Conditions et boucles
- **Fonctions utilisateur** : Définition et appel de fonctions
- **Déploiement Docker** : Configuration complète avec Nginx

### 🏗️ Architecture
- **Lexer** : Analyseur lexical pour la tokenisation
- **Parser** : Analyseur syntaxique pour la construction d'AST
- **Interpréteur** : Exécution des arbres de syntaxe abstraite
- **API REST** : Backend Flask avec endpoints pour l'exécution
- **Frontend** : Interface web responsive avec JavaScript

---

## 📋 Format des versions

Ce projet utilise [Semantic Versioning](https://semver.org/) :
- **MAJOR** : Changements incompatibles avec l'API
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs compatibles

## 🔮 Roadmap

### Version 2.1.0 (Prévue)
- [ ] Gestion des fichiers (lecture/écriture)
- [ ] Gestion d'exceptions (try/catch)
- [ ] Amélioration des performances
- [ ] Tests unitaires automatisés

### Version 2.2.0 (Prévue)
- [ ] Support des modules/imports
- [ ] Gestion des classes et objets
- [ ] Interface de débogage
- [ ] Thèmes personnalisables pour l'IDE

### Version 3.0.0 (Future)
- [ ] Compilateur vers bytecode
- [ ] Machine virtuelle optimisée
- [ ] Support multi-threading
- [ ] API de plugins

