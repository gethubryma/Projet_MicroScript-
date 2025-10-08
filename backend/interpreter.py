# backend/interpreter.py
from backend.interpreter.runtime import make_runtime
from backend.interpreter.evaluator import Evaluator

class Interpreter:
    def __init__(self, runtime=None, filename: str = "<stdin>"):
        self.runtime = runtime or make_runtime(filename=filename)
        self.evaluator = Evaluator(self.runtime)

    def eval(self, node):
        return self.evaluator.eval(node)

    # utilitaires optionnels
    def get_globals(self):
        return self.runtime.global_env.to_dict_flat()

    def set_global(self, name, value):
        self.runtime.global_env.set(name, value)
