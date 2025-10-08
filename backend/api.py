from flask import Flask, request, jsonify
from flask_cors import CORS
from io import StringIO
import sys
import uuid

from backend.lexer import lexer
from backend.parser import Parser

from backend.interpreter.runtime import make_runtime, RuntimeErrorMS
from backend.interpreter.evaluator import Evaluator
from backend.interpreter.debugger import Debugger
from backend.errors import format_error

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SESSIONS = {}         # { session_id: {"runtime": Runtime, "evaluator": Evaluator, "buffer": ""} }
DEBUG_SESSIONS = {}   # { session_id: {"debugger": Debugger, "ast": Program} }


def _eval_with_capture(code, runtime=None, evaluator=None):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()

        if runtime is None:
            runtime = make_runtime(filename="<stdin>")
        if evaluator is None:
            evaluator = Evaluator(runtime)

        evaluator.eval(ast)
        output = sys.stdout.getvalue()
        return True, output, runtime, evaluator
    except Exception as e:
        return False, f"Erreur : {format_error(e)}", runtime, evaluator
    finally:
        sys.stdout = old_stdout


@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json() or {}
    code = data.get("code", "")
    ok, out, _, _ = _eval_with_capture(code)
    return jsonify({"success": ok, "output": out})


@app.route("/repl/init", methods=["POST"])
def repl_init():
    session_id = str(uuid.uuid4())
    rt = make_runtime(filename="<stdin>")
    ev = Evaluator(rt)
    SESSIONS[session_id] = {"runtime": rt, "evaluator": ev, "buffer": ""}
    return jsonify({"session_id": session_id})


@app.route("/repl/reset", methods=["POST"])
def repl_reset():
    data = request.get_json() or {}
    sid = data.get("session_id")
    if not sid or sid not in SESSIONS:
        return jsonify({"success": False, "output": "Session inconnue."}), 400
    rt = make_runtime(filename="<stdin>")
    ev = Evaluator(rt)
    SESSIONS[sid] = {"runtime": rt, "evaluator": ev, "buffer": ""}
    return jsonify({"success": True, "output": "Session réinitialisée."})


@app.route("/repl/exec", methods=["POST"])
def repl_exec():
    data = request.get_json() or {}
    sid = data.get("session_id")
    line = data.get("line", "")

    if not sid:
        return jsonify({"success": False, "output": "session_id manquant."}), 400
    if sid not in SESSIONS:
        rt = make_runtime(filename="<stdin>")
        ev = Evaluator(rt)
        SESSIONS[sid] = {"runtime": rt, "evaluator": ev, "buffer": ""}

    rt = SESSIONS[sid]["runtime"]
    ev = SESSIONS[sid]["evaluator"]
    buf = SESSIONS[sid]["buffer"]

    code = (buf + "\n" + line) if buf else line

    if line.strip().endswith(":"):
        SESSIONS[sid]["buffer"] = code
        return jsonify({"success": True, "output": "... (suite attendue)", "more": True})

    ok, out, rt, ev = _eval_with_capture(code, runtime=rt, evaluator=ev)
    if ok:
        SESSIONS[sid]["buffer"] = ""
        SESSIONS[sid]["runtime"] = rt
        SESSIONS[sid]["evaluator"] = ev
        return jsonify({"success": True, "output": out, "more": False})
    else:
        if line.strip().endswith(":"):
            SESSIONS[sid]["buffer"] = code
            return jsonify({"success": True, "output": "... (suite attendue)", "more": True})
        return jsonify({"success": False, "output": out, "more": False}), 400


def _make_debugger():
    return Debugger(lambda rt: Evaluator(rt), filename="<stdin>")


@app.route("/debug/start", methods=["POST"])
def debug_start():
    data = request.get_json() or {}
    code = data.get("code", "")
    bps = data.get("breakpoints", []) or []

    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()

        dbg = _make_debugger()
        dbg.load_program(ast)
        if bps:
            dbg.set_breakpoints(bps)

        state = dbg.step()
        sid = str(uuid.uuid4())
        DEBUG_SESSIONS[sid] = {"debugger": dbg, "ast": ast}
        return jsonify({"session_id": sid, "state": state})
    except Exception as e:
        return jsonify({"error": format_error(e)}), 400


@app.route("/debug/set_breakpoints", methods=["POST"])
def debug_set_breakpoints():
    data = request.get_json() or {}
    sid = data.get("session_id")
    bps = data.get("breakpoints", []) or []
    if not sid or sid not in DEBUG_SESSIONS:
        return jsonify({"error": "Session debug inconnue"}), 400

    dbg = DEBUG_SESSIONS[sid]["debugger"]
    dbg.set_breakpoints(bps)
    return jsonify({"ok": True, "breakpoints": dbg.runtime.breakpoints.snapshot()})


@app.route("/debug/continue", methods=["POST"])
def debug_continue():
    data = request.get_json() or {}
    sid = data.get("session_id")
    if not sid or sid not in DEBUG_SESSIONS:
        return jsonify({"error": "Session debug inconnue"}), 400

    dbg = DEBUG_SESSIONS[sid]["debugger"]
    state = dbg.continue_()
    return jsonify({"state": state})


@app.route("/debug/step", methods=["POST"])
def debug_step():
    data = request.get_json() or {}
    sid = data.get("session_id")
    if not sid or sid not in DEBUG_SESSIONS:
        return jsonify({"error": "Session debug inconnue"}), 400

    dbg = DEBUG_SESSIONS[sid]["debugger"]
    state = dbg.step()
    return jsonify({"state": state})


@app.route("/debug/state", methods=["GET"])
def debug_state():
    sid = request.args.get("session_id")
    if not sid or sid not in DEBUG_SESSIONS:
        return jsonify({"error": "Session debug inconnue"}), 400

    dbg = DEBUG_SESSIONS[sid]["debugger"]
    state = {
        "paused": dbg.is_paused(),
        "output": dbg.last_output(),
        "variables": dbg.variables(),
        "callstack": dbg.callstack(),
        "breakpoints": dbg.runtime.breakpoints.snapshot(),
        "filename": dbg.filename,
    }
    return jsonify({"state": state})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
