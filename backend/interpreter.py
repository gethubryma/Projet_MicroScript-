from backend.ast_nodes import *

class Interpreter:
    def __init__(self):
        # environnement : dictionnaire des variables
        self.env = {}

    def eval(self, node):
        """Évalue un nœud de l’AST."""
        if isinstance(node, Program):
            for stmt in node.statements:
                self.eval(stmt)

        elif isinstance(node, Number):
            return node.value

        elif isinstance(node, Variable):
            if node.name not in self.env:
                raise NameError(f"Variable non définie : {node.name}")
            return self.env[node.name]

        elif isinstance(node, BinaryOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            op = node.op
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            else:
                raise ValueError(f"Opérateur inconnu : {op}")

        elif isinstance(node, Assign):
            value = self.eval(node.value)
            self.env[node.target.name] = value

        elif isinstance(node, PrintStmt):
            value = self.eval(node.expression)
            print(value)

        elif isinstance(node, IfStmt):
            cond = self.eval(node.condition)
            if cond:
                for stmt in node.body:
                    self.eval(stmt)

        else:
            raise ValueError(f"Type de nœud inconnu : {type(node).__name__}")
