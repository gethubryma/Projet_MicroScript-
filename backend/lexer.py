import re

# Spécification des tokens
TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),              # Nombres entiers ou réels
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),   # Identificateurs (variables, mots-clés)
    ('OP',       r'[+\-*/=<>!]'),              # Opérateurs simples
    ('LPAREN',   r'\('),                       # Parenthèse ouvrante
    ('RPAREN',   r'\)'),                       # Parenthèse fermante
    ('COLON',    r':'),                        # Pour if/for/while :
    ('NEWLINE',  r'\n'),                       # Saut de ligne
    ('SKIP',     r'[ \t]+'),                   # Espaces et tabulations
    ('COMMENT',  r'\#.*'),                     # Commentaires
    ('MISMATCH', r'.'),                        # Tout le reste → erreur
]

# Mots-clés réservés 
KEYWORDS = {'if', 'else', 'for', 'while', 'print', 'in', 'range'}

def lexer(code):
    """Transforme le texte source en une liste de tokens."""
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            tokens.append(('NUMBER', float(value) if '.' in value else int(value)))

        elif kind == 'ID':
            if value in KEYWORDS:
                tokens.append(('KEYWORD', value))
            else:
                tokens.append(('ID', value))

        elif kind == 'OP':
            tokens.append(('OP', value))

        elif kind in ('LPAREN', 'RPAREN', 'COLON'):
            tokens.append((kind, value))

        elif kind == 'COMMENT':
            continue  # On ignore les commentaires

        elif kind in ('NEWLINE', 'SKIP'):
            continue  # On ignore les espaces et les sauts de ligne

        elif kind == 'MISMATCH':
            raise SyntaxError(f"Caractère inconnu: {value}")
    
    tokens.append(('EOF', None))  # Fin de fichier
    return tokens
