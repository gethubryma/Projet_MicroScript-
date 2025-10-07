from backend.lexer import lexer

def test_lexer():
    code = "x = 3 + 5"
    tokens = lexer(code)
    expected = [
        ('ID', 'x'),
        ('OP', '='),
        ('NUMBER', 3),
        ('OP', '+'),
        ('NUMBER', 5),
        ('EOF', None)
    ]
    assert tokens == expected
