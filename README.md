# WALL IS YOU

Projet de programmation Python, BUT Informatique 1re année, IUT de Marne-la-Vallée (2025 - 2026).
Réalisé en binôme par Yasin Boukraa et Nasser-Edine Cheikh-Bencheikh.

Jeu de donjon : le joueur fait pivoter les salles d'un labyrinthe pour ouvrir un chemin à l'aventurier, qui doit affronter les dragons et atteindre la victoire.

## Commandes

| Touche | Action |
|---|---|
| Clic gauche | Tourner une salle |
| Clic droit | Tracer le chemin de l'aventurier |
| Espace | Suivre le chemin tracé |
| R | Recommencer le niveau |
| Échap | Retour au menu |

Deux modes : facile (donjon 3x3) et difficile (donjon 7x7).

## Fonctionnalités

- Sauvegarde de partie, trésors
- Génération de donjons à partir de fichiers texte
- Éditeur de donjon et niveaux aléatoires

## Architecture

```
src/main.py        lancement, menu, choix du mode
src/moteur.py      logique du jeu : rotation des salles, connexions, combats
src/graphique.py   affichage : menu, salles, dragons
src/fltk.py        bibliothèque graphique fournie par l'enseignant
src/*.txt          donjons prédéfinis
```

Séparer le moteur de l'affichage rend la logique testable indépendamment de l'interface.

## Lancer

```
cd src
python main.py
```

Python 3, Tkinter requis (inclus avec la plupart des installations).

Le rapport détaillé des trois rendus est dans `Rapport synthétique Wall Is You (1).pdf`.
