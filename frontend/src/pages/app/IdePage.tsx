import { useState } from "react";

import Fond from "../../assets/imageFond.jpg";
import Header from "../../components/Header";
import Editor from "../../components/Editor";
import Terminal from "../../components/Terminal";

// import axios  from 'axios'

function IdePage() {
  const [code, setCode] = useState(
    '// Écrivez votre code ici !\nvariable message = "Bonjour le monde !" \nafficher message'
  );
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [, setStatus] = useState(0);

  // États pour la fenêtre de l'Éditeur
  const [isEditorVisible, setIsEditorVisible] = useState(true);
  const [isEditorMinimized, setIsEditorMinimized] = useState(false);
  const [isEditorMaximized, setIsEditorMaximized] = useState(false);

  // NOUVEAU : États pour la fenêtre du Terminal
  const [isTerminalVisible, setIsTerminalVisible] = useState(true);
  const [isTerminalMinimized, setIsTerminalMinimized] = useState(false);
  const [isTerminalMaximized, setIsTerminalMaximized] = useState(false);

  //   const handleRun = async () => {
  //     setLoading(true);
  //     setOutput('Exécution en cours...');

  //     try {
  //       // 1. Définir l'URL de votre backend
  //       const backendUrl = 'http://195.15.242.96:2806/executer'; // Assurez-vous que le port est correct

  //       // 2. Envoyer la requête POST avec les données au format JSON
  //       const response = await fetch(backendUrl, {
  //         method: 'POST',
  //         headers: {
  //           'Content-Type': 'application/json',
  //         },
  //         // 3. Convertir l'objet JavaScript en chaîne JSON
  //         body: JSON.stringify({ code: code }),
  //       });

  //       // 4. Analyser la réponse JSON du backend
  //       const data = await response.json();
  // console.log(data)
  //       // 5. Mettre à jour le terminal avec le résultat
  //       if (data.success) {
  //         setOutput(`Exécution terminée.\nRésultat : ${data.resultat || 'Aucun'}\n\nVariables : ${JSON.stringify(data.variables)}`);
  //       } else {
  //         setOutput(`Erreur : ${data.erreur}`);
  //       }

  //     } catch (error) {
  //       // Gérer les erreurs de connexion au serveur
  //       setOutput(`Erreur de connexion au serveur : ${error}`);
  //     } finally {
  //       // 6. Arrêter l'indicateur de chargement
  //       setLoading(false);
  //     }
  //   };

  const handleRun = async () => {
    setLoading(true);
    setStatus(1);
    setOutput("Lancement de l'exécution...");

    try {
      const backendUrl = "http://195.15.242.96:2801/executer";
      const collectedInputs: string[] = []; // Tableau pour stocker toutes les entrées

      // --- PREMIER APPEL ---
      // On envoie le code avec un tableau d'entrées vide pour démarrer
      let response = await fetch(backendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code, entrees: [] }),
      });
      let data = await response.json();

      //   console.log(data);

      // Affiche les premiers résultats (qui peuvent inclure la première demande d'input)
      setOutput(
        Array.isArray(data.resultat)
          ? data.resultat.join("\n")
          : String(data.resultat)
      );

      // --- BOUCLE DE DIALOGUE ---
      // Tant que le backend nous demande des entrées...
      while (
        data.success &&
        data.entrees_requises &&
        data.entrees_requises.length > 0
      ) {
        // On prend la dernière demande d'input non satisfaite
        const promptMessage = data.entrees_requises[collectedInputs.length];
        if (!promptMessage) break; // Sécurité si le backend renvoie une incohérence

        const userInput = prompt(promptMessage);

        if (userInput !== null) {
          // On ajoute la nouvelle entrée à notre liste
          collectedInputs.push(userInput);

          // On met à jour le terminal pour montrer l'entrée de l'utilisateur
          setOutput((prev) => prev + `\n> ${userInput}`);

          // --- APPELS SUIVANTS ---
          // On refait un appel avec toutes les entrées collectées
          response = await fetch(backendUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: code, entrees: collectedInputs }),
          });
          data = await response.json();

          // On met à jour l'affichage avec la nouvelle réponse
          setOutput(
            Array.isArray(data.resultat)
              ? data.resultat.join("\n")
              : String(data.resultat)
          );
        } else {
          throw new Error("Exécution annulée par l'utilisateur.");
        }
      }

      // --- AFFICHAGE FINAL ---
      // Une fois la boucle terminée, on s'assure que tout est bien affiché
      if (data.success) {
        setStatus(1);
      } else {
        setOutput(`Erreur : ${data.erreur}`);
        setStatus(0);
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Erreur inconnue";
      setOutput(`Erreur de connexion ou d'exécution : ${errorMessage}`);
      setStatus(0);
    } finally {
      setLoading(false);
    }
  };
  return (
    // Conteneur principal qui prend tout l'écran
    <div className="flex justify-center items-center min-h-screen  bg-gradient-to-br from-[#2c3e50] to-[#000000] p-4 relative">
      <img
        src={Fond}
        alt="image de fond"
        className="absolute inset-0 h-full w-full bg-cover"
      />
      {/* Conteneur de l'IDE avec fond semi-transparent et effet de flou */}
      <div className="w-11/12 max-w-7xl bg-black/40 rounded-2xl shadow-2xl backdrop-blur-md p-6">
        <Header
          onRun={handleRun}
          load={loading}
          setCode={setCode}
          isEditorVisible={isEditorVisible}
          setIsEditorVisible={setIsEditorVisible}
          isTerminalVisible={isTerminalVisible}
          setIsTerminalVisible={setIsTerminalVisible}
        />

        <div className="flex flex-col md:flex-row gap-0 mt-5">
          {isEditorVisible && (
            <Editor
              isVisible={isEditorVisible}
              code={code}
              setCode={setCode}
              isMinimized={isEditorMinimized}
              isMaximized={isEditorMaximized}
              onToggleMinimize={() => setIsEditorMinimized(!isEditorMinimized)}
              onToggleMaximize={() => setIsEditorMaximized(!isEditorMaximized)}
              onClose={() => setIsEditorVisible(false)}
            />
          )}

          {/* Le terminal est maintenant conditionnel et reçoit ses propres états et fonctions */}
          {isTerminalVisible && (
            <Terminal
              output={output}
              isVisible={isEditorVisible}
              isMinimized={isTerminalMinimized}
              isMaximized={isTerminalMaximized}
              onToggleMinimize={() =>
                setIsTerminalMinimized(!isTerminalMinimized)
              }
              onToggleMaximize={() =>
                setIsTerminalMaximized(!isTerminalMaximized)
              }
              onClose={() => setIsTerminalVisible(false)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default IdePage;
