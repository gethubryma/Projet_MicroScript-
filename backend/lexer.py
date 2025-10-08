import re

# Spécification des tokens
TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),              # Nombres entiers ou réels
    ('STRING',   r'"[^"\n]*"'),                # Chaînes de caractères (sur une ligne)
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),   # Identificateurs (variables, mots-clés)

    # Opérateurs (ordre important pour capter les multi-caractères)
    ('OP',       r'\*\*|//|==|!=|>=|<=|[+\-*/%<>=]'),

    ('LPAREN',   r'\('),                       # Parenthèse ouvrante
    ('RPAREN',   r'\)'),                       # Parenthèse fermante
    ('LBRACKET', r'\['),                       # Crochet ouvrant (listes / index)
    ('RBRACKET', r'\]'),                       # Crochet fermant
    ('LBRACE',   r'\{'),                       # Accolade ouvrante (dictionnaires)
    ('RBRACE',   r'\}'),                       # Accolade fermante
    ('DOT',      r'\.'),                       # Point (accès membre éventuel)
    ('COLON',    r':'),                        # Deux-points
    ('COMMA',    r','),                        # Virgule

    ('NEWLINE',  r'\n'),                       # Saut de ligne
    ('SKIP',     r'[ \t]+'),                   # Espaces et tabulations
    ('COMMENT',  r'\#.*'),                     # Commentaires
    ('MISMATCH', r'.'),                        # Tout le reste → erreur
]

# Mots-clés réservés 
KEYWORDS = {
    'if', 'elif', 'else',
    'for', 'while', 'in',
    'print', 'range',
    'def', 'return',
    'true', 'false'
}

def lexer(code):
    """Transforme le texte source en une liste de tokens."""
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            tokens.append(('NUMBER', float(value) if '.' in value else int(value)))

        elif kind == 'STRING':
            tokens.append(('STRING', value))

        elif kind == 'ID':
            lower = value.lower()
            if lower in KEYWORDS:
                tokens.append(('KEYWORD', lower))
            else:
                tokens.append(('ID', value))

        elif kind == 'OP':
            tokens.append(('OP', value))

        elif kind in ('LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'DOT', 'COLON', 'COMMA'):
            tokens.append((kind, value))

        elif kind == 'COMMENT':
            continue

        elif kind in ('NEWLINE', 'SKIP'):
            continue

        elif kind == 'MISMATCH':
            raise SyntaxError(f"Caractère inconnu: {value}")
    
    tokens.append(('EOF', None))  # Fin de fichier
    return tokens
