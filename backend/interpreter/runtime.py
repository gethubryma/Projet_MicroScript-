# backend/interpreter/runtime.py

from typing import Any, Dict, Optional, List, Tuple

try:
    # Chargement facultatif de la stdlib pour préremplir le global
    from backend.stdlib import BUILTINS as _BUILTINS  # type: ignore
except Exception:
    _BUILTINS = {}  # fallback si stdlib pas encore créée


class RuntimeErrorMS(Exception):
    """Erreur d'exécution avec position optionnelle."""
    def __init__(self, message: str, line: Optional[int] = None, col: Optional[int] = None, filename: str = "<stdin>"):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        where = ""
        if line is not None:
            where = f" (line {line}"
            if col is not None:
                where += f", col {col}"
            where += f", file {filename})"
        super().__init__(message + where)


class ReturnSignal(Exception):
    """Signal interne pour 'return' dans une fonction."""
    def __init__(self, value: Any = None):
        self.value = value


class Env:
    """Environnement chaîné (scope)."""
    def __init__(self, bindings: Optional[Dict[str, Any]] = None, parent: Optional["Env"] = None):
        self.bindings: Dict[str, Any] = dict(bindings or {})
        self.parent: Optional["Env"] = parent

    def define(self, name: str, value: Any) -> None:
        self.bindings[name] = value

    def resolve(self, name: str) -> Optional["Env"]:
        cur: Optional["Env"] = self
        while cur is not None:
            if name in cur.bindings:
                return cur
            cur = cur.parent
        return None

    def set(self, name: str, value: Any) -> None:
        found = self.resolve(name)
        if found is None:
            # par défaut, affectation crée dans l'env courant si non trouvé
            self.bindings[name] = value
        else:
            found.bindings[name] = value

    def get(self, name: str) -> Any:
        found = self.resolve(name)
        if found is None:
            raise NameError(f"Variable non définie : {name}")
        return found.bindings[name]

    def new_child(self, initial: Optional[Dict[str, Any]] = None) -> "Env":
        return Env(bindings=initial, parent=self)

    def to_dict_flat(self) -> Dict[str, Any]:
        """Fusionne les bindings depuis la chaîne d'envs (lecture seule)."""
        out: Dict[str, Any] = {}
        chain: List[Env] = []
        cur: Optional[Env] = self
        while cur is not None:
            chain.append(cur)
            cur = cur.parent
        for env in reversed(chain):
            out.update(env.bindings)
        return out


class Frame:
    """Frame d'appel."""
    def __init__(
        self,
        func_name: str,
        env: Env,
        filename: str = "<stdin>",
        call_line: Optional[int] = None,
        call_col: Optional[int] = None,
    ):
        self.func_name = func_name
        self.env = env
        self.filename = filename
        self.call_line = call_line
        self.call_col = call_col

    def info(self) -> Dict[str, Any]:
        return {
            "function": self.func_name,
            "filename": self.filename,
            "line": self.call_line,
            "col": self.call_col,
            "locals": self.env.bindings.copy(),
        }


class CallStack:
    """Pile d'appels."""
    def __init__(self):
        self._frames: List[Frame] = []

    def push(self, frame: Frame) -> None:
        self._frames.append(frame)

    def pop(self) -> Frame:
        if not self._frames:
            raise RuntimeErrorMS("Pop de pile d'appels vide")
        return self._frames.pop()

    def top(self) -> Optional[Frame]:
        return self._frames[-1] if self._frames else None

    def as_list(self) -> List[Dict[str, Any]]:
        return [f.info() for f in reversed(self._frames)]


class BreakpointManager:
    """Gestion simple des breakpoints par fichier/ligne."""
    def __init__(self):
        self._bp: Dict[str, set] = {}

    def clear(self) -> None:
        self._bp.clear()

    def add(self, filename: str, line: int) -> None:
        self._bp.setdefault(filename, set()).add(int(line))

    def remove(self, filename: str, line: int) -> None:
        if filename in self._bp:
            self._bp[filename].discard(int(line))
            if not self._bp[filename]:
                del self._bp[filename]

    def has(self, filename: str, line: Optional[int]) -> bool:
        if line is None:
            return False
        return int(line) in self._bp.get(filename, set())

    def snapshot(self) -> Dict[str, List[int]]:
        return {k: sorted(v) for k, v in self._bp.items()}


class Runtime:
    """
    Regroupe global_env, call stack, breakpoints, et expose des hooks utiles
    pour l'interpréteur (before/after execution).
    """
    def __init__(self, builtins: Optional[Dict[str, Any]] = None, filename: str = "<stdin>"):
        base = dict(_BUILTINS)
        if builtins:
            base.update(builtins)
        self.global_env = Env(bindings=base, parent=None)
        self.filename = filename
        self.stack = CallStack()
        self.breakpoints = BreakpointManager()
        self.paused = False
        self.step_mode = False  # si tu veux un step-by-step

    def new_child_env(self, initial: Optional[Dict[str, Any]] = None) -> Env:
        return self.global_env.new_child(initial)

    def enter_function(
        self,
        func_name: str,
        params: List[str],
        args: List[Any],
        caller_env: Env,
        call_line: Optional[int] = None,
        call_col: Optional[int] = None,
    ) -> Env:
        local_bindings = dict(zip(params, args))
        local_env = Env(bindings=local_bindings, parent=caller_env)
        frame = Frame(func_name=func_name, env=local_env, filename=self.filename, call_line=call_line, call_col=call_col)
        self.stack.push(frame)
        return local_env

    def leave_function(self) -> None:
        self.stack.pop()

    def current_env(self) -> Env:
        top = self.stack.top()
        return top.env if top is not None else self.global_env

    def set_breakpoints(self, filename: str, lines: List[int]) -> None:
        self.breakpoints.clear()
        for ln in lines:
            self.breakpoints.add(filename, ln)

    def before_stmt(self, line: Optional[int] = None, col: Optional[int] = None) -> bool:
        """
        Hook à appeler par l'interpréteur avant chaque statement.
        Retourne True si l'exécution doit se mettre en pause (breakpoint ou step).
        """
        if self.step_mode:
            self.paused = True
            return True
        if self.breakpoints.has(self.filename, line):
            self.paused = True
            return True
        return False

    def continue_(self) -> None:
        self.paused = False
        self.step_mode = False

    def step(self) -> None:
        self.paused = False
        self.step_mode = True

    def variables_snapshot(self) -> Dict[str, Any]:
        env = self.current_env()
        return env.to_dict_flat()

    def callstack_snapshot(self) -> List[Dict[str, Any]]:
        return self.stack.as_list()


def make_runtime(filename: str = "<stdin>", builtins: Optional[Dict[str, Any]] = None) -> Runtime:
    return Runtime(builtins=builtins, filename=filename)
