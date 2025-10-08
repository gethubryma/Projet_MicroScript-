from backend.ast_nodes import (
    Number, Variable, BinaryOp, Assign, PrintStmt, IfStmt, Program,
    WhileStmt, FunctionDef, FunctionCall, Array, String,
    Bool, Dict, Index, ForStmt, Return
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ('EOF', None)

    def eat(self, expected_type):
        token_type, value = self.current()
        if token_type == expected_type:
            self.pos += 1
            return value
        raise SyntaxError(f"Attendu {expected_type}, obtenu {token_type}")

    def eat_specific(self, expected_type, expected_value):
        token_type, value = self.current()
        if token_type == expected_type and value == expected_value:
            self.pos += 1
            return value
        raise SyntaxError(f"Attendu {expected_type}='{expected_value}', obtenu {token_type}='{value}'")

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            if self.current()[0] == 'NEWLINE':
                self.eat('NEWLINE')
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_block(self):
        body = []
        while self.current()[0] == 'NEWLINE':
            self.eat('NEWLINE')
        while self.current()[0] not in ('EOF', 'DEDENT'):
            if self.current()[0] == 'EOF':
                break
            if self.current()[0] == 'NEWLINE':
                self.eat('NEWLINE')
                continue
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current()[0] == 'NEWLINE':
                self.eat('NEWLINE')
            if self.current()[0] in ('EOF', 'DEDENT', 'COLON'):
                break
        return body

    def parse_statement(self):
        token_type, value = self.current()

        if token_type == 'ID':
            if self.peek()[0] == 'LPAREN':
                return self.parse_function_call()
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
            self.eat('KEYWORD')  # if
            condition = self.parse_expression()
            self.eat('COLON')
            body = self.parse_block()
            elifs = []
            orelse = []
            while self.current()[0] == 'KEYWORD' and self.current()[1] == 'elif':
                self.eat('KEYWORD')  # elif
                c = self.parse_expression()
                self.eat('COLON')
                b = self.parse_block()
                elifs.append((c, b))
            if self.current()[0] == 'KEYWORD' and self.current()[1] == 'else':
                self.eat('KEYWORD')
                self.eat('COLON')
                orelse = self.parse_block()
            return IfStmt(condition, body, elifs=elifs, orelse=orelse)

        elif token_type == 'KEYWORD' and value == 'while':
            self.eat('KEYWORD')
            condition = self.parse_expression()
            self.eat('COLON')
            body = self.parse_block()
            return WhileStmt(condition, body)

        elif token_type == 'KEYWORD' and value == 'for':
            self.eat('KEYWORD')  # for
            var_name = self.eat('ID')
            self.eat_specific('KEYWORD', 'in')
            iterable = self.parse_expression()
            self.eat('COLON')
            body = self.parse_block()
            return ForStmt(var_name, iterable, body)

        elif token_type == 'KEYWORD' and value == 'def':
            self.eat('KEYWORD')
            name = self.eat('ID')
            self.eat('LPAREN')
            params = []
            if self.current()[0] == 'ID':
                params.append(self.eat('ID'))
                while self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                    params.append(self.eat('ID'))
            self.eat('RPAREN')
            self.eat('COLON')
            body = [self.parse_statement()]
            return FunctionDef(name, params, body)

        elif token_type == 'KEYWORD' and value == 'return':
            self.eat('KEYWORD')
            if self.current()[0] in ('NEWLINE', 'EOF', 'DEDENT'):
                return Return(None)
            val = self.parse_expression()
            return Return(val)

        else:
            expr = self.parse_expression()
            return expr

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_add()
        while self.current()[0] == 'OP' and self.current()[1] in ('>', '<', '==', '!=', '>=', '<='):
            op = self.eat('OP')
            right = self.parse_add()
            left = BinaryOp(left, op, right)
        return left

    def parse_add(self):
        left = self.parse_mul()
        while self.current()[0] == 'OP' and self.current()[1] in ('+', '-'):
            op = self.eat('OP')
            right = self.parse_mul()
            left = BinaryOp(left, op, right)
        return left

    def parse_mul(self):
        left = self.parse_power()
        while self.current()[0] == 'OP' and self.current()[1] in ('*', '/', '//', '%'):
            op = self.eat('OP')
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        return left

    def parse_power(self):
        left = self.parse_unary()
        if self.current()[0] == 'OP' and self.current()[1] == '**':
            op = self.eat('OP')
            right = self.parse_power()  # droite-associatif
            left = BinaryOp(left, op, right)
        return left

    def parse_unary(self):
        if self.current()[0] == 'OP' and self.current()[1] in ('+', '-'):
            op = self.eat('OP')
            expr = self.parse_unary()
            if op == '+':
                return BinaryOp(Number(0), '+', expr)
            else:
                return BinaryOp(Number(0), '-', expr)
        return self.parse_postfix()

    def parse_postfix(self):
        node = self.parse_atom()
        while True:
            tok_type, tok_val = self.current()
            if tok_type == 'LBRACKET':
                self.eat('LBRACKET')
                idx = self.parse_expression()
                self.eat('RBRACKET')
                node = Index(node, idx)
                continue
            else:
                break
        return node

    def parse_atom(self):
        token_type, value = self.current()

        if token_type == 'NUMBER':
            self.eat('NUMBER')
            return Number(value)

        elif token_type == 'STRING':
            self.eat('STRING')
            return String(value)

        elif token_type == 'KEYWORD' and value in ('true', 'false'):
            self.eat('KEYWORD')
            return Bool(True if value == 'true' else False)

        elif token_type == 'ID':
            if self.peek()[0] == 'LPAREN':
                return self.parse_function_call()
            name = self.eat('ID')
            return Variable(name)

        elif token_type == 'LBRACKET':
            self.eat('LBRACKET')
            elements = []
            if self.current()[0] != 'RBRACKET':
                elements.append(self.parse_expression())
                while self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                    elements.append(self.parse_expression())
            self.eat('RBRACKET')
            return Array(elements)

        elif token_type == 'LBRACE':
            self.eat('LBRACE')
            pairs = []
            if self.current()[0] != 'RBRACE':
                k = self.parse_expression()
                self.eat('COLON')
                v = self.parse_expression()
                pairs.append((k, v))
                while self.current()[0] == 'COMMA':
                    self.eat('COMMA')
                    k = self.parse_expression()
                    self.eat('COLON')
                    v = self.parse_expression()
                    pairs.append((k, v))
            self.eat('RBRACE')
            return Dict(pairs)

        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr

        else:
            raise SyntaxError(f"Facteur inattendu : {token_type}")

    def parse_function_call(self):
        name = self.eat('ID')
        self.eat('LPAREN')
        args = []
        if self.current()[0] != 'RPAREN':
            args.append(self.parse_expression())
            while self.current()[0] == 'COMMA':
                self.eat('COMMA')
                args.append(self.parse_expression())
        self.eat('RPAREN')
        return FunctionCall(name, args)
