class NumberNode:
    def __init__(self, value):
        self.value = value

class IdentifierNode:
    def __init__(self, name):
        self.name = name

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignmentNode:
    def __init__(self, target, value):
        self.target = target
        self.value = value

class PrintNode:
    def __init__(self, expression):
        self.expression = expression
