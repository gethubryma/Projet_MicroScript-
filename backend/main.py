from lexer import lexer

if __name__ == "__main__":
    code_source = """
x = 10
y = x + 5
print(y)
if y > 10:
    print(y)
# commentaire ignoré
"""

    tokens = lexer(code_source)
    for t in tokens:
        print(t)
