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
    def __init__(self, condition, body, elifs=None, orelse=None):
        self.condition = condition
        self.body = body
        self.elifs = elifs or []
        self.orelse = orelse or []
    def __repr__(self):
        el = f", elifs={self.elifs}" if self.elifs else ""
        oe = f", else={self.orelse}" if self.orelse else ""
        return f"If({self.condition}, {self.body}{el}{oe})"


class Program:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"


class String:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'String({self.value})'


class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f'While({self.condition}, {self.body})'


class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f'FunctionDef({self.name}, {self.params}, {self.body})'


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f'Call({self.name}, {self.args})'


class Array:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f'Array({self.elements})'


class Bool:
    def __init__(self, value):
        self.value = bool(value)
    def __repr__(self):
        return f'Bool({self.value})'


class Dict:
    def __init__(self, pairs):
        self.pairs = pairs  # list of (key_expr, value_expr)
    def __repr__(self):
        return f'Dict({self.pairs})'


class Index:
    def __init__(self, target, index):
        self.target = target
        self.index = index
    def __repr__(self):
        return f'Index({self.target}, {self.index})'


class ForStmt:
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
    def __repr__(self):
        return f'For({self.var_name}, {self.iterable}, {self.body})'


class Return:
    def __init__(self, value=None):
        self.value = value
    def __repr__(self):
        return f'Return({self.value})'
