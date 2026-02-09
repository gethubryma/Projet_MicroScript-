# interpreteur.py
import math
import random
import datetime
from parser import (
    NoeudProgramme,
    NoeudDeclarationVariable,
    NoeudAffectation,
    NoeudSi,
    NoeudTantQue,
    NoeudAfficher,
    NoeudLire,
    NoeudNombre,
    NoeudChaine,
    NoeudBooleen,
    NoeudVariable,
    NoeudExpressionBinaire,
    NoeudFonction,
    NoeudAppel,
    NoeudRetour,
    NoeudIndex,
)
from syntaxe import SyntaxeFr


class Interpreteur:
    def __init__(self):
        self.variables = {}
        self.sortie = []
        self.fonctions = {}
        self.entrees_en_attente = []
        self.entrees_fournies = []
    
    def executer(self, arbre):
        if isinstance(arbre, NoeudProgramme):
            for instruction in arbre.instructions:
                self.executer_instruction(instruction)
        return self.sortie
    
    def fournir_entrees(self, entrees):
        """Fournit des entrées utilisateur à l'interpréteur"""
        self.entrees_fournies = entrees
    
    def _convertir_en_nombre(self, valeur):
        """Convertit une valeur en nombre si possible"""
        if isinstance(valeur, (int, float)):
            return valeur
        
        if isinstance(valeur, str):
            try:
                # Nettoyer la valeur (enlever les espaces)
                valeur_clean = valeur.strip()
                
                # Si c'est un nombre entier
                if '.' not in valeur_clean and valeur_clean.lstrip('-').isdigit():
                    return int(valeur_clean)
                # Si c'est un nombre décimal
                elif valeur_clean.replace('.', '').replace('-', '').isdigit() and valeur_clean.count('.') <= 1:
                    return float(valeur_clean)
            except:
                pass
        
        # Si la conversion échoue, lever une exception
        raise Exception(f"Impossible de convertir '{valeur}' en nombre")
    
    def executer_instruction(self, instruction):
        if isinstance(instruction, NoeudDeclarationVariable):
            if instruction.nom in self.variables:
                raise Exception(f"Variable déjà déclarée: {instruction.nom}")
            if instruction.valeur:
                self.variables[instruction.nom] = self.evaluer(instruction.valeur)
            else:
                self.variables[instruction.nom] = None
                
        elif isinstance(instruction, NoeudAffectation):
            if instruction.nom not in self.variables:
                raise Exception(f"Variable non déclarée: {instruction.nom}")
            self.variables[instruction.nom] = self.evaluer(instruction.valeur)
            
        elif isinstance(instruction, NoeudSi):
            condition = self.evaluer(instruction.condition)
            if condition:
                for instr in instruction.bloc_si:
                    self.executer_instruction(instr)
            elif instruction.bloc_sinon:
                for instr in instruction.bloc_sinon:
                    self.executer_instruction(instr)
                    
        elif isinstance(instruction, NoeudTantQue):
            while self.evaluer(instruction.condition):
                for instr in instruction.bloc:
                    self.executer_instruction(instr)
                    
        elif isinstance(instruction, NoeudAfficher):
            valeur = self.evaluer(instruction.expression)
            self.sortie.append(str(valeur))
            
        elif isinstance(instruction, NoeudLire):
            prompt = self.evaluer(instruction.prompt) if instruction.prompt else ""
            # Enregistrer l'entrée en attente
            self.entrees_en_attente.append(prompt)
            self.sortie.append(f"[ENTRÉE REQUISE: {prompt}]")
            # Utiliser les entrées fournies si disponibles
            if len(self.entrees_fournies) > len(self.entrees_en_attente) - 1:
                return self.entrees_fournies[len(self.entrees_en_attente) - 1]
            return "entrée_simulée"
        elif isinstance(instruction, NoeudFonction):
            # Enregistrer la définition de fonction
            self.fonctions[instruction.nom] = instruction
        elif isinstance(instruction, NoeudRetour):
            # Spécial: remonter la valeur via une exception contrôlée
            valeur = self.evaluer(instruction.expression) if instruction.expression is not None else None
            raise _RetourFonction(valeur)
    
    def evaluer(self, noeud):
        if isinstance(noeud, NoeudNombre):
            return noeud.valeur
        elif isinstance(noeud, NoeudChaine):
            return noeud.valeur
        elif isinstance(noeud, NoeudBooleen):
            return noeud.valeur
        elif isinstance(noeud, NoeudVariable):
            if noeud.nom not in self.variables:
                raise Exception(f"Variable non définie: {noeud.nom}")
            return self.variables[noeud.nom]
        elif isinstance(noeud, NoeudExpressionBinaire):
            # Traiter d'abord les opérateurs spéciaux construits par le parser
            if noeud.operateur == 'array':
                return [self.evaluer(elem) for elem in noeud.droite]
            if noeud.operateur == 'dict':
                res = {}
                for k_node, v_node in noeud.droite:
                    res[self.evaluer(k_node)] = self.evaluer(v_node)
                return res
            if noeud.operateur == 'set_index':
                valeur = self.evaluer(noeud.droite)
                self._set_index(noeud.gauche, valeur)
                return valeur

            gauche = self.evaluer(noeud.gauche)
            droite = self.evaluer(noeud.droite) if noeud.droite else None

            if noeud.operateur == '+':
                # Autoriser la concaténation de chaînes et la somme numérique
                if isinstance(gauche, str) or isinstance(droite, str):
                    return str(gauche) + str(droite)
                # Conversion automatique pour les opérations numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num + droite_num
                except ValueError:
                    return gauche + droite
            elif noeud.operateur == '-':
                # Conversion automatique pour les opérations numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num - droite_num
                except ValueError:
                    return gauche - droite
            elif noeud.operateur == '*':
                # Conversion automatique pour les opérations numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num * droite_num
                except ValueError:
                    return gauche * droite
            elif noeud.operateur == '/':
                # Conversion automatique pour les opérations numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    if droite_num == 0:
                        raise Exception("Division par zéro")
                    return gauche_num / droite_num
                except ValueError:
                    if droite == 0:
                        raise Exception("Division par zéro")
                    return gauche / droite
            elif noeud.operateur == '%':
                # Conversion automatique pour les opérations numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num % droite_num
                except ValueError:
                    return gauche % droite
            elif noeud.operateur == '==':
                return gauche == droite
            elif noeud.operateur == '!=':
                return gauche != droite
            elif noeud.operateur == '<':
                # Conversion automatique pour les comparaisons numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num < droite_num
                except ValueError:
                    return gauche < droite
            elif noeud.operateur == '>':
                # Conversion automatique pour les comparaisons numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num > droite_num
                except ValueError:
                    return gauche > droite
            elif noeud.operateur == '<=':
                # Conversion automatique pour les comparaisons numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num <= droite_num
                except ValueError:
                    return gauche <= droite
            elif noeud.operateur == '>=':
                # Conversion automatique pour les comparaisons numériques
                try:
                    gauche_num = self._convertir_en_nombre(gauche)
                    droite_num = self._convertir_en_nombre(droite)
                    return gauche_num >= droite_num
                except ValueError:
                    return gauche >= droite
            elif noeud.operateur == 'et':
                return gauche and droite
            elif noeud.operateur == 'ou':
                return gauche or droite
            elif noeud.operateur == 'non':
                return not gauche
        elif isinstance(noeud, NoeudIndex):
            cible = self.evaluer(noeud.cible)
            idx = self.evaluer(noeud.index)
            return cible[idx]
        elif isinstance(noeud, NoeudAppel):
            # Vérifier d'abord les fonctions built-in
            if noeud.nom in SyntaxeFr.FONCTIONS_BUILTIN:
                return self._executer_fonction_builtin(noeud.nom, noeud.args)
            
            # Sinon, fonction utilisateur
            if noeud.nom not in self.fonctions:
                raise Exception(f"Fonction non définie: {noeud.nom}")
            definition = self.fonctions[noeud.nom]
            if len(definition.params) != len(noeud.args):
                raise Exception(f"Nombre d'arguments invalide pour {noeud.nom}")
            # Créer un nouvel environnement local chaîné
            ancien_env = self.variables
            local_env = dict(ancien_env)  # capture par valeur simple
            # Lier paramètres
            for nom_param, arg_expr in zip(definition.params, noeud.args):
                local_env[nom_param] = self.evaluer(arg_expr)
            # Exécuter le corps avec environnement local
            self.variables = local_env
            try:
                for instr in definition.corps:
                    self.executer_instruction(instr)
            except _RetourFonction as r:
                resultat = r.valeur
            else:
                resultat = None
            finally:
                self.variables = ancien_env
            return resultat
                
        raise Exception(f"Type de nœud non supporté: {type(noeud)}")

    def _set_index(self, noeud_index, valeur):
        if isinstance(noeud_index.cible, NoeudIndex):
            parent = self.evaluer(noeud_index.cible.cible)
            cle_parent = self.evaluer(noeud_index.cible.index)
            cible = parent[cle_parent]
            cle_finale = self.evaluer(noeud_index.index)
            cible[cle_finale] = valeur
        elif isinstance(noeud_index.cible, NoeudVariable):
            nom = noeud_index.cible.nom
            if nom not in self.variables:
                raise Exception(f"Variable non définie: {nom}")
            cible = self.variables[nom]
            cle = self.evaluer(noeud_index.index)
            cible[cle] = valeur
        else:
            raise Exception("Affectation indexée invalide")

    def _convertir_en_nombre(self, valeur):
        """Convertit une valeur en nombre si possible"""
        if isinstance(valeur, (int, float)):
            return valeur
        if isinstance(valeur, str):
            # Si c'est une valeur simulée, retourner 0
            if valeur == "entrée_simulée":
                return 0
            # Essayer de convertir en int d'abord
            try:
                return int(valeur)
            except ValueError:
                pass
            # Essayer de convertir en float
            try:
                return float(valeur)
            except ValueError:
                pass
        # Si on ne peut pas convertir, lever une exception
        raise ValueError(f"Impossible de convertir '{valeur}' en nombre")

    def _executer_fonction_builtin(self, nom, args):
        """Exécute les fonctions built-in du langage"""
        args_evalues = [self.evaluer(arg) for arg in args]
        
        # Conversion automatique des types pour les fonctions mathématiques
        if nom in ['sqrt', 'sin', 'cos', 'tan', 'abs', 'round']:
            args_evalues = [self._convertir_en_nombre(arg) for arg in args_evalues]
        
        if nom == 'lire' or nom == 'input':
            if len(args_evalues) > 0:
                prompt = str(args_evalues[0])
            else:
                prompt = ""
            # Enregistrer l'entrée en attente
            self.entrees_en_attente.append(prompt)
            self.sortie.append(f"[ENTRÉE REQUISE: {prompt}]")
            # Utiliser les entrées fournies si disponibles
            if len(self.entrees_fournies) > len(self.entrees_en_attente) - 1:
                valeur = self.entrees_fournies[len(self.entrees_en_attente) - 1]
                # Essayer de convertir en nombre si possible
                try:
                    # Nettoyer la valeur (enlever les espaces)
                    valeur_clean = valeur.strip()
                    
                    # Si c'est un nombre entier
                    if '.' not in valeur_clean and valeur_clean.lstrip('-').isdigit():
                        return int(valeur_clean)
                    # Si c'est un nombre décimal
                    elif valeur_clean.replace('.', '').replace('-', '').isdigit() and valeur_clean.count('.') <= 1:
                        return float(valeur_clean)
                    # Sinon, garder comme chaîne
                    else:
                        return valeur_clean
                except:
                    return valeur
            return "entrée_simulée"
        
        elif nom == 'len':
            if len(args_evalues) != 1:
                raise Exception("len() attend exactement 1 argument")
            return len(args_evalues[0])
        
        elif nom == 'sqrt':
            if len(args_evalues) != 1:
                raise Exception("sqrt() attend exactement 1 argument")
            return math.sqrt(args_evalues[0])
        
        elif nom == 'sin':
            if len(args_evalues) != 1:
                raise Exception("sin() attend exactement 1 argument")
            return math.sin(args_evalues[0])
        
        elif nom == 'cos':
            if len(args_evalues) != 1:
                raise Exception("cos() attend exactement 1 argument")
            return math.cos(args_evalues[0])
        
        elif nom == 'tan':
            if len(args_evalues) != 1:
                raise Exception("tan() attend exactement 1 argument")
            return math.tan(args_evalues[0])
        
        elif nom == 'abs':
            if len(args_evalues) != 1:
                raise Exception("abs() attend exactement 1 argument")
            return abs(args_evalues[0])
        
        elif nom == 'round':
            if len(args_evalues) == 1:
                return round(args_evalues[0])
            elif len(args_evalues) == 2:
                return round(args_evalues[0], args_evalues[1])
            else:
                raise Exception("round() attend 1 ou 2 arguments")
        
        elif nom == 'maj':
            if len(args_evalues) != 1:
                raise Exception("maj() attend exactement 1 argument")
            return str(args_evalues[0]).upper()
        
        elif nom == 'min':
            if len(args_evalues) != 1:
                raise Exception("min() attend exactement 1 argument")
            return str(args_evalues[0]).lower()
        
        elif nom == 'random':
            return random.random()
        
        elif nom == 'date':
            return datetime.datetime.now().strftime("%Y-%m-%d")
        
        elif nom == 'heure':
            return datetime.datetime.now().strftime("%H:%M:%S")
        
        elif nom == 'annee':
            return datetime.datetime.now().year
        
        elif nom == 'mois':
            return datetime.datetime.now().month
        
        elif nom == 'jour':
            return datetime.datetime.now().day
        
        else:
            raise Exception(f"Fonction built-in non implémentée: {nom}")


class _RetourFonction(Exception):
    def __init__(self, valeur):
        super().__init__('retour')
        self.valeur = valeur