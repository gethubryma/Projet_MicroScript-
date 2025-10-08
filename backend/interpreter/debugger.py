from typing import Any, Callable, Dict, List, Optional, Tuple
import io
import sys

from backend.interpreter.runtime import Runtime, make_runtime, ReturnSignal, RuntimeErrorMS

class StdoutCapture:
    def __init__(self):
        self._buf = io.StringIO()
        self._old = None

    def __enter__(self):
        self._old = sys.stdout
        sys.stdout = self._buf
        return self

    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._old

    @property
    def text(self) -> str:
        return self._buf.getvalue()


class Debugger:
    """
    Orchestrateur de debug : runtime + interpréteur + programme.
    Fournit : set_breakpoints, continue, step, variables, callstack,
    run_until_pause, run_to_end, capture stdout, etc.
    """
    def __init__(
        self,
        interpreter_factory: Callable[[Runtime], Any],
        filename: str = "<stdin>"
    ):
        self.filename = filename
        self.runtime: Runtime = make_runtime(filename=filename)
        self._make_interpreter = interpreter_factory
        self.interpreter = self._make_interpreter(self.runtime)
        self._program = None
        self._paused = False
        self._last_output = ""

    # Chargement programme/AST
    def load_program(self, program_ast: Any) -> None:
        self._program = program_ast

    def reset(self) -> None:
        self.runtime = make_runtime(filename=self.filename)
        self.interpreter = self._make_interpreter(self.runtime)
        self._program = None
        self._paused = False
        self._last_output = ""

    # Breakpoints / contrôle
    def set_breakpoints(self, lines: List[int]) -> None:
        self.runtime.set_breakpoints(self.filename, lines)

    def clear_breakpoints(self) -> None:
        self.runtime.breakpoints.clear()

    def continue_(self) -> Dict[str, Any]:
        self.runtime.continue_()
        return self._run_until_pause()

    def step(self) -> Dict[str, Any]:
        self.runtime.step()
        return self._run_until_pause()

    def run_to_end(self) -> Dict[str, Any]:
        self.runtime.continue_()
        return self._run(full=True)

    def variables(self) -> Dict[str, Any]:
        return self.runtime.variables_snapshot()

    def callstack(self) -> List[Dict[str, Any]]:
        return self.runtime.callstack_snapshot()

    def is_paused(self) -> bool:
        return self.runtime.paused

    def last_output(self) -> str:
        return self._last_output

    # Exécution
    def _run_until_pause(self) -> Dict[str, Any]:
        return self._run(full=False)

    def _run(self, full: bool) -> Dict[str, Any]:
        if self._program is None:
            raise RuntimeErrorMS("Aucun programme chargé", filename=self.filename)

        out = ""
        err = None
        paused = False

        try:
            with StdoutCapture() as cap:
                # L’interpréteur doit consulter runtime.before_stmt(...) avant chaque statement
                # pour que les breakpoints/step prennent effet. Ici on lance l’évaluation :
                self.interpreter.eval(self._program)
                out = cap.text
        except ReturnSignal as rs:
            out = out + ""
            paused = False
        except RuntimeErrorMS as ex:
            err = str(ex)
            paused = False
        except Exception as ex:
            err = f"RuntimeError: {ex}"
            paused = False
        finally:
            # Si le hook before_stmt a mis paused=True en cours de route, on le reflète ici
            paused = paused or self.runtime.paused
            self._paused = paused
            self._last_output = out

        result = {
            "paused": paused,
            "output": out,
            "error": err,
            "breakpoints": self.runtime.breakpoints.snapshot(),
            "variables": self.variables(),
            "callstack": self.callstack(),
        }
        return result

def default_interpreter_factory(InterpreterClass):
    def factory(rt: Runtime):
        return InterpreterClass() if rt is None else InterpreterClass()
    return factory
