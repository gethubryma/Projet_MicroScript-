# syntaxe.py
class SyntaxeFr:
    MOTS_CLES = {
        'variable': 'variable',
        'si': 'si',
        'sinon': 'sinon',
        'fin_si': 'fin_si',
        'tant_que': 'tant_que',
        'fin_tant_que': 'fin_tant_que',
        'afficher': 'afficher',
        'fonction': 'fonction',
        'fin_fonction': 'fin_fonction',
        'retour': 'retour'
    }
    
    FONCTIONS_BUILTIN = {
        'lire', 'input', 'len', 'sqrt', 'sin', 'cos', 'tan', 'abs', 'round',
        'maj', 'min', 'random', 'date', 'heure', 'annee', 'mois', 'jour'
    }
    
    OPERATEURS = {
        '+', '-', '*', '/', '%',
        '==','=', '!=', '<', '>', '<=', '>=',
        'et', 'ou', 'non'
    }
    
    SEPARATEURS = {'(', ')', '{', '}', '[', ']', ',', ';', ':'}