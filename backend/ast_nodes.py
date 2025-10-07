class Number:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"


class Variable:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Variable({self.name})"


class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOp({self.left}, '{self.op}', {self.right})"


class Assign:
    def __init__(self, target, value):
        self.target = target
        self.value = value
    def __repr__(self):
        return f"Assign({self.target}, {self.value})"


class PrintStmt:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"Print({self.expression})"


class IfStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"If({self.condition}, {self.body})"


class Program:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"
