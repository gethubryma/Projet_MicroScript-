# parser.py
from syntaxe import SyntaxeFr

class NoeudAST:
    pass

class NoeudProgramme(NoeudAST):
    def __init__(self, instructions):
        self.instructions = instructions

class NoeudDeclarationVariable(NoeudAST):
    def __init__(self, nom, valeur=None):
        self.nom = nom
        self.valeur = valeur

class NoeudAffectation(NoeudAST):
    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

class NoeudExpressionBinaire(NoeudAST):
    def __init__(self, gauche, operateur, droite):
        self.gauche = gauche
        self.operateur = operateur
        self.droite = droite

class NoeudNombre(NoeudAST):
    def __init__(self, valeur):
        self.valeur = valeur

class NoeudChaine(NoeudAST):
    def __init__(self, valeur):
        self.valeur = valeur

class NoeudBooleen(NoeudAST):
    def __init__(self, valeur):
        self.valeur = valeur

class NoeudVariable(NoeudAST):
    def __init__(self, nom):
        self.nom = nom

class NoeudIndex(NoeudAST):
    def __init__(self, cible, index):
        self.cible = cible
        self.index = index

class NoeudSi(NoeudAST):
    def __init__(self, condition, bloc_si, bloc_sinon=None):
        self.condition = condition
        self.bloc_si = bloc_si
        self.bloc_sinon = bloc_sinon

class NoeudTantQue(NoeudAST):
    def __init__(self, condition, bloc):
        self.condition = condition
        self.bloc = bloc

class NoeudAfficher(NoeudAST):
    def __init__(self, expression):
        self.expression = expression

class NoeudLire(NoeudAST):
    def __init__(self, prompt):
        self.prompt = prompt

class NoeudFonction(NoeudAST):
    def __init__(self, nom, params, corps):
        self.nom = nom
        self.params = params
        self.corps = corps

class NoeudAppel(NoeudAST):
    def __init__(self, nom, args):
        self.nom = nom
        self.args = args

class NoeudRetour(NoeudAST):
    def __init__(self, expression=None):
        self.expression = expression

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def parser(self):
        instructions = []
        while self.position < len(self.tokens):
            instructions.append(self.parser_instruction())
        return NoeudProgramme(instructions)
    
    def parser_instruction(self):
        token = self.regarder_actuel()
        
        if token['type'] == 'MOT_CLE':
            if token['valeur'] == 'variable':
                return self.parser_declaration_variable()
            elif token['valeur'] == 'si':
                return self.parser_si()
            elif token['valeur'] == 'tant_que':
                return self.parser_tant_que()
            elif token['valeur'] == 'afficher':
                return self.parser_afficher()
            elif token['valeur'] == 'fonction':
                return self.parser_fonction()
            elif token['valeur'] == 'retour':
                return self.parser_retour()
        
        # Affectation de variable
        if token['type'] == 'IDENTIFIANT':
            # Affectation ou appel de fonction
            if (self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1]['type'] == 'SEPARATEUR'
                and self.tokens[self.position + 1]['valeur'] == '('):
                return self.parser_appel()
            return self.parser_affectation()
        
        # Expression commençant par une fonction built-in
        if token['type'] == 'FONCTION_BUILTIN':
            return self.parser_expression()
            
        raise Exception(f"Instruction inattendue: {token}")
    
    def parser_declaration_variable(self):
        self.consumer('MOT_CLE', 'variable')
        nom = self.consumer('IDENTIFIANT')['valeur']
        
        if self.regarder_actuel()['valeur'] == '=':
            self.consumer('OPERATEUR', '=')
            valeur = self.parser_expression()
            return NoeudDeclarationVariable(nom, valeur)
        else:
            return NoeudDeclarationVariable(nom)
    
    def parser_affectation(self):
        # support a[i] = x et obj["k"] = x en plus de nom = x
        cible = self.parser_lvalue()
        self.consumer('OPERATEUR', '=')
        valeur = self.parser_expression()
        if isinstance(cible, NoeudVariable):
            return NoeudAffectation(cible.nom, valeur)
        else:
            # Utiliser un opérateur spécial via NoeudExpressionBinaire pour signaler une affectation indexée
            return NoeudExpressionBinaire(cible, 'set_index', valeur)

    def parser_lvalue(self):
        # Parse un identifiant puis zéro ou plusieurs [expr]
        if self.regarder_actuel()['type'] != 'IDENTIFIANT':
            raise Exception("Lvalue attendue")
        noeud = NoeudVariable(self.consumer('IDENTIFIANT')['valeur'])
        while self.position < len(self.tokens) and self.regarder_actuel()['valeur'] == '[':
            self.consumer('SEPARATEUR', '[')
            idx = self.parser_expression()
            self.consumer('SEPARATEUR', ']')
            noeud = NoeudIndex(noeud, idx)
        return noeud
    
    def parser_si(self):
        self.consumer('MOT_CLE', 'si')
        condition = self.parser_expression()
        
        bloc_si = []
        while (self.position < len(self.tokens) and 
               not (self.regarder_actuel()['type'] == 'MOT_CLE' and 
                    self.regarder_actuel()['valeur'] in ['sinon', 'fin_si'])):
            bloc_si.append(self.parser_instruction())
        
        bloc_sinon = None
        if (self.position < len(self.tokens) and 
            self.regarder_actuel()['valeur'] == 'sinon'):
            self.consumer('MOT_CLE', 'sinon')
            bloc_sinon = []
            while (self.position < len(self.tokens) and 
                   self.regarder_actuel()['valeur'] != 'fin_si'):
                bloc_sinon.append(self.parser_instruction())
        
        self.consumer('MOT_CLE', 'fin_si')
        return NoeudSi(condition, bloc_si, bloc_sinon)
    
    def parser_tant_que(self):
        self.consumer('MOT_CLE', 'tant_que')
        condition = self.parser_expression()
        
        bloc = []
        while (self.position < len(self.tokens) and 
               self.regarder_actuel()['valeur'] != 'fin_tant_que'):
            bloc.append(self.parser_instruction())
        
        self.consumer('MOT_CLE', 'fin_tant_que')
        return NoeudTantQue(condition, bloc)
    
    def parser_afficher(self):
        self.consumer('MOT_CLE', 'afficher')
        expression = self.parser_expression()
        return NoeudAfficher(expression)
    

    def parser_fonction(self):
        self.consumer('MOT_CLE', 'fonction')
        nom = self.consumer('IDENTIFIANT')['valeur']
        self.consumer('SEPARATEUR', '(')
        params = []
        if self.regarder_actuel()['valeur'] != ')':
            params.append(self.consumer('IDENTIFIANT')['valeur'])
            while self.regarder_actuel()['valeur'] == ',':
                self.consumer('SEPARATEUR', ',')
                params.append(self.consumer('IDENTIFIANT')['valeur'])
        self.consumer('SEPARATEUR', ')')
        corps = []
        while not (self.regarder_actuel()['type'] == 'MOT_CLE' and self.regarder_actuel()['valeur'] == 'fin_fonction'):
            corps.append(self.parser_instruction())
        self.consumer('MOT_CLE', 'fin_fonction')
        return NoeudFonction(nom, params, corps)

    def parser_appel(self):
        token = self.regarder_actuel()
        if token['type'] == 'IDENTIFIANT':
            nom = self.consumer('IDENTIFIANT')['valeur']
        elif token['type'] == 'FONCTION_BUILTIN':
            nom = self.consumer('FONCTION_BUILTIN')['valeur']
        else:
            raise Exception(f"Attendu IDENTIFIANT ou FONCTION_BUILTIN, obtenu {token}")
        
        self.consumer('SEPARATEUR', '(')
        args = []
        if self.regarder_actuel()['valeur'] != ')':
            args.append(self.parser_expression())
            while self.regarder_actuel()['valeur'] == ',':
                self.consumer('SEPARATEUR', ',')
                args.append(self.parser_expression())
        self.consumer('SEPARATEUR', ')')
        return NoeudAppel(nom, args)

    def parser_retour(self):
        self.consumer('MOT_CLE', 'retour')
        if self.position < len(self.tokens) and self.regarder_actuel()['type'] not in ('MOT_CLE',):
            expr = self.parser_expression()
        else:
            expr = None
        return NoeudRetour(expr)
    
    def parser_expression(self):
        return self.parser_expression_logique()
    
    def parser_expression_logique(self):
        gauche = self.parser_expression_comparaison()
        
        while (self.position < len(self.tokens) and 
               self.regarder_actuel()['type'] == 'OPERATEUR' and 
               self.regarder_actuel()['valeur'] in ['et', 'ou']):
            operateur = self.consumer('OPERATEUR')['valeur']
            droite = self.parser_expression_comparaison()
            gauche = NoeudExpressionBinaire(gauche, operateur, droite)
        
        return gauche
    
    def parser_expression_comparaison(self):
        gauche = self.parser_expression_arithmetique()
        
        while (self.position < len(self.tokens) and 
               self.regarder_actuel()['type'] == 'OPERATEUR' and 
               self.regarder_actuel()['valeur'] in ['==', '!=', '<', '>', '<=', '>=']):
            operateur = self.consumer('OPERATEUR')['valeur']
            droite = self.parser_expression_arithmetique()
            gauche = NoeudExpressionBinaire(gauche, operateur, droite)
        
        return gauche
    
    def parser_expression_arithmetique(self):
        gauche = self.parser_terme()
        
        while (self.position < len(self.tokens) and 
               self.regarder_actuel()['type'] == 'OPERATEUR' and 
               self.regarder_actuel()['valeur'] in ['+', '-']):
            operateur = self.consumer('OPERATEUR')['valeur']
            droite = self.parser_terme()
            gauche = NoeudExpressionBinaire(gauche, operateur, droite)
        
        return gauche
    
    def parser_terme(self):
        gauche = self.parser_facteur()
        
        while (self.position < len(self.tokens) and 
               self.regarder_actuel()['type'] == 'OPERATEUR' and 
               self.regarder_actuel()['valeur'] in ['*', '/', '%']):
            operateur = self.consumer('OPERATEUR')['valeur']
            droite = self.parser_facteur()
            gauche = NoeudExpressionBinaire(gauche, operateur, droite)
        
        return gauche
    
    def parser_facteur(self):
        token = self.regarder_actuel()
        
        if token['type'] == 'NOMBRE':
            self.position += 1
            return NoeudNombre(token['valeur'])
        elif token['type'] == 'CHAINE':
            self.position += 1
            return NoeudChaine(token['valeur'])
        elif token['type'] == 'BOOLEEN':
            self.position += 1
            return NoeudBooleen(token['valeur'])
        elif token['type'] == 'IDENTIFIANT':
            # variable, appel de fonction, ou indexation
            if (self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1]['type'] == 'SEPARATEUR'
                and self.tokens[self.position + 1]['valeur'] == '('):
                return self.parser_appel()
            # variable ou chaines d'index
            noeud = NoeudVariable(token['valeur'])
            self.position += 1
            while self.position < len(self.tokens) and self.regarder_actuel()['valeur'] == '[':
                self.consumer('SEPARATEUR', '[')
                idx = self.parser_expression()
                self.consumer('SEPARATEUR', ']')
                noeud = NoeudIndex(noeud, idx)
            return noeud
        elif token['type'] == 'FONCTION_BUILTIN':
            # Fonction built-in
            if (self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1]['type'] == 'SEPARATEUR'
                and self.tokens[self.position + 1]['valeur'] == '('):
                return self.parser_appel()
            else:
                # Fonction built-in sans parenthèses (comme 'random')
                self.position += 1
                return NoeudAppel(token['valeur'], [])
        elif token['valeur'] == '(':
            self.consumer('SEPARATEUR', '(')
            expression = self.parser_expression()
            self.consumer('SEPARATEUR', ')')
            return expression
        elif token['valeur'] == '[':
            return self.parser_tableau()
        elif token['valeur'] == '{':
            return self.parser_dictionnaire()
        elif token['valeur'] == 'non':
            self.consumer('OPERATEUR', 'non')
            expression = self.parser_facteur()
            return NoeudExpressionBinaire(NoeudBooleen(True), 'non', expression)
        elif token['valeur'] == '-':
            # Opérateur unaire moins (ex: -5)
            self.consumer('OPERATEUR', '-')
            expression = self.parser_facteur()
            return NoeudExpressionBinaire(NoeudNombre(0), '-', expression)
        elif token['valeur'] == '+':
            # Opérateur unaire plus (ex: +5)
            self.consumer('OPERATEUR', '+')
            expression = self.parser_facteur()
            return expression  # +5 est équivalent à 5
        
        raise Exception(f"Expression inattendue: {token}")

    def parser_tableau(self):
        elements = []
        self.consumer('SEPARATEUR', '[')
        if self.regarder_actuel()['valeur'] != ']':
            elements.append(self.parser_expression())
            while self.regarder_actuel()['valeur'] == ',':
                self.consumer('SEPARATEUR', ',')
                elements.append(self.parser_expression())
        self.consumer('SEPARATEUR', ']')
        # Réutiliser NoeudExpressionBinaire avec opérateur spécial 'array'
        return NoeudExpressionBinaire(None, 'array', elements)

    def parser_dictionnaire(self):
        paires = []
        self.consumer('SEPARATEUR', '{')
        if self.regarder_actuel()['valeur'] != '}':
            cle = self.parser_expression()
            self.consumer('SEPARATEUR', ':')
            valeur = self.parser_expression()
            paires.append((cle, valeur))
            while self.regarder_actuel()['valeur'] == ',':
                self.consumer('SEPARATEUR', ',')
                cle = self.parser_expression()
                self.consumer('SEPARATEUR', ':')
                valeur = self.parser_expression()
                paires.append((cle, valeur))
        self.consumer('SEPARATEUR', '}')
        return NoeudExpressionBinaire(None, 'dict', paires)
    
    def consumer(self, type_attendu, valeur_attendue=None):
        token = self.regarder_actuel()
        if token['type'] != type_attendu or (valeur_attendue and token['valeur'] != valeur_attendue):
            raise Exception(f"Attendu {type_attendu}{f'({valeur_attendue})' if valeur_attendue else ''}, obtenu {token}")
        self.position += 1
        return token
    
    def regarder_actuel(self):
        if self.position >= len(self.tokens):
            raise Exception("Fin inattendue du fichier")
        return self.tokens[self.position]