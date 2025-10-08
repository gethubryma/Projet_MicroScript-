from typing import Any, List
from backend.ast_nodes import (
    Program, Number, String, Bool, Array, Dict,
    Variable, Assign, BinaryOp, PrintStmt,
    IfStmt, WhileStmt, ForStmt,
    FunctionDef, FunctionCall, Return, Index
)
from backend.interpreter.runtime import (
    Runtime, Env, ReturnSignal, RuntimeErrorMS
)


class UserFunction:
    def __init__(self, name: str, params: List[str], body: List[Any], closure_env: Env):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env

    def __repr__(self):
        return f"<Function {self.name}({', '.join(self.params)})>"


class Evaluator:
    def __init__(self, runtime: Runtime):
        self.rt = runtime

    def eval(self, node: Any) -> Any:
        t = type(node)

        if t is Program:
            for stmt in node.statements:
                self._before_stmt()
                self.eval(stmt)
            return None

        if t is Number:
            return node.value

        if t is String:
            v = node.value
            if isinstance(v, str) and len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                return v[1:-1]
            return v

        if t is Bool:
            return bool(node.value)

        if t is Array:
            return [self.eval(e) for e in node.elements]

        if t is Dict:
            out = {}
            for k_expr, v_expr in node.pairs:
                k = self.eval(k_expr)
                v = self.eval(v_expr)
                out[k] = v
            return out

        if t is Variable:
            env = self.rt.current_env()
            return env.get(node.name)

        if t is Index:
            target = self.eval(node.target)
            idx = self.eval(node.index)
            try:
                return target[idx]
            except Exception as ex:
                raise RuntimeErrorMS(f"Indexation invalide: {ex}", filename=self.rt.filename)

        if t is BinaryOp:
            left = self.eval(node.left)
            right = self.eval(node.right)
            op = node.op
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if op == '-':
                return left - right
            if op == '*':
                return left * right
            if op == '/':
                return left / right
            if op == '//':
                return left // right
            if op == '%':
                return left % right
            if op == '**':
                return left ** right
            if op == '>':
                return left > right
            if op == '<':
                return left < right
            if op == '==':
                return left == right
            if op == '!=':
                return left != right
            if op == '>=':
                return left >= right
            if op == '<=':
                return left <= right
            raise RuntimeErrorMS(f"Opérateur inconnu: {op}", filename=self.rt.filename)

        if t is Assign:
            env = self.rt.current_env()
            value = self.eval(node.value)
            if isinstance(node.target, Variable):
                env.set(node.target.name, value)
                return None
            if isinstance(node.target, Index):
                target = self.eval(node.target.target)
                idx = self.eval(node.target.index)
                try:
                    target[idx] = value
                except Exception as ex:
                    raise RuntimeErrorMS(f"Affectation index invalide: {ex}", filename=self.rt.filename)
                return None
            raise RuntimeErrorMS("Cible d'affectation invalide", filename=self.rt.filename)

        if t is PrintStmt:
            val = self.eval(node.expression)
            print(val)
            return None

        if t is IfStmt:
            if self._truthy(self.eval(node.condition)):
                for s in node.body:
                    self._before_stmt()
                    self.eval(s)
            else:
                done = False
                for cond, body in getattr(node, "elifs", []):
                    if self._truthy(self.eval(cond)):
                        for s in body:
                            self._before_stmt()
                            self.eval(s)
                        done = True
                        break
                if not done:
                    for s in getattr(node, "orelse", []):
                        self._before_stmt()
                        self.eval(s)
            return None

        if t is WhileStmt:
            guard = 0
            while self._truthy(self.eval(node.condition)):
                for s in node.body:
                    self._before_stmt()
                    self.eval(s)
                guard += 1
                if guard > 1_000_000:
                    raise RuntimeErrorMS("Boucle infinie détectée (>1e6 itérations)", filename=self.rt.filename)
            return None

        if t is ForStmt:
            env = self.rt.current_env()
            iterable = self.eval(node.iterable)
            try:
                iterator = iter(iterable)
            except Exception:
                raise RuntimeErrorMS("Objet non itérable dans 'for'", filename=self.rt.filename)
            for v in iterator:
                env.set(node.var_name, v)
                for s in node.body:
                    self._before_stmt()
                    self.eval(s)
            return None

        if t is FunctionDef:
            closure = self.rt.current_env()
            fn = UserFunction(node.name, node.params, node.body, closure)
            closure.set(node.name, fn)
            return None

        if t is FunctionCall:
            env = self.rt.current_env()
            callee = env.get(node.name)
            args = [self.eval(a) for a in node.args]

            if isinstance(callee, UserFunction):
                local_env = self.rt.enter_function(
                    func_name=callee.name,
                    params=callee.params,
                    args=args,
                    caller_env=callee.closure_env,
                    call_line=None,
                    call_col=None,
                )
                try:
                    for s in callee.body:
                        self._before_stmt()
                        self.eval(s)
                except ReturnSignal as rs:
                    self.rt.leave_function()
                    return rs.value
                self.rt.leave_function()
                return None

            if callable(callee):
                return callee(*args)

            raise RuntimeErrorMS(f"Objet appelable inconnu: {callee}", filename=self.rt.filename)

        if t is Return:
            if node.value is None:
                raise ReturnSignal(None)
            val = self.eval(node.value)
            raise ReturnSignal(val)

        raise RuntimeErrorMS(f"Nœud AST non géré: {t.__name__}", filename=self.rt.filename)

    def _truthy(self, v: Any) -> bool:
        return bool(v)

    def _before_stmt(self):
        self.rt.before_stmt(line=None, col=None)
