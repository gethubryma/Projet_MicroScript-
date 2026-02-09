// src/examples.ts

export type Example = {
  name: string;
  code: string;
};

export const examples: Example[] = [
  {
    name: "Variables et Types",
    code: `// Déclaration avec valeur initiale
variable nom = "Alice"
variable age = 25
variable actif = vrai

# Affectation à une variable existante
age = 26
nom = "Bob"

afficher "Bonjour " + nom`
  },
  {
    name: "Opérateurs Arithmétiques",
    code: `variable a = 10
variable b = 3
afficher "10 + 3 = " + (a + b)
afficher "10 - 3 = " + (a - b)
afficher "10 * 3 = " + (a * b)
afficher "10 / 3 = " + (a / b)`
  },
  {
    name: "Structures de Contrôle (Si/Sinon)",
    code: `variable note = 15

si note >= 16
    afficher "Très bien"
sinon si note >= 14
    afficher "Bien"
sinon
    afficher "Assez bien"
fin_si`
  },
  {
    name: "Boucle Tant Que",
    code: `variable i = 0
tant_que i < 5
    afficher "Itération " + i
    i = i + 1
fin_tant_que`
  },
  {
    name: "Fonctions Utilisateur",
    code: `# Définition
fonction calculer_carre(nombre)
    retour nombre * nombre
fin_fonction

# Appel
variable resultat = calculer_carre(5)
afficher "Le carré de 5 est " + resultat`
  },
  {
    name: "Collections (Tableaux)",
    code: `variable nombres = [1, 2, 3, 4, 5]
afficher "Premier élément : " + nombres[0]
nombres[2] = 99
afficher "Tableau modifié : " + nombres`
  },
  {
    name: "Entrées Utilisateur",
    code: `variable nom = lire("Votre nom: ")
variable age = input("Votre âge: ")
afficher "Bonjour " + nom + ", vous avez " + age + " ans"`
  },
  {
    name: "Fonctions Mathématiques",
    code: `afficher "Racine de 16 : " + sqrt(16)
afficher "Arrondi de 3.7 : " + round(3.7)
afficher "Valeur absolue de -5 : " + abs(-5)`
  },
  {
    name: "Manipulation de Chaînes",
    code: `variable texte = "Bonjour le monde"
afficher maj(texte)
afficher min(texte)
afficher "Longueur du texte : " + len(texte)`
  },
  {
    name: "Jeu de Devinette",
    code: `variable nombre_secret = round(random() * 100)
variable tentative = 0
variable trouve = faux

afficher "J'ai choisi un nombre entre 0 et 100. À vous de deviner !"

tant_que non trouve
    variable proposition = lire("Votre proposition : ")
    tentative = tentative + 1
    
    si proposition == nombre_secret
        afficher "Bravo ! Trouvé en " + tentative + " tentatives"
        trouve = vrai
    sinon si proposition < nombre_secret
        afficher "C'est plus grand !"
    sinon
        afficher "C'est plus petit !"
    fin_si
fin_tant_que`
  },
];