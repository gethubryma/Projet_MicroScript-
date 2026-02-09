# lexer.py  # Fichier du composant d'analyse lexicale
import re  # Module pour les expressions régulières
from syntaxe import SyntaxeFr  # Définition de la grammaire (mots-clés, opérateurs, séparateurs)

class Lexer:  # Convertit une chaîne de code source en une liste de tokens
    def __init__(self, code):  # Initialise l'état du lexer
        self.code = code  # Code source complet
        self.position = 0  # Index courant dans la chaîne
        self.tokens = []  # Liste des tokens collectés
        self.ligne = 1  # Numéro de ligne pour les messages d'erreur
        self.colonne = 1  # Numéro de colonne pour les messages d'erreur
        
    def tokenize(self):  # Point d'entrée : parcourt le code et produit les tokens
        while self.position < len(self.code):  # Tant qu'il reste des caractères
            self.ignorer_espaces()  # Sauter les espaces et gérer les retours à la ligne
            # Commentaires une ligne: commence par # ou // jusqu'à fin de ligne
            if self.position < len(self.code) and self.code[self.position] == '#':
                self._ignorer_commentaire_simple()
                continue
            if self.position+1 < len(self.code) and self.code[self.position:self.position+2] == '//':
                self._ignorer_commentaire_simple()
                continue
            if self.position >= len(self.code):  # Fin du code après espaces
                break  # Sortir de la boucle principale
            
            if self.analyser_nombre():  # Essayer de lire un nombre
                continue  # Reprendre au prochain caractère
            if self.analyser_chaine():  # Essayer de lire une chaîne "..."
                continue  # Continuer si réussi
            if self.analyser_identifiant():  # Essayer de lire un identifiant/mot-clé/opérateur logique
                continue  # Continuer si réussi
            if self.analyser_operateur():  # Essayer de lire un opérateur symbolique (+, -, ==, ...)
                continue  # Continuer si réussi
            if self.analyser_separateur():  # Essayer de lire un séparateur (, ), ;, ...
                continue  # Continuer si réussi
            
            raise Exception(f"Caractère inattendu à la ligne {self.ligne}: {self.code[self.position]}")  # Erreur si aucun cas ne correspond
            
        return self.tokens  # Retourner la liste de tokens construite
    
    def ignorer_espaces(self):  # Avance en ignorant les espaces et maj les coordonnées
        while self.position < len(self.code) and self.code[self.position].isspace():  # Tant qu'on est sur un espace
            if self.code[self.position] == '\n':  # Saut de ligne
                self.ligne += 1  # Incrémenter la ligne
                self.colonne = 1  # Réinitialiser la colonne
            else:  # Espace, tabulation, etc.
                self.colonne += 1  # Avancer la colonne
            self.position += 1  # Avancer d'un caractère
    
    def analyser_nombre(self):  # Tente d'extraire un nombre entier ou décimal
        match = re.match(r'\d+(\.\d*)?', self.code[self.position:])  # Regex pour 123 ou 123. ou 123.45
        if match:  # Si un nombre est trouvé au début
            valeur = match.group()  # Valeur textuelle trouvée
            self.ajouter_token('NOMBRE', float(valeur) if '.' in valeur else int(valeur))  # Convertir en int/float
            self.position += len(valeur)  # Avancer la position de la longueur lue
            self.colonne += len(valeur)  # Avancer la colonne d'autant
            return True  # Indiquer qu'on a consommé un token
        return False  # Aucun nombre ici
    
    def analyser_chaine(self):  # Tente d'extraire une chaîne délimitée par ""
        if self.code[self.position] == '"':  # Début de chaîne trouvé
            debut = self.position  # Mémoriser la position d'ouverture
            self.position += 1  # Sauter le guillemet ouvrant
            self.colonne += 1  # Avancer la colonne
            
            while self.position < len(self.code) and self.code[self.position] != '"':  # Avancer jusqu'au " fermant
                if self.code[self.position] == '\n':  # Gestion des retours à la ligne
                    self.ligne += 1  # Nouvelle ligne
                    self.colonne = 1  # Réinitialiser colonne
                else:
                    self.colonne += 1  # Avancer la colonne
                self.position += 1  # Avancer d'un caractère
                
            if self.position >= len(self.code):  # Fin du fichier sans fermeture
                raise Exception("Chaîne non terminée")  # Erreur de chaîne non close
                
            valeur = self.code[debut+1:self.position]  # Extraire le contenu sans guillemets
            self.ajouter_token('CHAINE', valeur)  # Ajouter le token chaîne
            self.position += 1  # Consommer le guillemet fermant
            self.colonne += 1  # Avancer la colonne
            return True  # Token consommé
        return False  # Pas une chaîne ici
    
    def analyser_identifiant(self):  # Tente d'extraire identifiant/mot-clé/opérateur logique
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.code[self.position:])  # Nom valide
        if match:  # Si un jeton textuel est trouvé
            identifiant = match.group()  # Texte de l'identifiant
            
            # Vérifier les booléens EN PREMIER (avant les mots-clés)
            if identifiant in ['vrai', 'faux']:  # Littéraux booléens
                self.ajouter_token('BOOLEEN', identifiant == 'vrai')  # True si 'vrai', sinon False
            elif identifiant in {'et', 'ou', 'non'}:  # Opérateurs logiques en toutes lettres
                self.ajouter_token('OPERATEUR', identifiant)  # Les classer comme opérateurs
            elif identifiant in SyntaxeFr.MOTS_CLES.values():  # Mots-clés du langage
                self.ajouter_token('MOT_CLE', identifiant)  # Ajouter un token mot-clé
            elif identifiant in SyntaxeFr.FONCTIONS_BUILTIN:  # Fonctions built-in
                self.ajouter_token('FONCTION_BUILTIN', identifiant)  # Ajouter un token fonction built-in
            else:  # Sinon, c'est un identifiant utilisateur
                self.ajouter_token('IDENTIFIANT', identifiant)  # Ajouter un token identifiant
                
            self.position += len(identifiant)  # Avancer la position d'autant de caractères lus
            self.colonne += len(identifiant)  # Avancer la colonne
            return True  # Token consommé
        return False  # Pas d'identifiant ici
    
    def analyser_operateur(self):  # Tente d'extraire un opérateur symbolique
        for op in sorted(SyntaxeFr.OPERATEURS, key=len, reverse=True):  # Plus longs d'abord (ex: '>=')
            if self.code[self.position:].startswith(op):  # Vérifier le préfixe courant
                self.ajouter_token('OPERATEUR', op)  # Ajouter le token opérateur
                self.position += len(op)  # Avancer la position
                self.colonne += len(op)  # Avancer la colonne
                return True  # Token consommé
        return False  # Pas d'opérateur ici
    
    def analyser_separateur(self):  # Tente d'extraire un séparateur ((),[] ,; ...)
        if self.code[self.position] in SyntaxeFr.SEPARATEURS:  # Caractère est un séparateur reconnu
            self.ajouter_token('SEPARATEUR', self.code[self.position])  # Ajouter le token séparateur
            self.position += 1  # Avancer d'un caractère
            self.colonne += 1  # Avancer la colonne
            return True  # Token consommé
        return False  # Pas de séparateur ici
    
    def ajouter_token(self, type_token, valeur):  # Ajoute un token avec ses métadonnées
        self.tokens.append({  # Empile un dictionnaire représentant le token
            'type': type_token,  # Type du token (NOMBRE, IDENTIFIANT, ...)
            'valeur': valeur,  # Valeur du token (ex: 42, "abc", '+')
            'ligne': self.ligne,  # Ligne où le token commence
            'colonne': self.colonne  # Colonne où le token commence
        })

    def _ignorer_commentaire_simple(self):  # Ignore tout jusqu'à la fin de ligne
        while self.position < len(self.code) and self.code[self.position] != '\n':
            self.position += 1
            self.colonne += 1