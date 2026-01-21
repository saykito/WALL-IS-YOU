Nasser-Edine CHEIKH-BENCHEIKH                                                BUT INFO1
Yassin BOUKRAA
WALL IS YOU










1 - L’organisation du programme        2
1.1 - Présentation de WALL IS YOU        2
1.2 - L’arborescence        2
1.3 - Fonctionnement général        3
2 - Choix techniques        3
2.1 - Séparation moteur/graphique        3
2.2 - Utilisation de FLTK pour l’affichage        3
2.3 - Choix du format des images        4
2.4 - Architecture interne du donjon        4
2.5 - Gestion du menu principal        4
3 - Problèmes rencontrées        5
3.1 Gestion des images avec FLTK (erreurs “pyimage1 doesn’t exist)        5
3.2 Implémentation des règles        5
3.3 Problèmes de rafraîchissement de l’écran        5
3.4 Taille des images        6
4 - Explication fonction afficher donjon fenêtre
2 ème rendu         6
1 - Correction des bug et conseil        6
2 - Nouvelles fonctions de la tâche 3 et variante        7
2.1 - Sauvegarder        7
2.2 - Trésors        7
2.3 - Générations de donjon grâce au caractères.


3 ème rendu le 09/01/2026 
        7
1 - Tache 4        7
2.1 Editeur de donjon        8
2.2 Niveaux aléatoire        9






















Je tient a préciser tout d’abord pour lancer le jeux il faut se placer dans WALL IS YOU\src> et lancer le main.py
1 - L’organisation du programme 


1.1 - Présentation de WALL IS YOU


Wall is you est un petit jeu de type donjon, dans lequel un aventurier doit parcourir un labyrinthe, combattre des dragons et atteindre la victoire. Nous avons essayé d'organiser le programme de manière à séparer la logique du jeu, l'affichage graphique et le programme principal.
1.2 - L’arborescence


Tout d’abord nous avons commencé par faire l’arborescence du jeu.




Main.py : qui est le fichier principal, il gère le lancement du menu, le choix du mode de jeu, la réinitialisation avec la touche R


Graphique.py : C’est le fichier qui est le plus important au niveau de l’affichage, il affiche le menu, dessine le dragon, dessine les salles…


Moteur.py : Contient la logique du jeu avec les règles internes comme la rotation des salles, le test de connexion entre salles, combats entre aventuriers et dragons.


Fltk.py : Une librairie graphique fournie par l'enseignant qui permet de crée des fenêtres, afficher les images, du texte…


Image du jeu : sont dans le fichier source/ le programme charge automatiquement les images via image(...)


1.3 - Fonctionnement général


Le joueur commence par lancer le main.py, le menu s’affiche et le joueur choisit un mode facile (donjon 3x3) ou mode dur (donjon 7x7). 














Le jeu démarre : 


clic gauche → tourner la salle

clic droit → tracer un chemin rouge

espace → suivre ce chemin

esc → retour au menu


r → revenir dès le début


2 - Choix techniques
2.1 - Séparation moteur/graphique


Le projet est organisé en plusieurs fichiers pour séparer les responsabilités : 


Pour le moteur.py il contient toute la logique du jeu comme les connexions entre les salles,rotation… Cela rend la logique testable, claire et indépendante de l’affichage.
Par la suite pour le graphique.py il contient uniquement l’affichage. Enfin nous avons le main.py qui lance le menu puis le jeu selon le mode choisi


2.2 - Utilisation de FLTK pour l’affichage


Le fltk qui a était fourni par l’enseignant. Nous l’avons utilisé pour créer une fenêtre, afficher du texte, afficher des images, détecter les clics et rafraîchir l’écran.


2.3 - Choix du format des images 


Les images sont en PNG car elles gèrent la transparence ce qui rend plus ergonomique notre jeu. De plus, elles sont compatibles avec FLTK et gardent une belle qualité même redimensionnées.


2.4 - Architecture interne du donjon




Le donjon est représenté comme une liste de liste, chaque salle étant un tuple : (haut, droite, bas, gauche).
Chaque valeur booléenne indique si un passage existe ( True = porte ouverte, False = porte fermée).
Ce choix a plusieurs avantages: une structure légère, facile à manipuler, parfaite pour représenter un labyrinthe.


2.5 - Gestion du menu principal


Le menu utilise une image menu.png pour un rendu professionnel et pour une bonne immersion.
Le Menu comporte 2 choix: un Mode Facile et un Mode Durt.
Ce choix permet d’avoir un menu visuel, et de laisser au joueur le choix.


Le Mode Facile est un donjon 3x3 qui comporte 1 dragon de niveau 1(cf.Illustration1) et le Mode Durt est un donjon 7x7 comportant 3 dragons de niveaux 1,2,3(cf.illustration2)  


              Illustration 1                                         Illustration 2 
  
  





3 - Problèmes rencontrées 
3.1 Gestion des images avec FLTK (erreurs “pyimage1 doesn’t exist)


Le plus gros problème rencontré concerne le système d’images de FLTK. FLTK perd parfois la réference interne, alors les images disparaissent après un rafraîchissement de la fenêtre et le jeu plantait avec TclError: image "pyimage1" doesn't exist.
Ce qui fait que la fonctionnalité avec ESC fonctionne 1 fois sur 2.


La solution qui peut être adoptée est de centraliser les appels image() sans utiliser de cache, et éviter toute destruction de l’image.


3.2 Implémentation des règles


Plusieurs soucis sont apparus lors de l’implémentation des règles, je voulais créer un système qui fait apparaître dans un rectangle les règles du jeux, puis une fois qu’on re appuis cela nous redirige vers le menu une fois qu’on a lus les règles l’utilisateur choisi un mode et joue. Cependant dès que j’ai implémenté ce système tout le système de jeux ses déréglées, j’ai donc préféré remettre le système comme avant.  


3.3 Problèmes de rafraîchissement de l’écran


Certaines actions (rotation de salles, déplacement de l’aventurier,combat) n’actualisaient pas correctement à l’écran, j’ai donc créé une fonction qui dessine tout complètement ce qui m'a permis de corriger cela.


3.4 Taille des images


Certaines images dépassent des cases, cacher les tuiles et par conséquent la fenêtre devenait trop petite. J’ai donc du adaptées toutes mes images en 100x100 spécialement pour régler se problèmes.














4 - Explication fonction afficher donjon fenêtre 




La fonction afficher_donjon_fenetre constitue la boucle principale du jeu. Elle ouvre la fenêtre graphique, affiche le donjon ainsi que tous les éléments du jeu (salles, aventurier, dragons et chemin d’intention), puis gère l’ensemble des interactions du joueur. Elle interprète les clics de souris (rotation des salles, dessin d’un chemin rouge)). Après chaque action de l’aventurier, elle actualise l’état du jeu : vérification des portes, déplacements possibles, combat éventuel avec un dragon et mouvement aléatoire des dragons restants. La fonction détecte aussi les conditions de fin : victoire si tous les dragons sont vaincus, ou défaite si l’aventurier rencontre un ennemi plus fort. Dans chacun de ces cas, un écran final s’affiche avant de fermer la fenêtre. Ainsi, afficher_donjon_fenetre centralise toute la logique visuelle et interactive du jeu.


2 ème rendu le 19/12/2025


1 - Correction des bug et conseil 


Après consultation avec le professeur nous avons pu prendre quelques conseils comme le fait d’optimiser au niveau algorithmique certaines fonctions. De plus nous avons parfois au premier rendu un bug qui mettait pyimage3 en voulant retourner au menu avec la touche Esc. Nous avons cherchée comment ce bug se produisait, nous avons donc compris que le problème venait du fait que nous chargeons dans un premier temps une fenêtre en introduisant plusieurs image, puis en faisant la touche Esc nous supprimons la fenêtre qui contient toute les images et nous en chargeons une autre en lui faisant appel à des images qu’elle na pas. Nous avons donc fait en sorte qu' aucune fenêtre ne se ferme pour pouvoir éviter ce bug. 


2 - Nouvelles fonctions de la tâche 3 et variante
2.1 - Sauvegarder
Nous avons rajouter la fonctionnalité sauvegarder à notre jeux, nous nous sommes aidé du cours sur les ouvertures de fichier qui nous a vraiment aider et en réfléchissant à un système qui permet cela. Nous n'avons pas forcément rencontrées de problèmes à ce niveaux la.


2.2 - Trésors
Alors pour la fonctionnalitée trésors cela a était plus compliquée dans un premier temps par la compréhension du texte et puis par quelque bug que nous avons rencontrées comme le fait que les trésors se mettait à l’infini en ne respectant pas le nombre de trésors indiquées ou encore le fait que l’aventurier en se mettant dessus ne le prenait pas.


2.3 - Générations de donjon grâce au caractères.  
Cette tâche nous à poser plusieurs problèmes comme le fait que le jeux ne reconnaissait pas les caractères que la tâche 3 nous impose, nous avons se message d’erreur qui s’affichait UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 5: character maps to <undefined>, nous avons donc cherché a comprendre d’ou venait le problème après une recherche, nous avons donc compris que nous devons ajouter un encodage à la fonction pour qu’elle comprend enfin à quoi correspond ses caractères. Puis nous avons fait la fonction qui gère les positionnements des personnages qui a était assez facile après avoir fait avec les caractères.






3 ème rendu le 09/01/2026


1 - Tache 4 
La tâche 4 consiste à implémenter un calcul automatique de l'intention de l'aventurier. Avant cette tâche, le joueur devait manuellement tracer le chemin que l'aventurier devait suivre en cliquant successivement sur les cases. Cette approche était fastidieuse et peu ergonomique, obligeant le joueur à recliquer à chaque modification du donjon. La tâche 4 améliore considérablement l'expérience utilisateur en calculant automatiquement le meilleur chemin que l'aventurier devrait suivre, libérant ainsi le joueur pour qu'il se concentre uniquement sur la rotation des salles et le placement stratégique des trésors.


L'implémentation utilise l'algorithme BFS (Breadth-First Search) qui explore le donjon niveau par niveau pour trouver le chemin le plus court. Le BFS maintient une file d'attente de cases à explorer, partant de la position de l'aventurier. Pour chaque case retirée de la file, il examine ses quatre voisins et ajoute ceux qui sont accessibles via des portes ouvertes et non encore visités. Un ensemble de cases visitées évite les boucles infinies.
La fonction calculer_intention() applique un système de priorités crucial pour le gameplay. Si un trésor est placé, il devient la cible prioritaire absolue, quelle que soit la présence de dragons. Sans trésor, la fonction cible le dragon accessible de plus haut niveau. Cette logique force le joueur à placer stratégiquement des trésors pour diriger l'aventurier vers des dragons faibles d'abord, créant ainsi un puzzle tactique où il faut bloquer l'accès aux dragons trop forts.
L'intention est recalculée automatiquement après chaque rotation de salle, placement ou retrait de trésor, déplacement de l'aventurier et des dragons, reset ou chargement de partie. La ligne rouge affichée à l'écran se met à jour instantanément, offrant une rétroaction visuelle immédiate qui guide le joueur.
2.1 Editeur de donjon


L’éditeur de donjon est une fonctionnalité essentielle du programme, car il permet au joueur de créer ses propres niveaux de manière interactive. Il offre une interface graphique simple et intuitive dans laquelle l’utilisateur peut définir la taille du donjon, modifier les salles, placer l’aventurier, ajouter ou supprimer des dragons, ajuster leur niveau ainsi que définir le nombre de trésors.
Tout d’abord, le donjon est représenté sous forme d’une grille de taille n×mn \times mn×m, stockée dans une structure de type liste de listes. Ce choix permet un accès direct et rapide à chaque salle, ce qui est essentiel lors des modifications effectuées par l’utilisateur.
Ensuite, l’éditeur repose sur une boucle principale qui gère les événements clavier et souris. Ce fonctionnement permet de traiter les actions du joueur en temps réel, comme la rotation des salles, le changement de mode (édition de salle, placement de l’aventurier, placement de dragons) ou la modification du niveau des ennemis.
Le choix de redessiner entièrement le donjon à chaque itération garantit une cohérence visuelle parfaite entre l’état interne du niveau et son affichage à l’écran. Bien que cette méthode soit plus coûteuse en temps de calcul, elle simplifie considérablement la logique graphique et évite les erreurs d’affichage.
Enfin, la sauvegarde des niveaux est réalisée à partir d’un parcours complet du donjon, ce qui permet de stocker toutes les informations nécessaires pour recharger fidèlement un niveau ultérieurement.


2.2 Niveaux aléatoire


La génération de niveau aléatoire permet de proposer au joueur une expérience renouvelée à chaque partie. Contrairement à l’éditeur de donjon, qui repose sur une création manuelle, cette fonctionnalité automatise la conception du niveau en produisant une configuration différente à chaque lancement.
Le donjon est représenté sous forme d’une grille de taille n×mn \times mn×m, ce qui facilite la génération systématique de chaque salle. Chaque case est initialisée une seule fois, puis configurée aléatoirement selon des règles précises (orientation, type de salle, ouvertures).
L’utilisation de fonctions aléatoires permet de déterminer la position de l’aventurier, des dragons et des trésors. Cependant, ces placements sont contrôlés afin d’éviter les incohérences, comme le chevauchement de plusieurs entités sur une même case.
Les dragons sont stockés dans une liste, ce qui permet de les parcourir facilement pour les afficher, les déplacer ou gérer les combats. Cette structure est simple, efficace et adaptée à un nombre modéré d’ennemis.


/