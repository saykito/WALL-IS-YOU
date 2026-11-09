# WALL IS YOU

Projet de programmation en Python du BUT Informatique 1re année, IUT de Marne-la-Vallée, Université Gustave Eiffel (2025 - 2026).
Réalisé par Nasser-Edine Cheikh-Bencheikh et Yasin Boukraa.

Jeu de donjon en vue de dessus : le joueur ne contrôle pas l'aventurier, il fait pivoter les salles du donjon pour lui ouvrir un chemin, afin qu'il affronte les dragons du plus faible au plus fort et gagne des niveaux.

## Fonctionnalités

- Deux donjons prédéfinis : mode facile (3 x 3, 1 dragon) et mode dur (7 x 7, 3 dragons de niveaux 1 à 3)
- Calcul automatique de l'intention de l'aventurier (parcours en largeur, BFS), affichée en rouge et mise à jour après chaque action
- Trésors à placer pour attirer l'aventurier vers une cible précise
- Sauvegarde et chargement de partie
- Éditeur de donjon (taille, salles, aventurier, dragons, trésors)
- Génération de niveaux aléatoires à partir d'un labyrinthe parfait
- Indice pour aider le joueur
- Lecture des donjons depuis des fichiers texte en caractères de dessin de boîte (`╔═╦═╗`...)

## Commandes

| Action | Effet |
| --- | --- |
| Clic gauche sur une salle | Tourner la salle |
| Clic droit sur une salle | Placer ou retirer un trésor |
| Espace | Faire avancer l'aventurier, puis les dragons |
| I | Afficher ou masquer l'indice |
| S / L | Sauvegarder / charger la partie |
| R | Recommencer le niveau |
| Échap | Retour au menu |

## Lancer le jeu

Python 3 avec tkinter (inclus dans l'installation standard de Python sur Windows). Pillow est optionnel.

```
cd src
python main.py
```

Le jeu doit être lancé depuis le dossier `src`, car les images et les fichiers de donjon y sont chargés par chemin relatif.

## Structure

```
src/
├── main.py              Menu et choix du mode
├── moteur.py            Logique du jeu (rotations, connexions, combats, intention, sauvegarde, génération)
├── graphique.py         Affichage et gestion des événements
├── fltk.py              Bibliothèque graphique fournie par l'enseignant (basée sur tkinter)
├── sauvegarde.py
├── donjon_facile.txt    Donjon du mode facile
├── donjon_durt.txt      Donjon du mode dur
└── *.png                Tuiles, personnages et menus
```

Les choix techniques et les problèmes rencontrés sont détaillés dans `Rapport synthétique Wall Is You (1).pdf` et `README 3nd rendu.pdf`.
