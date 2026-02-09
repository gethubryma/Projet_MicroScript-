// src/documentationContent.ts
export const documentationSections = [
  {
    id: "introduction",
    title: "Introduction",
    content: `
## 🎯 Introduction à MONOSCRIPT

MONOSCRIPT (Mon Langage Français) est un langage de programmation éducatif conçu pour faciliter l'apprentissage de la programmation en français. Il offre une syntaxe claire et intuitive, parfaite pour les débutants.

---

### 💻 Utilisation de l'IDE web

L'interface web propose:
-   **Éditeur de code** : Zone de texte pour écrire vos programmes.
-   **Bouton "Exécuter"** : Lance l'interprétation du code.
-   **Zone de résultats** : Affiche la sortie et l'état des variables.
-   **Exemples prédéfinis** : Boutons pour charger des exemples.

### Étapes d'utilisation
1.  Écrivez votre programme dans l'éditeur.
2.  Cliquez sur "Exécuter le Code".
3.  Si votre programme contient des entrées utilisateur (\`lire()\` ou \`input()\`), une interface apparaîtra pour saisir les valeurs.
4.  Consultez les résultats et l'état des variables.

<div class="feature-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
    <div class="feature-card bg-[#21262d] p-6 rounded-lg border border-gray-700 shadow-md">
        <h4 class="text-xl font-bold text-white mb-2 flex items-center gap-2">🇫🇷 100% Français</h4>
        <p class="text-gray-400">Syntaxe entièrement en français pour une meilleure compréhension</p>
    </div>
    <div class="feature-card bg-[#21262d] p-6 rounded-lg border border-gray-700 shadow-md">
        <h4 class="text-xl font-bold text-white mb-2 flex items-center gap-2">💡 Simple et Intuitif</h4>
        <p class="text-gray-400">Conçu pour être facile à apprendre et à utiliser</p>
    </div>
    <div class="feature-card bg-[#21262d] p-6 rounded-lg border border-gray-700 shadow-md">
        <h4 class="text-xl font-bold text-white mb-2 flex items-center gap-2">🚀 Interactif</h4>
        <p class="text-gray-400">IDE web intégré avec exécution en temps réel</p>
    </div>
    <div class="feature-card bg-[#21262d] p-6 rounded-lg border border-gray-700 shadow-md">
        <h4 class="text-xl font-bold text-white mb-2 flex items-center gap-2">🔧 Complet</h4>
        <p class="text-gray-400">Fonctions mathématiques, manipulation de chaînes, et plus</p>
    </div>
</div>
        `,
  },
  {
    id: "premiers-pas",
    title: "Premiers Pas",
    content: `
## 🚀 Premiers Pas

### Votre Premier Programme
Commençons par le traditionnel "Bonjour le monde" :

\`\`\`
afficher "Bonjour le monde !"
\`\`\`

<div class="info-box bg-green-800/20 text-green-300 p-4 rounded-md border border-green-700 mt-4">
    <div class="info-box-title font-bold flex items-center gap-2">✅ C'est fait !</div>
    <p>Vous venez d'écrire votre premier programme en MOL. Copiez ce code dans l'IDE et cliquez sur "Exécuter" pour le tester.</p>
</div>
        `,
  },
  {
    id: "variables",
    title: "Variables & Types",
    content: `
## 📝 Variables et Types de Données

### Déclaration de Variables
En MOL, les variables se déclarent avec le mot-clé \`variable\` :

\`\`\`
// Déclaration avec valeur initiale
variable nom = "Alice"
variable age = 25
variable actif = vrai

// Modification d'une variable
age = 26
nom = "Bob"
\`\`\`

### Types de Données
| Type          | Description                   | Exemple                     |
| :------------ | :---------------------------- | :-------------------------- |
| **Nombres** | Entiers et décimaux           | \`42\`, \`3.14\`, \`-10\`   |
| **Chaînes** | Texte entre guillemets        | \`"Bonjour"\`, \`"Hello World"\` |
| **Booléens** | Vrai ou faux                  | \`vrai\`, \`faux\`            |
| **Tableaux** | Listes d'éléments             | \`[1, 2, 3]\`, \`["a", "b"]\` |
| **Dictionnaires** | Paires clé-valeur           | \`{"nom": "Alice", "age": 25}\` |
        `,
  },
  {
    id: "operateurs",
    title: "Opérateurs",
    content: `
## 🔢 Opérateurs

### Opérateurs Arithmétiques
\`\`\`
variable a = 10
variable b = 3

afficher a + b   // 13 (addition)
afficher a - b   // 7 (soustraction)
afficher a * b   // 30 (multiplication)
afficher a / b   // 3.333... (division)
\`\`\`

### Opérateurs de Comparaison
\`\`\`
variable x = 10
variable y = 5

afficher x > y    // vrai (plus grand que)
afficher x < y    // faux (plus petit que)
afficher x >= y   // vrai (plus grand ou égal)
afficher x <= y   // faux (plus petit ou égal)
afficher x == y   // faux (égal à)
afficher x != y   // vrai (différent de)
\`\`\`

### Opérateurs Logiques
\`\`\`
variable a = vrai
variable b = faux

afficher a et b   // faux (ET logique)
afficher a ou b   // vrai (OU logique)
afficher non a    // faux (NON logique)
\`\`\`
        `,
  },
  {
    id: "conditions",
    title: "Conditions",
    content: `
## 🔀 Structures Conditionnelles

### Condition avec Alternative
\`\`\`
variable note = 15

si note >= 10
    afficher "Admis !"
sinon
    afficher "Recalé..."
fin_si
\`\`\`

<div class="info-box bg-sky-800/20 text-sky-300 p-4 rounded-md border border-sky-700 mt-4">
    <div class="info-box-title font-bold flex items-center gap-2">💡 Astuce</div>
    <p>N'oubliez pas de fermer chaque condition avec \`fin_si\` !</p>
</div>
        `,
  },
  {
    id: "boucles",
    title: "Boucles",
    content: `
## 🔁 Boucles

### Boucle Tant Que
La boucle \`tant_que\` répète un bloc de code tant qu'une condition est vraie :

\`\`\`
variable i = 0

tant_que i < 5
    afficher "Itération " + i
    i = i + 1
fin_tant_que
\`\`\`

<div class="info-box bg-yellow-800/20 text-yellow-300 p-4 rounded-md border border-yellow-700 mt-4">
    <div class="info-box-title font-bold flex items-center gap-2">⚠ Attention</div>
    <p>Assurez-vous que la condition de la boucle finira par devenir fausse, sinon vous créerez une boucle infinie !</p>
</div>
        `,
  },
  {
    id: "fonctions",
    title: "Fonctions",
    content: `
## 🎯 Fonctions

### Définir une Fonction
\`\`\`
fonction saluer(nom)
    afficher "Bonjour " + nom + " !"
fin_fonction

// Appel de la fonction
saluer("Alice")
\`\`\`

### Fonction avec Retour
\`\`\`
fonction carre(nombre)
    retour nombre * nombre
fin_fonction

variable resultat = carre(5)
afficher "Le carré de 5 est " + resultat
\`\`\`
        `,
  },
  {
    id: "collections",
    title: "Collections",
    content: `
## 📋 Collections

### Tableaux
\`\`\`
variable nombres = [1, 2, 3]
afficher nombres[0]  // 1
nombres[1] = 99
afficher len(nombres) // 3
\`\`\`

### Dictionnaires
\`\`\`
variable personne = {"nom": "Alice", "age": 25}
afficher personne["nom"] // Alice
personne["pays"] = "France"
\`\`\`
        `,
  },
  {
    id: "entrees",
    title: "Entrées Utilisateur",
    content: `
## ⌨ Entrées Utilisateur

### Fonctions lire() et input()
\`\`\`
variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom
\`\`\`

<div class="info-box bg-green-800/20 text-green-300 p-4 rounded-md border border-green-700 mt-4">
    <div class="info-box-title font-bold flex items-center gap-2">✨ Fonctionnalité Avancée</div>
    <p>Dans l'IDE web, une interface interactive apparaît automatiquement pour saisir les valeurs lorsque votre programme contient des fonctions \`lire()\` ou \`input()\`. </p>
</div>
        `,
  },
  {
    id: "fonctions-builtin",
    title: "Fonctions Intégrées",
    content: `
## 🔧 Fonctions Intégrées

### Fonctions Mathématiques
| Fonction                 | Description           |
| :----------------------- | :-------------------- |
| \`sqrt(x)\`                | Racine carrée         |
| \`abs(x)\`                 | Valeur absolue        |
| \`round(x)\`               | Arrondi               |
| \`sin(x)\`, \`cos(x)\`, \`tan(x)\` | Trigonométrie         |

### Fonctions de Chaînes et Utilitaires
| Fonction          | Description                         |
| :---------------- | :---------------------------------- |
| \`maj(texte)\`      | Convertir en majuscules             |
| \`min(texte)\`      | Convertir en minuscules             |
| \`len(x)\`          | Longueur (chaîne ou tableau)        |
| \`random()\`, \`randomInt(min, max)\` | Nombre aléatoire                |
| \`date()\`, \`heure()\` | Date et heure actuelles             |
        `,
  },
  {
    id: "exemples",
    title: "Exemples Pratiques",
    content: `
## 📖 Exemples Pratiques

### Calcul de Moyenne
\`\`\`
variable notes = [15, 12, 18, 14, 16]
variable somme = 0
variable i = 0

tant_que i < len(notes)
    somme = somme + notes[i]
    i = i + 1
fin_tant_que

variable moyenne = somme / len(notes)
afficher "Moyenne des notes: " + moyenne
\`\`\`

### Suite de Fibonacci
\`\`\`
variable a = 0
variable b = 1
variable i = 0

tant_que i < 10
    afficher a
    variable temp = a + b
    a = b
    b = temp
    i = i + 1
fin_tant_que
\`\`\`
        `,
  },
];
