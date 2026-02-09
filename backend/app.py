# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from lexer import Lexer
from parser import Parser
from interpreteur import Interpreteur

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/documentation-technique')
def documentation_technique():
    return render_template('documentation_technique.html')

@app.route('/executer', methods=['POST'])
def executer_code():
    try:
        code = request.json['code']
        entrees = request.json.get('entrees', [])
        
        # Analyse lexicale
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Analyse syntaxique
        parser = Parser(tokens)
        arbre_ast = parser.parser()
        
        # Exécution
        interpreteur = Interpreteur()
        interpreteur.fournir_entrees(entrees)
        resultat = interpreteur.executer(arbre_ast)
        
        return jsonify({
            'success': True,
            'resultat': resultat,
            'tokens': tokens,
            'variables': interpreteur.variables,
            'entrees_requises': interpreteur.entrees_en_attente
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'erreur': str(e)
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', '5009'))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(debug=True, host=host, port=port)