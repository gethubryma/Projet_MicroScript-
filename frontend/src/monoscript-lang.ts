/* eslint-disable no-useless-escape */
import { StreamLanguage } from '@codemirror/language';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language'; // syntaxHighlighting est la clé
import { tags as t } from '@lezer/highlight';

// ... (Vos listes de mots-clés, opérateurs, etc. restent inchangées)
const motsCles = ["variable", "si", "sinon", "fin_si", "tant_que", "fin_tant_que", "afficher", "lire", "vrai", "faux", "fonction", "fin_fonction", "retour"];
const operateurs = ["+", "-", "*", "/", "%", "==", "=", "!=", "<", ">", "<=", ">=", "et", "ou", "non"];
const separateurs = /[()\[\]{},;:]/;


// 1. Définition de la coloration (inchangée)
const monoscriptHighlighting = HighlightStyle.define([
  { tag: t.keyword, color: "#d73a49", fontWeight: "bold" },
  { tag: t.variableName, color: "#fff" },
  { tag: t.operator, color: "#005cc5" },
  { tag: t.punctuation, color: "#6f42c1" },
  { tag: t.bool, color: "#22863a" },
  { tag: t.number, color: "#22863a" },
  { tag: t.string, color: "#032f62" },
  { tag: t.comment, color: "#6a737d", fontStyle: "italic" },
]);

// 2. On exporte l'extension de la logique du langage
export const monoscriptLanguage = StreamLanguage.define({
  token(stream) {
    // ... (la fonction token reste exactement la même)
    if (stream.match("//")) {
      stream.skipToEnd();
      return "comment";
    }
    if (stream.match(/"[^"]*"/)) {
      return "string";
    }
    if (stream.match(/^[0-9]+\b/)) {
      return "number";
    }
    if (stream.match(separateurs)) {
        return "punctuation";
    }
    if (stream.match(/^[+\-*\/%=<>&|!]+/)) {
        if (operateurs.includes(stream.current())) {
            return "operator";
        }
    }
    if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
      const mot = stream.current();
      if (motsCles.includes(mot)) {
        if (mot === "vrai" || mot === "faux") return "bool";
        return "keyword";
      } else {
        return "variableName";
      }
    }
    stream.next();
    return null;
  },
  languageData: {
    commentTokens: {line: "//"}
  }
});

// 3. On exporte l'extension pour le thème de coloration en l'enveloppant
export const monoscriptTheme = syntaxHighlighting(monoscriptHighlighting);