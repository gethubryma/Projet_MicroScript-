from flask import Flask, request, jsonify
from flask_cors import CORS
from io import StringIO
import sys
import uuid

from backend.lexer import lexer
from backend.parser import Parser
from backend.interpreter import Interpreter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Sessions REPL (mémoire en RAM)
SESSIONS = {}  # { session_id: {"interpreter": Interpreter(), "buffer": ""} }


def _run_with_capture(code, interpreter=None):
    """Exécute du code MicroScript en capturant stdout.
       Si interpreter est fourni, réutilise son environnement (REPL)."""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()
        if interpreter is None:
            interpreter = Interpreter()
        interpreter.eval(ast)
        output = sys.stdout.getvalue()
        return True, output, interpreter
    except Exception as e:
        return False, f"Erreur : {e}", interpreter
    finally:
        sys.stdout = old_stdout


@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json() or {}
    code = data.get("code", "")
    ok, out, _ = _run_with_capture(code)
    return jsonify({"success": ok, "output": out})


@app.route("/repl/init", methods=["POST"])
def repl_init():
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"interpreter": Interpreter(), "buffer": ""}
    return jsonify({"session_id": session_id})


@app.route("/repl/reset", methods=["POST"])
def repl_reset():
    data = request.get_json() or {}
    sid = data.get("session_id")
    if not sid or sid not in SESSIONS:
        return jsonify({"success": False, "output": "Session inconnue."}), 400
    SESSIONS[sid] = {"interpreter": Interpreter(), "buffer": ""}
    return jsonify({"success": True, "output": "Session réinitialisée."})


@app.route("/repl/exec", methods=["POST"])
def repl_exec():
    data = request.get_json() or {}
    sid = data.get("session_id")
    line = data.get("line", "")

    if not sid:
        return jsonify({"success": False, "output": "session_id manquant."}), 400
    if sid not in SESSIONS:
        SESSIONS[sid] = {"interpreter": Interpreter(), "buffer": ""}

    interp = SESSIONS[sid]["interpreter"]
    buf = SESSIONS[sid]["buffer"]

    # Accumule si on est dans un bloc (ex: "if cond:")
    if buf:
        code = buf + "\n" + line
    else:
        code = line

    # Heuristique simple : si la ligne se termine par ":", on attend la suite
    if line.strip().endswith(":"):
        SESSIONS[sid]["buffer"] = code
        return jsonify({"success": True, "output": "... (suite attendue)", "more": True})

    # Essaye d'exécuter
    ok, out, interp = _run_with_capture(code, interpreter=interp)
    if ok:
        SESSIONS[sid]["buffer"] = ""     # code complet exécuté
        SESSIONS[sid]["interpreter"] = interp
        return jsonify({"success": True, "output": out, "more": False})
    else:
        # Si erreur et que le code se termine par ":" on garde en buffer
        if line.strip().endswith(":"):
            SESSIONS[sid]["buffer"] = code
            return jsonify({"success": True, "output": "... (suite attendue)", "more": True})
        return jsonify({"success": False, "output": out, "more": False}), 400


if __name__ == "__main__":
    app.run(debug=True)
