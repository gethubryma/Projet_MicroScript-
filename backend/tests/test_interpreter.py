from backend.lexer import lexer
from backend.parser import Parser
from backend.interpreter import Interpreter

def test_interpreter_basic(capsys):
    code = "x = 2\ny = x + 3\nprint(y)"
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.eval(ast)

    captured = capsys.readouterr()
    assert captured.out.strip() == "5"

