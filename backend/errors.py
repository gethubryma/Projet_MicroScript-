# backend/errors.py
from typing import Optional

# Base commune
class MicroScriptError(Exception):
    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        col: Optional[int] = None,
        filename: str = "<stdin>",
    ):
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        super().__init__(self._fmt())

    def _fmt(self) -> str:
        loc = ""
        if self.line is not None:
            loc = f" (line {self.line}"
            if self.col is not None:
                loc += f", col {self.col}"
            loc += f", file {self.filename})"
        return f"{self.message}{loc}"

    def __str__(self) -> str:
        return self._fmt()


# Erreurs de lexing et parsing (avec position optionnelle)
class LexError(MicroScriptError):
    pass


class ParseError(MicroScriptError):
    pass


# Réexport de l'erreur runtime depuis le moteur pour éviter deux classes différentes
try:
    from backend.interpreter.runtime import RuntimeErrorMS  # type: ignore
except Exception:
    # Fallback si runtime non disponible au moment de l'import
    class RuntimeErrorMS(MicroScriptError):
        pass


# Aides de formatage
def format_error(e: BaseException) -> str:
    if isinstance(e, MicroScriptError):
        return str(e)
    return f"{e.__class__.__name__}: {e}"


def make_lex_error(msg: str, line: Optional[int] = None, col: Optional[int] = None, filename: str = "<stdin>") -> LexError:
    return LexError(msg, line=line, col=col, filename=filename)


def make_parse_error(msg: str, line: Optional[int] = None, col: Optional[int] = None, filename: str = "<stdin>") -> ParseError:
    return ParseError(msg, line=line, col=col, filename=filename)


def make_runtime_error(msg: str, line: Optional[int] = None, col: Optional[int] = None, filename: str = "<stdin>") -> RuntimeErrorMS:
    return RuntimeErrorMS(msg, line=line, col=col, filename=filename)  # type: ignore
