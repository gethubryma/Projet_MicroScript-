from backend.lexer import lexer
from backend.parser import Parser
from backend.ast_nodes import Assign, Variable, Number, BinaryOp

def test_simple_expression():
    code = "x = 2 + 3"
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast.statements[0], Assign)
    assert isinstance(ast.statements[0].value, BinaryOp)
    assert isinstance(ast.statements[0].value.left, Number)
    assert isinstance(ast.statements[0].value.right, Number)

