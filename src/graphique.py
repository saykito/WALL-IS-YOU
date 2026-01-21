from fltk import (
    cree_fenetre,
    ferme_fenetre,
    efface_tout,
    mise_a_jour,
    rectangle,
    texte,
    ligne,
    image,
    cercle,
    redimensionne_fenetre,
    donne_ev,
    type_ev,
    abscisse,
    ordonnee,
    touche,
)

from moteur import (
    rotation_horaire,
    calculer_intention,
    calculer_indice,
    deplacer_aventurier_si_possible,
    deplacer_dragons,
    gerer_combat,
    nom_image_salle,
    sauvegarder_partie,
    charger_partie,
    salle_suivante,
    sauvegarder_niveau,
    generer_niveau_aleatoire,
)

from random import randint, choice, shuffle
from time import strftime, localtime
from os import path

# constantes
TAILLE = 80
TAILLE_PERSO = 40


def calculer_decalages(donjon):
    """Calcule les décalages pour centrer le donjon"""
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    largeur_donjon = nb_colonnes * TAILLE
    hauteur_donjon = nb_lignes * TAILLE
    decalage_x = (1248 - largeur_donjon) // 2
    decalage_y = (832 - hauteur_donjon) // 2
    return decalage_x, decalage_y


def afficher_menu():
    """
    Menu principal avec structure hiérarchique :
    - JOUER (Mode Facile, Mode Difficile, Charger Partie)
    - OUTILS (Éditeur, Générateur)
    - QUITTER
    """

    LARGEUR = 1248
    HAUTEUR = 832

    redimensionne_fenetre(LARGEUR, HAUTEUR)

    # Vérifier si une sauvegarde existe
    if path.exists("sauvegarde.txt"):
        sauvegarde_existe = True

    else:
        sauvegarde_existe = False
        date_sauvegarde = ""

    phase = "principal"  # "principal", "jouer", "outils"
    fini_menu = False
    choix = "quit"

    # Coordonnées des boutons du menu principal
    x1, x2 = 499, 749
    y_jouer = (500, 570)
    y_outils = (600, 670)
    y_quitter = (700, 770)

    while not fini_menu:
        efface_tout()
        image(0, 0, "menu.png", ancrage="nw", largeur=LARGEUR, hauteur=HAUTEUR)

        if phase == "principal":
            # MENU PRINCIPAL

            # Bouton JOUER
            rectangle(
                x1,
                y_jouer[0],
                x2,
                y_jouer[1],
                remplissage="green",
                epaisseur=3,
                couleur="white",
            )
            texte(
                (x1 + x2) // 2,
                (y_jouer[0] + y_jouer[1]) // 2,
                "JOUER",
                ancrage="center",
                taille=28,
                couleur="white",
            )

            # Bouton OUTILS
            rectangle(
                x1,
                y_outils[0],
                x2,
                y_outils[1],
                remplissage="orange",
                epaisseur=3,
                couleur="white",
            )
            texte(
                (x1 + x2) // 2,
                (y_outils[0] + y_outils[1]) // 2,
                "OUTILS",
                ancrage="center",
                taille=28,
                couleur="white",
            )

            # Bouton QUITTER
            rectangle(
                x1,
                y_quitter[0],
                x2,
                y_quitter[1],
                remplissage="red",
                epaisseur=3,
                couleur="white",
            )
            texte(
                (x1 + x2) // 2,
                (y_quitter[0] + y_quitter[1]) // 2,
                "QUITTER",
                ancrage="center",
                taille=28,
                couleur="white",
            )

        elif phase == "jouer":
            # SOUS-MENU JOUER

            # Titre
            texte(
                LARGEUR // 2, 200, "JOUER", ancrage="center", taille=42, couleur="white"
            )

            # Bouton Mode Facile
            rectangle(
                x1, 300, x2, 370, remplissage="lightgreen", epaisseur=3, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                335,
                "Mode Facile",
                ancrage="center",
                taille=24,
                couleur="black",
            )

            # Bouton Mode Difficile
            rectangle(
                x1, 390, x2, 460, remplissage="orange", epaisseur=3, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                425,
                "Mode Difficile",
                ancrage="center",
                taille=24,
                couleur="black",
            )

            # Bouton Charger Partie
            if sauvegarde_existe:
                rectangle(
                    x1, 480, x2, 550, remplissage="cyan", epaisseur=3, couleur="white"
                )
                texte(
                    (x1 + x2) // 2,
                    505,
                    "Charger Partie",
                    ancrage="center",
                    taille=20,
                    couleur="black",
                )

            else:
                rectangle(
                    x1,
                    480,
                    x2,
                    550,
                    remplissage="gray",
                    epaisseur=3,
                    couleur="darkgray",
                )
                texte(
                    (x1 + x2) // 2,
                    515,
                    "Pas de sauvegarde",
                    ancrage="center",
                    taille=18,
                    couleur="darkgray",
                )

            # Bouton Retour
            rectangle(
                x1, 600, x2, 660, remplissage="gray", epaisseur=2, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                630,
                "RETOUR",
                ancrage="center",
                taille=20,
                couleur="white",
            )

        elif phase == "outils":
            # SOUS-MENU OUTILS

            # Titre
            texte(
                LARGEUR // 2,
                200,
                "OUTILS",
                ancrage="center",
                taille=42,
                couleur="white",
            )

            # Bouton Éditeur
            rectangle(
                x1, 320, x2, 400, remplissage="purple", epaisseur=3, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                360,
                "Éditeur de niveau",
                ancrage="center",
                taille=22,
                couleur="white",
            )

            # Bouton Générateur
            rectangle(
                x1, 420, x2, 500, remplissage="violet", epaisseur=3, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                460,
                "Générateur aléatoire",
                ancrage="center",
                taille=20,
                couleur="white",
            )

            # Bouton Retour
            rectangle(
                x1, 600, x2, 660, remplissage="gray", epaisseur=2, couleur="white"
            )
            texte(
                (x1 + x2) // 2,
                630,
                "RETOUR",
                ancrage="center",
                taille=20,
                couleur="white",
            )

        mise_a_jour()

        # Gestion des événements
        ev = donne_ev()
        if ev:
            t = type_ev(ev)

            if t == "Quitte":
                fini_menu = True
                choix = "quit"

            elif t == "ClicGauche":
                x = abscisse(ev)
                y = ordonnee(ev)

                if phase == "principal":
                    # Bouton JOUER
                    if x1 <= x <= x2 and y_jouer[0] <= y <= y_jouer[1]:
                        phase = "jouer"

                    # Bouton OUTILS
                    elif x1 <= x <= x2 and y_outils[0] <= y <= y_outils[1]:
                        phase = "outils"

                    # Bouton QUITTER
                    elif x1 <= x <= x2 and y_quitter[0] <= y <= y_quitter[1]:
                        fini_menu = True
                        choix = "quit"

                elif phase == "jouer":
                    # Mode Facile
                    if x1 <= x <= x2 and 300 <= y <= 370:
                        fini_menu = True
                        choix = "facile"

                    # Mode Difficile
                    elif x1 <= x <= x2 and 390 <= y <= 460:
                        fini_menu = True
                        choix = "durt"

                    # Charger Partie
                    elif x1 <= x <= x2 and 480 <= y <= 550 and sauvegarde_existe:
                        fini_menu = True
                        choix = "charger"

                    # Bouton Retour
                    elif x1 <= x <= x2 and 600 <= y <= 660:
                        phase = "principal"

                elif phase == "outils":
                    # Éditeur
                    if x1 <= x <= x2 and 320 <= y <= 400:
                        fini_menu = True
                        choix = "editeur"

                    # Générateur
                    elif x1 <= x <= x2 and 420 <= y <= 500:
                        fini_menu = True
                        choix = "generateur"

                    # Bouton Retour
                    elif x1 <= x <= x2 and 600 <= y <= 660:
                        phase = "principal"

            elif t == "Touche":
                key = touche(ev)
                # Esc pour revenir en arrière ou quitter
                if key in ("Escape", "esc", "ESC"):
                    if phase == "principal":
                        fini_menu = True
                        choix = "quit"
                    else:
                        phase = "principal"

        mise_a_jour()

    return choix


def dessiner_salle(i, j, salle, donjon):
    """
    Dessine la salle (i, j) en utilisant l'image correspondante.
    Les fichiers tile_*.png doivent être dans le même dossier que graphique.py.
    """
    DECALAGE_X, DECALAGE_Y = calculer_decalages(donjon)

    x = j * TAILLE + DECALAGE_X
    y = i * TAILLE + DECALAGE_Y

    # Si salle fermée (aucune porte), dessiner un rectangle gris
    if salle == (False, False, False, False):
        rectangle(
            x,
            y,
            x + TAILLE,
            y + TAILLE,
            remplissage="#404040",
            epaisseur=2,
            couleur="#606060",
        )
    else:
        nom = nom_image_salle(salle)
        image(x, y, nom, ancrage="nw")


def dessiner_aventurier(i, j, niveau, donjon):
    """
    Dessine un aventurier à la position spécifiée et affiche
    son niveau de puissance dans un petit rectangle.

    L'aventurier est centré dans la salle
    """
    DECALAGE_X, DECALAGE_Y = calculer_decalages(donjon)
    x = j * TAILLE + DECALAGE_X
    y = i * TAILLE + DECALAGE_Y

    dx = (TAILLE - TAILLE_PERSO) // 2  # TAILLE - TAILLE PERSO sert a calculer
    dy = (
        TAILLE - TAILLE_PERSO
    ) // 2  # l'espace vide qui doit etre reparti a droite et a gauche

    image(
        x + dx,
        y + dy,
        "aventurier.png",
        ancrage="nw",
        hauteur=TAILLE_PERSO,
        largeur=TAILLE_PERSO,
    )

    rect_w = 12
    rect_h = 16
    margin = 10

    rect_x1 = x + TAILLE - rect_w - margin
    rect_y1 = y + margin
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h

    rectangle(rect_x1, rect_y1, rect_x2, rect_y2, remplissage="white")

    texte(
        rect_x1 + rect_w // 2,
        rect_y1 + rect_h // 2,
        str(niveau),
        couleur="black",
        ancrage="center",
        taille=10,
    )


def dessiner_dragon(i, j, niveau, donjon):
    """
    Dessine un dragon à la position spécifiée et affiche
    son niveau de puissance dans un petit rectangle.

    L'image du dragon est choisie en fonction de son niveau ('dragon1.png',
    'dragon2.png', ou 'dragon3.png').
    """
    DECALAGE_X, DECALAGE_Y = calculer_decalages(donjon)
    x = j * TAILLE + DECALAGE_X
    y = i * TAILLE + DECALAGE_Y

    # Choix de l'image selon le niveau
    if niveau == 1:
        nom_img = "dragon1.png"
    elif niveau == 2:
        nom_img = "dragon2.png"
    elif niveau == 3:
        nom_img = "dragon3.png"
    else:
        nom_img = "dragon1.png"  # par défaut

    dx = (TAILLE - TAILLE_PERSO) // 2
    dy = (TAILLE - TAILLE_PERSO) // 2

    image(
        x + dx,
        y + dy,
        nom_img,
        ancrage="nw",
        hauteur=TAILLE_PERSO,
        largeur=TAILLE_PERSO,
    )

    # Petit rectangle avec le niveau
    rect_w = 12
    rect_h = 16
    margin = 10

    rect_x1 = x + TAILLE - rect_w - margin
    rect_y1 = y + margin
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h

    rectangle(rect_x1, rect_y1, rect_x2, rect_y2, remplissage="white")

    texte(
        rect_x1 + rect_w // 2,
        rect_y1 + rect_h // 2,
        str(niveau),
        couleur="black",
        ancrage="center",
        taille=10,
    )


def dessiner_ligne_intention(case1, case2, donjon):
    """
    Dessine un trait rouge entre deux cases (i, j), pour représenter un
    chemin d'intention entre le centre de deux cases adjacentes.
    Le segment est dessiné sous la forme d'un rectangle (horizontal ou vertical)
    pour simuler l'épaisseur d'un trait.
    """
    DECALAGE_X, DECALAGE_Y = calculer_decalages(donjon)
    i1, j1 = case1  # décompose le tuple
    i2, j2 = case2

    x1 = (
        j1 * TAILLE + TAILLE // 2 + DECALAGE_X
    )  # coordonnée X du centre, prenant le bord gauche de la salle (j1 * TAILLE) et en ajoutant la moitié de la taille de la salle (TAILLE // 2).
    y1 = i1 * TAILLE + TAILLE // 2 + DECALAGE_Y
    x2 = j2 * TAILLE + TAILLE // 2 + DECALAGE_X
    y2 = i2 * TAILLE + TAILLE // 2 + DECALAGE_Y

    # petit rectangle horizontal/vertical pour simuler une ligne
    if x1 == x2:  # même colonne → vertical
        if (
            y1 > y2
        ):  # S'assure que la coordonnée de début (y1) est la plus petite. Si y1 est plus grand que y2 (ce qui signifie qu'on va vers le haut), on inverse les valeurs pour que y1 soit le minimum et y2 le maximum.
            y1, y2 = y2, y1
        rectangle(x1 - 2, y1, x2 + 2, y2, remplissage="red")
    elif y1 == y2:  # même ligne → horizontal
        if x1 > x2:
            x1, x2 = x2, x1
        rectangle(x1, y1 - 2, x2, y2 + 2, remplissage="red")


def dessiner_tresor(i, j, donjon):
    """
    Dessine un trésor à la position spécifiée.
    """
    decalage_x, decalage_y = calculer_decalages(donjon)
    x = j * TAILLE + decalage_x
    y = i * TAILLE + decalage_y

    dx = (TAILLE - TAILLE_PERSO) // 2
    dy = (TAILLE - TAILLE_PERSO) // 2

    image(
        x + dx,
        y + dy,
        "tresor.png",
        ancrage="nw",
        hauteur=TAILLE_PERSO,
        largeur=TAILLE_PERSO,
    )


def dessiner_etat_complet(
    donjon,
    pos_av,
    niveau_av,
    dragons,
    intention,
    pos_tresor,
    tresors_restants,
    indice,
    afficher_indice,
):
    """
    Efface l'écran et dessine l'état complet du jeu.

    Pourquoi cette fonction ?
    Cette fonction centralise tout le dessin du jeu en un seul endroit.
    Au lieu de répéter le code de dessin partout (après chaque rotation,
    déplacement, placement de trésor, etc.), on appelle simplement cette
    fonction qui redessine tout l'écran à chaque changement. Cela évite
    les bugs d'affichage et rend le code plus maintenable.

    Cette fonction affiche tous les éléments visuels du jeu dans l'ordre :
    1. Fond bleu
    2. Informations en haut (nombre de dragons et trésors restants)
    3. Les salles du donjon
    4. Les lignes d'indice (chemin bleu - si activé)
    5. Les lignes d'intention (chemin rouge)
    6. Le trésor placé (s'il existe)
    7. Les dragons
    8. L'aventurier (en dernier pour être au-dessus)
    9. Les contrôles en bas de l'écran

    Paramètres :
        donjon : liste de listes de tuples (haut, droite, bas, gauche)
                 Représente la grille du donjon avec les portes
        pos_av : tuple (ligne, colonne)
                 Position actuelle de l'aventurier
        niveau_av : int
                    Niveau de puissance de l'aventurier
        dragons : liste de [position, niveau]
                  Liste des dragons encore en vie
        intention : liste de tuples (ligne, colonne)
                    Chemin tracé automatiquement (ligne rouge)
        pos_tresor : tuple (ligne, colonne) ou None
                     Position du trésor placé, None si aucun trésor
        tresors_restants : int
                           Nombre de trésors encore disponibles
        indice : liste de tuples (ligne, colonne) ou None
                 Chemin suggéré vers le dragon de plus bas niveau
        afficher_indice : bool
                          True si l'indice doit être affiché

    Retour : Aucun
    """
    efface_tout()
    rectangle(0, 0, 1248, 832, remplissage="#2a2a72")

    texte(
        20,
        20,
        "Dragons : " + str(len(dragons)),
        ancrage="nw",
        taille=16,
        couleur="white",
    )
    texte(
        20,
        45,
        "Trésors : " + str(tresors_restants),
        ancrage="nw",
        taille=16,
        couleur="white",
    )

    # Bouton Indice en haut à droite
    couleur_bouton = "cyan" if afficher_indice else "gray"
    rectangle(
        1100, 20, 1230, 60, remplissage=couleur_bouton, epaisseur=2, couleur="white"
    )
    texte(
        1165,
        40,
        "INDICE (I)",
        ancrage="center",
        taille=14,
        couleur="black" if afficher_indice else "darkgray",
    )

    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            dessiner_salle(i, j, donjon[i][j], donjon)

    # Dessiner l'indice (bleu clair) AVANT l'intention (rouge)
    if afficher_indice and indice is not None:
        for k in range(len(indice) - 1):
            dessiner_ligne_indice(indice[k], indice[k + 1], donjon)

    # Dessiner l'intention (rouge) par-dessus
    for k in range(len(intention) - 1):
        dessiner_ligne_intention(intention[k], intention[k + 1], donjon)

    # Dessiner le trésor s'il existe
    if pos_tresor is not None:
        i_t, j_t = pos_tresor
        dessiner_tresor(i_t, j_t, donjon)

    for d in dragons:
        pos_d, niv_d = d
        i_d, j_d = pos_d
        dessiner_dragon(i_d, j_d, niv_d, donjon)

    i_av, j_av = pos_av
    dessiner_aventurier(i_av, j_av, niveau_av, donjon)

    # Afficher le texte d'aide en bas sur 2 lignes
    texte(
        1248 // 2,
        760,
        "Clic Gauche : rotation | Clic Droit : placer un trésor  | I : indice",
        ancrage="center",
        taille=11,
        couleur="white",
    )
    texte(
        1248 // 2,
        795,
        "R : recommencer | Esc : menu | S : Sauvegarder | L : Charger",
        ancrage="center",
        taille=15,
        couleur="white",
    )

    mise_a_jour()


def afficher_donjon_fenetre(
    donjon, aventurier, dragons, nb_tresors, pos_tresor_initial
):
    """
    Gère toute la boucle de jeu : affichage, interactions et logique.

    Pourquoi cette fonction ?
    C'est le cœur du jeu qui fait tourner la partie. Elle gère :
    - L'affichage du donjon et des personnages
    - Les interactions du joueur
    - La logique du jeu
    - Les conditions de victoire/défaite
    Cette fonction tourne en boucle jusqu'à la fin de la partie, puis
    affiche l'écran de fin et retourne au menu principal.

    Déroulement :
    1. Initialisation : copie l'état initial pour permettre le reset
    2. Boucle principale : attend les actions du joueur
       - Clic gauche : pivoter une salle
       - Clic droit : placer un trésor
       - Espace : exécuter le chemin, déplacer l'aventurier et les dragons
       - R : recommencer la partie
       - S : sauvegarder la partie
       - L : charger une partie sauvegardée
       - Esc : retourner au menu
    3. Vérification de fin : victoire  ou défaite
    4. Écran de fin : affiche le résultat et attend une touche
    """
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])

    # Taille du donjon
    largeur_donjon = nb_colonnes * TAILLE
    hauteur_donjon = nb_lignes * TAILLE

    # Taille de la fenêtre (même que le menu)
    LARGEUR_FENETRE = 1248
    HAUTEUR_FENETRE = 832

    # Calculer le décalage pour centrer le donjon
    DECALAGE_X = (LARGEUR_FENETRE - largeur_donjon) // 2
    DECALAGE_Y = (HAUTEUR_FENETRE - hauteur_donjon) // 2

    # Redimensionner la fenêtre existante
    redimensionne_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    # Sauvegarde état initial pour le reset (R)
    donjon_initial = []
    for ligne in donjon:
        copie_ligne = ligne[:]
        donjon_initial.append(copie_ligne)
    aventurier_pos_initial = (aventurier[0][0], aventurier[0][1])
    aventurier_niv_initial = aventurier[1]
    dragons_initial = []
    for d in dragons:
        position_du_dragon = d[0]
        niveau_du_dragon = d[1]
        nouveau_dragon = [position_du_dragon, niveau_du_dragon]
        dragons_initial.append(nouveau_dragon)

    # État courant
    pos_av = (aventurier_pos_initial[0], aventurier_pos_initial[1])
    niveau_av = aventurier_niv_initial
    intention = []
    victoire = False
    defaite = False
    fini = False

    pos_tresor = pos_tresor_initial
    tresors_restants = nb_tresors

    # Variables pour l'indice
    afficher_indice = False
    indice = None

    # Calculer l'intention initiale
    intention = calculer_intention(donjon, pos_av, dragons, pos_tresor)
    if intention is None:
        intention = []

    # Premier affichage
    dessiner_etat_complet(
        donjon,
        pos_av,
        niveau_av,
        dragons,
        intention,
        pos_tresor,
        tresors_restants,
        indice,
        afficher_indice,
    )

    while not fini:
        ev = donne_ev()
        if ev:
            t = type_ev(ev)

            # Fermeture fenêtre
            if t == "Quitte":
                fini = True

            # Enlever le trésor placé (clic gauche)
            # Pivoter salle (clic gauche)
            elif t == "ClicGauche":
                x = abscisse(ev)
                y = ordonnee(ev)
                decalage_x, decalage_y = calculer_decalages(donjon)

                j = (x - decalage_x) // TAILLE
                i = (y - decalage_y) // TAILLE

                # Vérifier si on clique sur le bouton Indice
                if 1100 <= x <= 1230 and 20 <= y <= 60:
                    afficher_indice = not afficher_indice
                    if afficher_indice:
                        indice = calculer_indice(donjon, pos_av, dragons)
                    else:
                        indice = None
                    dessiner_etat_complet(
                        donjon,
                        pos_av,
                        niveau_av,
                        dragons,
                        intention,
                        pos_tresor,
                        tresors_restants,
                        indice,
                        afficher_indice,
                    )

                if 0 <= i < nb_lignes and 0 <= j < nb_colonnes:
                    # Pivoter la salle
                    donjon[i][j] = rotation_horaire(donjon[i][j])

                    # Toujours recalculer l'intention
                    intention = calculer_intention(donjon, pos_av, dragons, pos_tresor)
                    if intention is None:
                        intention = []

                    # Recalculer l'indice si activé
                    if afficher_indice:
                        indice = calculer_indice(donjon, pos_av, dragons)

                    dessiner_etat_complet(
                        donjon,
                        pos_av,
                        niveau_av,
                        dragons,
                        intention,
                        pos_tresor,
                        tresors_restants,
                        indice,
                        afficher_indice,
                    )

            # Clic droit : Placer/Enlever trésor OU Pivoter salle
            elif t == "ClicDroit":
                x = abscisse(ev)
                y = ordonnee(ev)
                decalage_x, decalage_y = calculer_decalages(donjon)

                j = (x - decalage_x) // TAILLE
                i = (y - decalage_y) // TAILLE
                case = (i, j)

                if 0 <= i < nb_lignes and 0 <= j < nb_colonnes:
                    # CAS 1 : On clique sur le trésor → L'enlever
                    if pos_tresor == case:
                        pos_tresor = None

                    # CAS 2 : On veut placer un trésor
                    elif tresors_restants > 0 and pos_tresor is None and case != pos_av:
                        # Vérifier qu'il n'y a pas de dragon sur cette case
                        case_occupee = False
                        for d in dragons:
                            if d[0] == case:
                                case_occupee = True
                                break

                        if not case_occupee:
                            # Placer le trésor
                            pos_tresor = case

                    # Recalcul de l'intention après toute action
                    intention = calculer_intention(donjon, pos_av, dragons, pos_tresor)
                    if intention is None:
                        intention = []

                    dessiner_etat_complet(
                        donjon,
                        pos_av,
                        niveau_av,
                        dragons,
                        intention,
                        pos_tresor,
                        tresors_restants,
                        indice,
                        afficher_indice,
                    )
            # Clavier
            elif t == "Touche":
                key = touche(ev)
                i = pos_av[0]
                j = pos_av[1]

                # Retour au menu (ESC)
                if key in ("Escape", "esc", "ESC"):
                    return "menu"

                i, j = pos_av

                # Reset complet (R)
                if key in ("r", "R"):
                    pos_tresor = None
                    tresors_restants = nb_tresors
                    donjon = [ligne[:] for ligne in donjon_initial]
                    pos_av = (aventurier_pos_initial[0], aventurier_pos_initial[1])
                    niveau_av = aventurier_niv_initial
                    aventurier[0] = pos_av
                    aventurier[1] = niveau_av
                    dragons = [[d[0], d[1]] for d in dragons_initial]
                    intention = calculer_intention(donjon, pos_av, dragons, pos_tresor)
                    if intention is None:
                        intention = []

                    victoire = False
                    defaite = False
                    dessiner_etat_complet(
                        donjon,
                        pos_av,
                        niveau_av,
                        dragons,
                        intention,
                        pos_tresor,
                        tresors_restants,
                        indice,
                        afficher_indice,
                    )

                # Sauvegarder (S)
                elif key in ("s", "S"):
                    sauvegarder_partie(
                        donjon, aventurier, dragons, tresors_restants, pos_tresor
                    )
                    # Afficher un message temporaire
                    texte(
                        1248 // 2,
                        10,
                        "Partie sauvegardée !",
                        ancrage="center",
                        taille=14,
                        couleur="green",
                    )
                    mise_a_jour()

                # Charger (L)
                elif key in ("l", "L"):
                    (
                        donjon_charge,
                        aventurier_charge,
                        dragons_charges,
                        tresors_restants,
                        pos_tresor,
                    ) = charger_partie()

                    if donjon_charge is not None:
                        # Remplacer l'état actuel par la sauvegarde
                        donjon = donjon_charge
                        aventurier = aventurier_charge
                        dragons = dragons_charges
                        pos_av = (aventurier[0][0], aventurier[0][1])
                        niveau_av = aventurier[1]
                        intention = []
                        victoire = False
                        defaite = False

                        intention = calculer_intention(
                            donjon, pos_av, dragons, pos_tresor
                        )
                        if intention is None:
                            intention = []

                        dessiner_etat_complet(
                            donjon,
                            pos_av,
                            niveau_av,
                            dragons,
                            intention,
                            pos_tresor,
                            tresors_restants,
                            indice,
                            afficher_indice,
                        )

                        # Afficher un message temporaire
                        texte(
                            1248 // 2,
                            10,
                            "Partie chargée !",
                            ancrage="center",
                            taille=14,
                            couleur="green",
                        )
                        mise_a_jour()
                # Touche I : indice
                elif key in ("i", "I"):
                    afficher_indice = not afficher_indice
                    if afficher_indice:
                        indice = calculer_indice(donjon, pos_av, dragons)
                    else:
                        indice = None
                    dessiner_etat_complet(
                        donjon,
                        pos_av,
                        niveau_av,
                        dragons,
                        intention,
                        pos_tresor,
                        tresors_restants,
                        indice,
                        afficher_indice,
                    )

                elif key in ("space", "Space", " "):
                    # Mémoriser la position de départ
                    pos_depart = pos_av

                    # L'aventurier se déplace sur tout son chemin
                    while len(intention) >= 2 and not fini:
                        prochaine = intention[1]
                        nouvelle_pos = deplacer_aventurier_si_possible(
                            donjon, pos_av, prochaine
                        )
                        if nouvelle_pos == pos_av:
                            break
                        pos_av = nouvelle_pos
                        aventurier[0] = pos_av

                        intention = intention[1:]

                        # Vérifier si on prend un trésor
                        if pos_tresor is not None and pos_tresor == pos_av:
                            pos_tresor = None
                            tresors_restants = tresors_restants - 1
                            intention = []  # Vider l'intention

                            # Recalculer l'indice si activé
                            if afficher_indice:
                                indice = calculer_indice(donjon, pos_av, dragons)

                            dessiner_etat_complet(
                                donjon,
                                pos_av,
                                niveau_av,
                                dragons,
                                intention,
                                pos_tresor,
                                tresors_restants,
                                indice,
                                afficher_indice,
                            )
                            break  #  Sortir de la boucle

                        # Gestion des combats avec les dragons
                        dragons, niveau_av, defaite = gerer_combat(
                            pos_av, niveau_av, dragons
                        )
                        aventurier[1] = niveau_av

                        if defaite:
                            fini = True
                        if len(dragons) == 0 and not defaite:
                            victoire = True
                            fini = True

                        dessiner_etat_complet(
                            donjon,
                            pos_av,
                            niveau_av,
                            dragons,
                            intention,
                            pos_tresor,
                            tresors_restants,
                            indice,
                            afficher_indice,
                        )

                    # Après que l'aventurier ait terminé son déplacement
                    # Les dragons se déplacent UNE SEULE FOIS
                    if not fini and len(dragons) > 0 and pos_av != pos_depart:
                        deplacer_dragons(donjon, dragons)

                        # Gestion des combats avec les dragons
                        dragons, niveau_av, defaite = gerer_combat(
                            pos_av, niveau_av, dragons
                        )
                        aventurier[1] = niveau_av

                        if defaite:
                            fini = True
                        # Vérifier la victoire après le déplacement des dragons
                        if len(dragons) == 0 and not defaite:
                            victoire = True
                            fini = True

                        # Recalculer l'intention après déplacement des dragons
                        intention = calculer_intention(
                            donjon, pos_av, dragons, pos_tresor
                        )
                        if intention is None:
                            intention = []

                        # Recalculer l'indice si activé
                        if afficher_indice:
                            indice = calculer_indice(donjon, pos_av, dragons)

                        dessiner_etat_complet(
                            donjon,
                            pos_av,
                            niveau_av,
                            dragons,
                            intention,
                            pos_tresor,
                            tresors_restants,
                            indice,
                            afficher_indice,
                        )

        mise_a_jour()

    # Écran de fin simple
    efface_tout()
    if victoire:
        texte(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 2 - 20,
            "Bien joué, tous les dragons ont été vaincus !",
            ancrage="center",
            taille=18,
            couleur="#2a2a72",
        )
    elif defaite:
        texte(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 2 - 20,
            "Dommage, vous avez été vaincu...",
            ancrage="center",
            taille=18,
            couleur="#2a2a72",
        )
    else:
        texte(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 2 - 20,
            "Partie terminée.",
            ancrage="center",
            taille=18,
            couleur="#2a2a72",
        )

    texte(
        LARGEUR_FENETRE // 2,
        HAUTEUR_FENETRE // 2 + 20,
        "Appuyez sur une touche pour revenir au menu.",
        ancrage="center",
        taille=12,
        couleur="#2a2a72",
    )
    mise_a_jour()

    attente = True
    while attente:
        ev = donne_ev()
        if ev:
            t = type_ev(ev)
            if t in ("Quitte", "Touche"):
                attente = False
        mise_a_jour()

    # Ne ferme PAS la fenêtre, on retourne juste au menu
    return "menu"


def editeur_donjon():
    """
    Éditeur de donjon entièrement graphique.

    Phase 1 : Choix des dimensions
    Phase 2 : Édition du donjon
    """

    redimensionne_fenetre(1248, 832)

    #  PHASE 1 : CHOIX DES DIMENSIONS
    nb_lignes = 5  # Valeur par défaut
    nb_colonnes = 5
    phase = "dimensions"  # "dimensions" ou "edition"

    while phase == "dimensions":
        efface_tout()
        rectangle(0, 0, 1248, 832, remplissage="#2a2a72")

        # Titre
        texte(
            1248 // 2,
            200,
            "ÉDITEUR DE DONJON",
            ancrage="center",
            taille=36,
            couleur="white",
        )
        texte(
            1248 // 2,
            250,
            "Choisissez les dimensions",
            ancrage="center",
            taille=18,
            couleur="lightgray",
        )

        # Affichage lignes
        texte(1248 // 2 - 150, 300, "Lignes :", ancrage="e", taille=20, couleur="white")
        rectangle(1248 // 2 - 150, 330, 1248 // 2 + 150, 380, remplissage="white")
        texte(
            1248 // 2, 355, str(nb_lignes), ancrage="center", taille=24, couleur="black"
        )

        # Boutons - / +
        rectangle(1248 // 2 - 250, 330, 1248 // 2 - 170, 380, remplissage="orange")
        texte(1248 // 2 - 210, 355, "-", ancrage="center", taille=30, couleur="white")

        rectangle(1248 // 2 + 170, 330, 1248 // 2 + 250, 380, remplissage="orange")
        texte(1248 // 2 + 210, 355, "+", ancrage="center", taille=30, couleur="white")

        # Affichage colonnes
        texte(
            1248 // 2 - 150, 410, "Colonnes :", ancrage="e", taille=20, couleur="white"
        )
        rectangle(1248 // 2 - 150, 430, 1248 // 2 + 150, 480, remplissage="white")
        texte(
            1248 // 2,
            455,
            str(nb_colonnes),
            ancrage="center",
            taille=24,
            couleur="black",
        )

        # Boutons - / +
        rectangle(1248 // 2 - 250, 430, 1248 // 2 - 170, 480, remplissage="orange")
        texte(1248 // 2 - 210, 455, "-", ancrage="center", taille=30, couleur="white")

        rectangle(1248 // 2 + 170, 430, 1248 // 2 + 250, 480, remplissage="orange")
        texte(1248 // 2 + 210, 455, "+", ancrage="center", taille=30, couleur="white")

        # Bouton Valider
        rectangle(1248 // 2 - 100, 550, 1248 // 2 + 100, 610, remplissage="green")
        texte(1248 // 2, 580, "CRÉER", ancrage="center", taille=24, couleur="white")

        # Bouton Retour
        rectangle(1248 // 2 - 100, 650, 1248 // 2 + 100, 710, remplissage="red")
        texte(1248 // 2, 680, "RETOUR", ancrage="center", taille=20, couleur="white")

        mise_a_jour()

        # Gestion événements
        ev = donne_ev()
        if ev:
            t = type_ev(ev)

            if t == "Quitte":
                return "menu"

            elif t == "ClicGauche":
                x = abscisse(ev)
                y = ordonnee(ev)

                # Lignes -
                if 1248 // 2 - 250 <= x <= 1248 // 2 - 170 and 330 <= y <= 380:
                    if nb_lignes > 3:
                        nb_lignes -= 1

                # Lignes +
                elif 1248 // 2 + 170 <= x <= 1248 // 2 + 250 and 330 <= y <= 380:
                    if nb_lignes < 10:
                        nb_lignes += 1

                # Colonnes -
                elif 1248 // 2 - 250 <= x <= 1248 // 2 - 170 and 430 <= y <= 480:
                    if nb_colonnes > 3:
                        nb_colonnes -= 1

                # Colonnes +
                elif 1248 // 2 + 170 <= x <= 1248 // 2 + 250 and 430 <= y <= 480:
                    if nb_colonnes < 10:
                        nb_colonnes += 1

                # Bouton Créer
                elif 1248 // 2 - 100 <= x <= 1248 // 2 + 100 and 550 <= y <= 610:
                    phase = "edition"

                # Bouton Retour
                elif 1248 // 2 - 100 <= x <= 1248 // 2 + 100 and 650 <= y <= 710:
                    return "menu"

            elif t == "Touche":
                key = touche(ev)
                if key in ("Escape", "esc", "ESC"):
                    return "menu"

        mise_a_jour()

    # PHASE 2 : ÉDITION
    # Créer le donjon avec toutes portes FERMÉES
    donjon = []
    for i in range(nb_lignes):
        ligne = []
        for j in range(nb_colonnes):
            salle = (True, True, True, True)  # ← Toutes portes fermées par défaut
            ligne.append(salle)
        donjon.append(ligne)

    # État de l'éditeur
    aventurier_pos = None
    dragons = []
    nb_tresors = 3  # Valeur par défaut

    mode = "salle"  # "salle", "aventurier", "dragon"
    niveau_dragon_selectionne = 1

    nom_fichier = "mon_niveau"
    message = ""
    message_temps = 0

    fini = False

    while not fini:
        # Affichage
        efface_tout()
        rectangle(0, 0, 1248, 832, remplissage="#2a2a72")

        # Calculer décalages
        decalage_x, decalage_y = calculer_decalages(donjon)

        # Dessiner les salles
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                dessiner_salle(i, j, donjon[i][j], donjon)

        # Dessiner l'aventurier
        if aventurier_pos is not None:
            i_av, j_av = aventurier_pos
            dessiner_aventurier(i_av, j_av, 1, donjon)

        # Dessiner les dragons
        for dragon in dragons:
            pos, niveau = dragon
            i_d, j_d = pos
            dessiner_dragon(i_d, j_d, niveau, donjon)

        # Interface - Panneau gauche
        rectangle(10, 10, 300, 400, remplissage="#1a1a3e", couleur="white", epaisseur=2)

        texte(155, 30, "ÉDITEUR", ancrage="center", taille=20, couleur="yellow")

        # Mode actuel
        couleur_mode = "lime" if mode == "salle" else "white"
        texte(
            20,
            70,
            f"Mode : {mode.upper()}",
            ancrage="nw",
            taille=14,
            couleur=couleur_mode,
        )

        if mode == "dragon":
            texte(
                20,
                95,
                f"Niveau : {niveau_dragon_selectionne}",
                ancrage="nw",
                taille=12,
                couleur="white",
            )

        # Statistiques
        texte(
            20,
            130,
            f"Dimensions : {nb_lignes}x{nb_colonnes}",
            ancrage="nw",
            taille=12,
            couleur="lightgray",
        )
        texte(
            20, 150, f"Trésors : {nb_tresors}", ancrage="nw", taille=12, couleur="gold"
        )
        texte(
            20,
            170,
            f"Dragons : {len(dragons)}",
            ancrage="nw",
            taille=12,
            couleur="orange",
        )

        aventurier_text = "✓ Placé" if aventurier_pos else "✗ Non placé"
        couleur_av = "lime" if aventurier_pos else "red"
        texte(
            20,
            190,
            f"Aventurier : {aventurier_text}",
            ancrage="nw",
            taille=12,
            couleur=couleur_av,
        )

        # Boutons de mode
        texte(20, 230, "MODES :", ancrage="nw", taille=14, couleur="white")

        # Bouton Salle
        couleur_btn = "orange" if mode == "salle" else "gray"
        rectangle(20, 250, 140, 290, remplissage=couleur_btn)
        texte(80, 270, "Salle (S)", ancrage="center", taille=12, couleur="white")

        # Bouton Aventurier
        couleur_btn = "orange" if mode == "aventurier" else "gray"
        rectangle(170, 250, 290, 290, remplissage=couleur_btn)
        texte(230, 270, "Aventurier (A)", ancrage="center", taille=12, couleur="white")

        # Bouton Dragon
        couleur_btn = "orange" if mode == "dragon" else "gray"
        rectangle(20, 300, 140, 340, remplissage=couleur_btn)
        texte(80, 320, "Dragon (D)", ancrage="center", taille=12, couleur="white")

        # Niveau dragon (si mode dragon)
        if mode == "dragon":
            texte(170, 310, "Niv:", ancrage="nw", taille=12, couleur="white")
            for niv in [1, 2, 3]:
                couleur_niv = "lime" if niv == niveau_dragon_selectionne else "gray"
                rectangle(
                    210 + (niv - 1) * 25,
                    300,
                    230 + (niv - 1) * 25,
                    340,
                    remplissage=couleur_niv,
                )
                texte(
                    220 + (niv - 1) * 25,
                    320,
                    str(niv),
                    ancrage="center",
                    taille=14,
                    couleur="white",
                )

        # Actions
        texte(20, 360, "ACTIONS :", ancrage="nw", taille=14, couleur="white")

        # Panneau bas - Contrôles
        rectangle(
            10, 750, 1238, 822, remplissage="#1a1a3e", couleur="white", epaisseur=2
        )
        texte(624, 765, "CONTRÔLES", ancrage="center", taille=14, couleur="yellow")
        texte(
            624,
            788,
            "Clic G : rotation | Clic D (mode salle) : changer de salles | Clic D (autres) : placer | S/A/D : changer mode",
            ancrage="center",
            taille=11,
            couleur="white",
        )
        texte(
            624,
            808,
            "T : +trésor | Y : -trésor | V : sauvegarder | C : effacer tout | Esc : retour menu",
            ancrage="center",
            taille=11,
            couleur="white",
        )

        couleur_jouer = (
            "green" if aventurier_pos is not None and len(dragons) > 0 else "gray"
        )
        rectangle(
            1050,
            750,
            1230,
            815,
            remplissage=couleur_jouer,
            epaisseur=3,
            couleur="white",
        )
        texte(
            1140,
            782,
            "JOUER",
            ancrage="center",
            taille=24,
            couleur="white" if aventurier_pos and len(dragons) > 0 else "darkgray",
        )

        # Message temporaire
        if message and message_temps > 0:
            rectangle(400, 10, 850, 60, remplissage="green")
            texte(625, 35, message, ancrage="center", taille=16, couleur="white")
            message_temps -= 1

        mise_a_jour()

        # Gestion événements
        ev = donne_ev()
        if ev:
            t = type_ev(ev)

            if t == "Quitte":
                fini = True

            # Clic gauche : Pivoter salle
            elif t == "ClicGauche":
                x = abscisse(ev)
                y = ordonnee(ev)

                # Vérifier si on clique sur le bouton JOUER
                if 1050 <= x <= 1230 and 750 <= y <= 815:
                    # Vérifier que le niveau est jouable
                    if aventurier_pos is None:
                        message = "❌ Placez l'aventurier !"
                        message_temps = 120
                    elif len(dragons) == 0:
                        message = "❌ Placez au moins un dragon !"
                        message_temps = 120
                    else:
                        # Préparer l'aventurier au bon format
                        aventurier = [aventurier_pos, 1]

                        # Lancer le jeu
                        resultat = afficher_donjon_fenetre(
                            donjon, aventurier, dragons, nb_tresors, None
                        )

                        # Après le jeu, revenir à l'éditeur
                        # Redimensionner la fenêtre pour l'éditeur
                        redimensionne_fenetre(1248, 832)

                        message = "Retour à l'éditeur"
                        message_temps = 90

                # Vérifier boutons interface
                elif 20 <= x <= 140 and 250 <= y <= 290:
                    mode = "salle"

                # Bouton Aventurier
                elif 170 <= x <= 290 and 250 <= y <= 290:
                    mode = "aventurier"

                # Bouton Dragon
                elif 20 <= x <= 140 and 300 <= y <= 340:
                    mode = "dragon"

                # Boutons niveau dragon
                elif mode == "dragon" and 300 <= y <= 340:
                    if 210 <= x <= 230:
                        niveau_dragon_selectionne = 1
                    elif 235 <= x <= 255:
                        niveau_dragon_selectionne = 2
                    elif 260 <= x <= 280:
                        niveau_dragon_selectionne = 3

                # Clic dans le donjon
                else:
                    j = (x - decalage_x) // TAILLE
                    i = (y - decalage_y) // TAILLE

                    if 0 <= i < nb_lignes and 0 <= j < nb_colonnes:
                        if mode == "salle":
                            # Rotation horaire classique
                            donjon[i][j] = rotation_horaire(donjon[i][j])

            # Clic droit : Changer type de salle OU Placer aventurier/dragon
            elif t == "ClicDroit":
                x = abscisse(ev)
                y = ordonnee(ev)
                j = (x - decalage_x) // TAILLE
                i = (y - decalage_y) // TAILLE
                case = (i, j)

                if 0 <= i < nb_lignes and 0 <= j < nb_colonnes:
                    if mode == "salle":
                        # Cycle à travers toutes les configurations
                        donjon[i][j] = salle_suivante(donjon[i][j])

                    elif mode == "aventurier":
                        # Vérifier qu'il n'y a pas de dragon sur cette case
                        case_occupee = False
                        for d in dragons:
                            if d[0] == case:
                                case_occupee = True
                                break

                        if not case_occupee:
                            # Placer l'aventurier
                            aventurier_pos = case
                            message = "Aventurier placé !"
                            message_temps = 60
                        else:
                            message = "❌ Case occupée par un dragon !"
                            message_temps = 60

                    elif mode == "dragon":
                        # Vérifier qu'il n'y a pas l'aventurier sur cette case
                        if aventurier_pos == case:
                            message = "❌ Case occupée par l'aventurier !"
                            message_temps = 60
                        else:
                            # Vérifier si dragon existe déjà
                            dragon_existant = None
                            for idx, d in enumerate(dragons):
                                if d[0] == case:
                                    dragon_existant = idx
                                    break

                            if dragon_existant is not None:
                                dragons.pop(dragon_existant)
                                message = "Dragon supprimé !"
                                message_temps = 60
                            else:
                                dragons.append([case, niveau_dragon_selectionne])
                                message = (
                                    f"Dragon niv.{niveau_dragon_selectionne} ajouté !"
                                )
                                message_temps = 60

                                # Passer automatiquement au niveau suivant
                                niveau_dragon_selectionne += 1
                                if niveau_dragon_selectionne > 3:
                                    niveau_dragon_selectionne = 1
            # Touches
            elif t == "Touche":
                key = touche(ev)

                # Esc : Retour menu
                if key in ("Escape", "esc", "ESC"):
                    fini = True

                # S : Mode salle
                elif key in ("s", "S"):
                    mode = "salle"

                # A : Mode aventurier
                elif key in ("a", "A"):
                    mode = "aventurier"

                # D : Mode dragon
                elif key in ("d", "D"):
                    mode = "dragon"

                # 1/2/3 : Niveau dragon
                elif key == "1":
                    niveau_dragon_selectionne = 1
                elif key == "2":
                    niveau_dragon_selectionne = 2
                elif key == "3":
                    niveau_dragon_selectionne = 3

                # T : +1 trésor
                elif key in ("t", "T"):
                    nb_tresors += 1
                    message = f"Trésors : {nb_tresors}"
                    message_temps = 60

                # Y : -1 trésor
                elif key in ("y", "Y"):
                    if nb_tresors > 0:
                        nb_tresors -= 1
                        message = f"Trésors : {nb_tresors}"
                        message_temps = 60

                # V : Sauvegarder
                elif key in ("v", "V"):
                    if aventurier_pos is None:
                        message = "❌ Placez l'aventurier !"
                        message_temps = 120
                    else:
                        # Générer nom automatique

                        timestamp = strftime("%Y%m%d_%H%M%S")
                        nom_fichier = f"niveau_{timestamp}.txt"
                        sauvegarder_niveau(
                            donjon, aventurier_pos, dragons, nb_tresors, nom_fichier
                        )
                        message = f"✓ Sauvegardé : {nom_fichier}"
                        message_temps = 180

                # C : Clear
                elif key in ("c", "C"):
                    # Réinitialiser tout
                    for i in range(nb_lignes):
                        for j in range(nb_colonnes):
                            donjon[i][j] = (True, True, True, True)
                    aventurier_pos = None
                    dragons = []
                    message = "✓ Tout effacé !"
                    message_temps = 90

        mise_a_jour()

    return "menu"


def lancer_niveau_aleatoire():
    """
    Génère et lance immédiatement un niveau aléatoire.
    Tous les paramètres sont choisis aléatoirement.
    """

    print("=== GÉNÉRATION NIVEAU ALÉATOIRE ===")

    # Paramètres aléatoires
    nb_lignes = randint(3, 7)
    nb_colonnes = randint(3, 7)
    nb_dragons = randint(1, 3)
    nb_tresors = randint(1, 5)

    print(f"Dimensions : {nb_lignes}x{nb_colonnes}")
    print(f"Dragons : {nb_dragons}")
    print(f"Trésors : {nb_tresors}")

    # Générer le niveau
    donjon, aventurier_pos, dragons, nb_tresors = generer_niveau_aleatoire(
        nb_lignes, nb_colonnes, nb_dragons, nb_tresors
    )

    # Convertir aventurier_pos en format attendu
    aventurier = [aventurier_pos, 1]

    print("✓ Niveau généré !")

    # Lancer le jeu
    return donjon, aventurier, dragons, nb_tresors


def dessiner_ligne_indice(case1, case2, donjon):
    """
    Dessine une ligne bleue claire entre deux cases adjacentes (indice).
    """
    DECALAGE_X, DECALAGE_Y = calculer_decalages(donjon)

    i1, j1 = case1
    i2, j2 = case2

    x1 = j1 * TAILLE + TAILLE // 2 + DECALAGE_X
    y1 = i1 * TAILLE + TAILLE // 2 + DECALAGE_Y
    x2 = j2 * TAILLE + TAILLE // 2 + DECALAGE_X
    y2 = i2 * TAILLE + TAILLE // 2 + DECALAGE_Y

    ligne(x1, y1, x2, y2, couleur="cyan", epaisseur=4)
