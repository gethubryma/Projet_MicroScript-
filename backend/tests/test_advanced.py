from backend.lexer import lexer
from backend.parser import Parser
from backend.interpreter import Interpreter

def run_code(code):
    import io, sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.eval(ast)
        output = sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout
    return output


def test_while_loop():
    code = """
x = 0
while x < 3:
    print(x)
    x = x + 1
"""
    result = run_code(code)
    assert result == "0\n1\n2"


def test_function_def_and_call():
    code = """
def add(a, b):
    print(a + b)
add(2, 3)
"""
    result = run_code(code)
    assert result == "5"


def test_string_and_array():
    code = """
text = "Hello"
nums = [1, 2, 3]
print(text)
print(nums)
"""
    result = run_code(code)
    assert result == "Hello\n[1, 2, 3]"


def test_if_and_comparison():
    code = """
x = 10
if x > 5:
    print("OK")
"""
    result = run_code(code)
    assert result == "OK"
