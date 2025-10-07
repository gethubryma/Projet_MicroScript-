from backend.ast_nodes import Number, Variable, BinaryOp, Assign, PrintStmt, IfStmt, Program

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def eat(self, expected_type):
        token_type, value = self.current()
        if token_type == expected_type:
            self.pos += 1
            return value
        raise SyntaxError(f"Attendu {expected_type}, obtenu {token_type}")

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self):
        token_type, value = self.current()

        if token_type == 'ID':
            # Affectation : x = expression
            name = self.eat('ID')
            op = self.eat('OP')
            if op != '=':
                raise SyntaxError("Attendu '=' dans une affectation")
            expr = self.parse_expression()
            return Assign(Variable(name), expr)

        elif token_type == 'KEYWORD' and value == 'print':
            self.eat('KEYWORD')
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return PrintStmt(expr)

        elif token_type == 'KEYWORD' and value == 'if':
            self.eat('KEYWORD')
            condition = self.parse_expression()   # on parse l’expression conditionnelle
            self.eat('COLON')
            body = [self.parse_statement()]
            return IfStmt(condition, body)

        else:
            # Expression seule
            return self.parse_expression()

    # Gestion des priorités d’opérateurs
    def parse_expression(self):
        left = self.parse_comparison()
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.current()[0] == 'OP' and self.current()[1] in ('>', '<', '==', '!=', '>=', '<='):
            op = self.eat('OP')
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current()[0] == 'OP' and self.current()[1] in ('+', '-'):
            op = self.eat('OP')
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        return left

    def parse_factor(self):
        left = self.parse_atom()
        while self.current()[0] == 'OP' and self.current()[1] in ('*', '/'):
            op = self.eat('OP')
            right = self.parse_atom()
            left = BinaryOp(left, op, right)
        return left

    def parse_atom(self):
        token_type, value = self.current()
        if token_type == 'NUMBER':
            self.eat('NUMBER')
            return Number(value)
        elif token_type == 'ID':
            self.eat('ID')
            return Variable(value)
        else:
            raise SyntaxError(f"Facteur inattendu : {token_type}")
