from random import randint, choice, shuffle

# Une salle est représentée par un tuple de 4 booléens :
# (haut, droite, bas, gauche)
# True  = porte ouverte
# False = porte fermée


def rotation_horaire(salle):
    """
    Tourne la salle 90° dans le sens horaire :
    (haut, droite, bas, gauche) devient (gauche, haut, droite, bas)
    """
    haut, droite, bas, gauche = salle
    return (gauche, haut, droite, bas)


def sont_voisines(pos1, pos2):
    """Retourne True si pos1 et pos2 sont voisines (haut/bas/gauche/droite)."""
    i1, j1 = pos1
    i2, j2 = pos2
    return (i1 == i2 and abs(j1 - j2) == 1) or (j1 == j2 and abs(i1 - i2) == 1)


def sont_connectees(donjon, pos1, pos2):
    """
    Deux cases sont connectées si :
    elles sont voisines
    les portes entre elles sont ouvertes
    """
    if not sont_voisines(pos1, pos2):
        return False

    i1, j1 = pos1
    i2, j2 = pos2

    salle1 = donjon[i1][j1]
    salle2 = donjon[i2][j2]

    # pos2 à droite de pos1
    if j2 == j1 + 1 and i2 == i1:
        return salle1[1] and salle2[3]  # il faut que la porte droite de salle1 est True
        # et la porte gauche de salle2

    # pos2 à gauche
    if j2 == j1 - 1 and i2 == i1:
        return salle1[3] and salle2[1]

    # pos2 en bas
    if i2 == i1 + 1 and j2 == j1:
        return salle1[2] and salle2[0]

    # pos2 en haut
    if i2 == i1 - 1 and j2 == j1:
        return salle1[0] and salle2[2]

    return False


def deplacer_aventurier_si_possible(donjon, pos_actuelle, pos_visee):
    """
    Renvoie :
    la position visée si les salles sont connectées
    sinon, la position actuelle
    """
    max_i = len(donjon)
    max_j = len(donjon[0])
    i, j = pos_visee

    # Si on sort du donjon → impossible
    if not (0 <= i < max_i and 0 <= j < max_j):
        return pos_actuelle

    if sont_connectees(donjon, pos_actuelle, pos_visee):
        return pos_visee
    return pos_actuelle


def nom_image_salle(salle):
    """
    Retourne le nom de fichier de la tuile correspondant à la salle.
    salle = (haut, droite, bas, gauche) avec des booléens.
    Exemple : (True, False, True, False) -> 'tile_HB.png'

    Note : Pour les salles fermées (False, False, False, False),
    retourne None pour permettre un affichage personnalisé.
    """
    haut, droite, bas, gauche = salle
    code = ""

    if haut:
        code += "H"
    if droite:
        code += "D"
    if bas:
        code += "B"
    if gauche:
        code += "G"

    if code == "":
        return None  # ← Retourne None au lieu de "tile_X.png"

    return "tile_" + code + ".png"


def sauvegarder_partie(
    donjon,
    aventurier,
    dragons,
    tresors_restants,
    pos_tresor,
    nom_fichier="sauvegarde.txt",
):
    """
    Sauvegarde la partie dans un fichier texte
    """
    fichier = open(nom_fichier, "w")

    # Sauvegarder les dimensions du donjon
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    fichier.write(str(nb_lignes) + "\n")
    fichier.write(str(nb_colonnes) + "\n")

    # Sauvegarder le donjon
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            salle = donjon[i][j]
            # Convertir (True, False, True, False) en "1010"
            ligne_salle = ""
            if salle[0]:
                ligne_salle += "1"
            else:
                ligne_salle += "0"
            if salle[1]:
                ligne_salle += "1"
            else:
                ligne_salle += "0"
            if salle[2]:
                ligne_salle += "1"
            else:
                ligne_salle += "0"
            if salle[3]:
                ligne_salle += "1"
            else:
                ligne_salle += "0"
            fichier.write(ligne_salle + "\n")

    # Sauvegarder l'aventurier
    fichier.write(str(aventurier[0][0]) + "\n")  # ligne
    fichier.write(str(aventurier[0][1]) + "\n")  # colonne
    fichier.write(str(aventurier[1]) + "\n")  # niveau

    # Sauvegarder le nombre de dragons
    fichier.write(str(len(dragons)) + "\n")

    # Sauvegarder chaque dragon
    for dragon in dragons:
        fichier.write(str(dragon[0][0]) + "\n")  # ligne
        fichier.write(str(dragon[0][1]) + "\n")  # colonne
        fichier.write(str(dragon[1]) + "\n")  # niveau

    # Trésors restants
    fichier.write(str(tresors_restants) + "\n")

    # Position du trésor placé (ou -1 -1 si aucun)
    if pos_tresor is None:
        fichier.write("-1\n-1\n")
    else:
        fichier.write(str(pos_tresor[0]) + "\n")
        fichier.write(str(pos_tresor[1]) + "\n")

    fichier.close()
    print("Partie sauvegardée dans " + nom_fichier)


def charger_partie(nom_fichier="sauvegarde.txt"):
    """
    Charge la partie depuis un fichier texte
    Retourne : donjon, aventurier, dragons
    """
    fichier = open(nom_fichier, "r")

    # Lire les dimensions
    nb_lignes = int(fichier.readline())
    nb_colonnes = int(fichier.readline())

    # Reconstruire le donjon
    donjon = []
    for i in range(nb_lignes):
        ligne = []
        for j in range(nb_colonnes):
            ligne_salle = fichier.readline()
            # Convertir "1010" en (True, False, True, False)
            haut = ligne_salle[0] == "1"
            droite = ligne_salle[1] == "1"
            bas = ligne_salle[2] == "1"
            gauche = ligne_salle[3] == "1"
            salle = (haut, droite, bas, gauche)
            ligne.append(salle)
        donjon.append(ligne)

    # Lire l'aventurier
    av_ligne = int(fichier.readline())
    av_col = int(fichier.readline())
    av_niveau = int(fichier.readline())
    aventurier = [(av_ligne, av_col), av_niveau]  # Tuple au lieu de liste

    # Lire les dragons
    nb_dragons = int(fichier.readline())
    dragons = []
    for i in range(nb_dragons):
        d_ligne = int(fichier.readline())
        d_col = int(fichier.readline())
        d_niveau = int(fichier.readline())
        dragon = [(d_ligne, d_col), d_niveau]  # Tuple au lieu de liste
        dragons.append(dragon)

    # Trésors
    tresors_restants = int(fichier.readline())
    t_i = int(fichier.readline())
    t_j = int(fichier.readline())
    if t_i == -1 and t_j == -1:
        pos_tresor = None
    else:
        pos_tresor = (t_i, t_j)

    fichier.close()
    print("Partie chargée depuis " + nom_fichier)
    return donjon, aventurier, dragons, tresors_restants, pos_tresor


def deplacer_dragons(donjon, dragons):
    """
    Déplace chaque dragon d'une case dans une direction aléatoire.
    Le dragon ne bouge que s'il peut accéder à une salle voisine.
    """

    # Pour chaque dragon
    for dragon in dragons:
        pos_dragon = dragon[0]  # (ligne, colonne)
        i, j = pos_dragon

        # Liste des directions possibles : haut, droite, bas, gauche
        directions = []

        # Vérifier le haut (i-1, j)
        if i > 0:
            nouvelle_pos = (i - 1, j)
            if sont_connectees(donjon, pos_dragon, nouvelle_pos):
                directions.append(nouvelle_pos)

        # Vérifier la droite (i, j+1)
        if j < len(donjon[0]) - 1:
            nouvelle_pos = (i, j + 1)
            if sont_connectees(donjon, pos_dragon, nouvelle_pos):
                directions.append(nouvelle_pos)

        # Vérifier le bas (i+1, j)
        if i < len(donjon) - 1:
            nouvelle_pos = (i + 1, j)
            if sont_connectees(donjon, pos_dragon, nouvelle_pos):
                directions.append(nouvelle_pos)

        # Vérifier la gauche (i, j-1)
        if j > 0:
            nouvelle_pos = (i, j - 1)
            if sont_connectees(donjon, pos_dragon, nouvelle_pos):
                directions.append(nouvelle_pos)

        # Si le dragon peut se déplacer, choisir une direction au hasard
        if len(directions) > 0:
            nouvelle_pos = choice(directions)
            dragon[0] = nouvelle_pos  # Mettre à jour la position du dragon


def caractere_vers_salle(caractere):
    """
    Convertit un caractère spécial en salle (tuple de 4 booléens).
    Format : (haut, droite, bas, gauche)
    """
    conversions = {
        "╬": (True, True, True, True),
        "╠": (True, True, True, False),
        "╦": (False, True, True, True),
        "╣": (True, False, True, True),
        "╩": (True, True, False, True),
        "╔": (False, True, True, False),
        "╗": (False, False, True, True),
        "╚": (True, True, False, False),
        "╝": (True, False, False, True),
        "═": (False, True, False, True),
        "║": (True, False, True, False),
        "╥": (False, False, True, False),
        "╨": (True, False, False, False),
        "╡": (False, False, False, True),
        "╞": (False, True, False, False),
    }

    # Retourner la salle correspondante ou une salle fermée par défaut
    if caractere in conversions:
        return conversions[caractere]
    else:
        return (False, False, False, False)


def charger_niveau_complet(nom_fichier):
    """
    Charge un niveau complet depuis un fichier :
    - Première partie : le donjon avec les caractères
    - Deuxième partie : les positions des personnages

    Retourne : donjon, aventurier, dragons, nb_tresors
    """
    fichier = open(nom_fichier, "r", encoding="utf-8")

    donjon = []
    lignes = fichier.readlines()

    # Variables pour séparer les deux parties
    partie_donjon = True
    aventurier = None
    dragons = []
    nb_tresors = 0

    for ligne_texte in lignes:
        if ligne_texte == "\n" and partie_donjon:
            partie_donjon = False
            continue

        # Partie 1 : Le donjon
        if partie_donjon:
            if ligne_texte == "\n":
                continue

            ligne_salles = []
            for caractere in ligne_texte:
                if caractere == "\n":
                    continue
                salle = caractere_vers_salle(caractere)
                ligne_salles.append(salle)

            donjon.append(ligne_salles)

        # Partie 2 : Les personnages
        else:
            if ligne_texte == "\n":
                continue

            # Séparer la ligne en mots
            mots = ligne_texte.split()

            if len(mots) == 0:
                continue

            # A ligne colonne -> Aventurier
            if mots[0] == "A":
                ligne = int(mots[1])
                colonne = int(mots[2])
                aventurier = [(ligne, colonne), 1]

            # D ligne colonne niveau -> Dragon
            elif mots[0] == "D":
                ligne = int(mots[1])
                colonne = int(mots[2])
                niveau = int(mots[3])
                dragon = [(ligne, colonne), niveau]
                dragons.append(dragon)

            # T nombre -> Nombre de trésors
            elif mots[0] == "T":
                nb_tresors = int(mots[1])

    fichier.close()
    return donjon, aventurier, dragons, nb_tresors


def gerer_combat(pos_av, niveau_av, dragons):
    """
    Gère les combats entre l'aventurier et les dragons.

    Retour : (nouveaux_dragons, nouveau_niveau_av, defaite)
    """
    nouveaux_dragons = []
    defaite = False

    for d in dragons:
        pos_d, niv_d = d
        if pos_d == pos_av:
            # Combat !
            if niveau_av >= niv_d:
                # Victoire : aventurier monte de niveau
                niveau_av += 1
                # Dragon éliminé (pas ajouté à la nouvelle liste)
            else:
                # Défaite
                defaite = True
                nouveaux_dragons.append(d)
        else:
            # Dragon pas touché
            nouveaux_dragons.append(d)

    return nouveaux_dragons, niveau_av, defaite


def calculer_intention(donjon, position, dragons, pos_tresor):
    """
    Calcule automatiquement le chemin vers le trésor (prioritaire) ou le dragon
    accessible de plus haut niveau.

    Priorité :
    1. Si un trésor est placé → chemin vers le trésor
    2. Sinon → chemin vers le dragon accessible de plus haut niveau


    Paramètres :
        donjon : liste de listes de tuples (haut, droite, bas, gauche)
                 La grille du donjon
        position : tuple (ligne, colonne)
                   Position de départ de l'aventurier
        dragons : liste de [position, niveau]
                  Liste des dragons présents dans le donjon
        pos_tresor : tuple (ligne, colonne) ou None
                     Position du trésor placé (None si aucun)

    Retour :
        liste de tuples : Chemin vers le trésor ou le dragon de plus haut niveau
        None : Si rien n'est accessible
    """
    if len(dragons) == 0 and pos_tresor is None:
        return None

    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])

    # File d'attente : (position_actuelle, chemin_parcouru)
    file = [(position, [position])]
    visites = {position}

    # Dictionnaire : position_dragon -> (chemin, niveau)
    dragons_accessibles = {}
    chemin_tresor = None

    # Dictionnaire des positions de dragons
    dragons_positions = {}
    for d in dragons:
        pos_d, niv_d = d
        dragons_positions[pos_d] = niv_d

    while len(file) > 0:
        pos_actuelle, chemin = file.pop(0)
        i, j = pos_actuelle

        # PRIORITÉ 1 : Vérifier si on a atteint le trésor
        if pos_tresor is not None and pos_actuelle == pos_tresor:
            chemin_tresor = chemin
            # On peut arrêter la recherche dès qu'on trouve le trésor
            # car il est prioritaire sur tout
            break

        # Vérifier si on a atteint un dragon
        if pos_actuelle in dragons_positions:
            niveau_dragon = dragons_positions[pos_actuelle]
            dragons_accessibles[pos_actuelle] = (chemin, niveau_dragon)

        # Explorer les 4 directions
        directions = [
            (i - 1, j),  # Haut
            (i, j + 1),  # Droite
            (i + 1, j),  # Bas
            (i, j - 1),  # Gauche
        ]

        for nouvelle_pos in directions:
            ni, nj = nouvelle_pos

            # Vérifier que la position est dans le donjon
            if 0 <= ni < nb_lignes and 0 <= nj < nb_colonnes:
                # Vérifier que les salles sont connectées et non visitées
                if nouvelle_pos not in visites and sont_connectees(
                    donjon, pos_actuelle, nouvelle_pos
                ):
                    visites.add(nouvelle_pos)
                    nouveau_chemin = chemin + [nouvelle_pos]
                    file.append((nouvelle_pos, nouveau_chemin))

    # Si un trésor est accessible, retourner son chemin (PRIORITÉ ABSOLUE)
    if chemin_tresor is not None:
        return chemin_tresor

    # Sinon, si aucun dragon n'est accessible
    if len(dragons_accessibles) == 0:
        return None

    # Trouver le dragon de PLUS HAUT niveau parmi les accessibles
    meilleur_dragon = None
    meilleur_niveau = -1
    meilleur_chemin = None

    for pos_dragon, (chemin, niveau) in dragons_accessibles.items():
        if niveau > meilleur_niveau:
            meilleur_niveau = niveau
            meilleur_chemin = chemin
            meilleur_dragon = pos_dragon

    return meilleur_chemin


def salle_vers_caractere(salle):
    """
    Convertit une salle (tuple de booléens) en caractère Unicode.
    Inverse de caractere_vers_salle().
    """
    conversions_inverses = {
        (True, True, True, True): "╬",
        (True, True, True, False): "╠",
        (False, True, True, True): "╦",
        (True, False, True, True): "╣",
        (True, True, False, True): "╩",
        (False, True, True, False): "╔",
        (False, False, True, True): "╗",
        (True, True, False, False): "╚",
        (True, False, False, True): "╝",
        (False, True, False, True): "═",
        (True, False, True, False): "║",
        (False, False, True, False): "╥",
        (True, False, False, False): "╨",
        (False, False, False, True): "╡",
        (False, True, False, False): "╞",
        (False, False, False, False): " ",  # Salle fermée = espace
    }
    return conversions_inverses.get(salle, " ")


def sauvegarder_niveau(donjon, aventurier, dragons, nb_tresors, nom_fichier):
    """
    Sauvegarde un niveau créé dans l'éditeur au format .txt
    """
    fichier = open(nom_fichier, "w", encoding="utf-8")

    # Partie 1 : Le donjon avec caractères Unicode
    for ligne in donjon:
        ligne_texte = ""
        for salle in ligne:
            ligne_texte += salle_vers_caractere(salle)
        fichier.write(ligne_texte + "\n")

    # Ligne vide
    fichier.write("\n")

    # Partie 2 : Personnages et trésors
    if aventurier is not None:
        i, j = aventurier
        fichier.write(f"A {i} {j}\n")

    for dragon in dragons:
        pos, niveau = dragon
        i, j = pos
        fichier.write(f"D {i} {j} {niveau}\n")

    fichier.write(f"T {nb_tresors}\n")

    fichier.close()
    print(f"Niveau sauvegardé dans {nom_fichier}")


def salle_suivante(salle):
    """
    Cycle simple à travers 5 configurations de base.

    Ordre :
    1. Haut seul (1 porte)
    2. Haut + Droite (2 portes)
    3. Haut + Bas (2 portes)
    4. Haut + Droite + Bas (3 portes)
    5. Toutes ouvertes (4 portes)
    -> Retour au début
    """
    configurations = [
        (True, False, False, False),  # 1 porte : Haut
        (True, True, False, False),  # 2 portes : Haut + Droite
        (True, False, True, False),  # 2 portes : Haut + Bas
        (True, True, True, False),  # 3 portes : Haut + Droite + Bas
        (True, True, True, True),  # 4 portes : Toutes ouvertes
    ]

    # Trouver l'index de la configuration actuelle
    if salle in configurations:
        index = configurations.index(salle)
        # Passer à la suivante (cycle)
        index_suivant = (index + 1) % len(configurations)
        return configurations[index_suivant]
    else:
        # Si pas dans la liste, commencer par Haut seul
        return configurations[0]


def ajouter_murs_voisins(case, visites, murs, nb_lignes, nb_colonnes):
    """
    Ajoute les murs voisins d'une case à la liste des candidats.
    """
    i, j = case

    # Haut
    if i > 0:
        voisin = (i - 1, j)
        if voisin not in visites:
            murs.append((case, voisin, "haut"))

    # Droite
    if j < nb_colonnes - 1:
        voisin = (i, j + 1)
        if voisin not in visites:
            murs.append((case, voisin, "droite"))

    # Bas
    if i < nb_lignes - 1:
        voisin = (i + 1, j)
        if voisin not in visites:
            murs.append((case, voisin, "bas"))

    # Gauche
    if j > 0:
        voisin = (i, j - 1)
        if voisin not in visites:
            murs.append((case, voisin, "gauche"))


def generer_labyrinthe_parfait(nb_lignes, nb_colonnes):
    """
    Génère un labyrinthe parfait .

    Un labyrinthe parfait garantit que toutes les cases sont accessibles.
    """

    # Initialiser toutes les salles fermées
    donjon = []
    for i in range(nb_lignes):
        ligne = []
        for j in range(nb_colonnes):
            ligne.append((False, False, False, False))
        donjon.append(ligne)

    # Ensemble des cases visitées
    visites = set()

    # Commencer par une case aléatoire
    case_depart = (randint(0, nb_lignes - 1), randint(0, nb_colonnes - 1))
    visites.add(case_depart)

    # Liste des murs candidats (case1, case2, direction)
    murs = []

    # Ajouter les murs de la case de départ
    ajouter_murs_voisins(case_depart, visites, murs, nb_lignes, nb_colonnes)

    # Algorithme de Prim
    while len(murs) > 0:
        # Choisir un mur aléatoire
        mur_index = randint(0, len(murs) - 1)
        case1, case2, direction = murs[mur_index]
        murs.pop(mur_index)

        # Si la case2 n'est pas visitée, ouvrir le passage
        if case2 not in visites:
            visites.add(case2)

            # Ouvrir les portes entre case1 et case2
            i1, j1 = case1
            i2, j2 = case2

            haut1, droite1, bas1, gauche1 = donjon[i1][j1]
            haut2, droite2, bas2, gauche2 = donjon[i2][j2]

            if direction == "haut":
                donjon[i1][j1] = (True, droite1, bas1, gauche1)
                donjon[i2][j2] = (haut2, droite2, True, gauche2)
            elif direction == "droite":
                donjon[i1][j1] = (haut1, True, bas1, gauche1)
                donjon[i2][j2] = (haut2, droite2, bas2, True)
            elif direction == "bas":
                donjon[i1][j1] = (haut1, droite1, True, gauche1)
                donjon[i2][j2] = (True, droite2, bas2, gauche2)
            elif direction == "gauche":
                donjon[i1][j1] = (haut1, droite1, bas1, True)
                donjon[i2][j2] = (haut2, True, bas2, gauche2)

            # Ajouter les murs de la nouvelle case
            ajouter_murs_voisins(case2, visites, murs, nb_lignes, nb_colonnes)

    return donjon


def generer_niveau_aleatoire(nb_lignes, nb_colonnes, nb_dragons, nb_tresors):
    """
    Génère un niveau aléatoire complet avec :
    - Un labyrinthe parfait
    - Un aventurier placé aléatoirement
    - Des dragons placés aléatoirement avec des niveaux croissants
    - Un nombre défini de trésors

    Garantit qu'il existe toujours une solution.
    L'aventurier et les dragons ne peuvent pas être sur la même case.
    """

    # Générer le labyrinthe
    donjon = generer_labyrinthe_parfait(nb_lignes, nb_colonnes)

    # Liste de toutes les cases
    toutes_cases = []
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            toutes_cases.append((i, j))

    # Mélanger les cases
    shuffle(toutes_cases)

    # Placer l'aventurier sur la première case
    aventurier_pos = toutes_cases[0]

    # Placer les dragons sur les cases suivantes (PAS sur la même case que l'aventurier)
    dragons = []
    index_dragon = 1  # Commence à 1 pour éviter la case de l'aventurier

    for k in range(nb_dragons):
        if index_dragon < len(toutes_cases):
            pos = toutes_cases[index_dragon]
            niveau = k + 1  # Niveau croissant : 1, 2, 3...
            dragons.append([pos, niveau])
            index_dragon += 1

    return donjon, aventurier_pos, dragons, nb_tresors


def calculer_indice(donjon, position, dragons):
    """
    Calcule le chemin le plus court vers le dragon de plus BAS niveau,
    en ignorant l'état des portes (comme si toutes étaient ouvertes).


    Paramètres :
        donjon : liste de listes de tuples
        position : tuple (ligne, colonne) - position de l'aventurier
        dragons : liste de [position, niveau]

    Retour :
        liste de tuples : Chemin vers le dragon de plus bas niveau
        None : Si aucun dragon
    """
    if len(dragons) == 0:
        return None

    # Trouver le dragon de plus bas niveau
    dragon_cible = None
    niveau_min = 999

    for d in dragons:
        pos_d, niv_d = d
        if niv_d < niveau_min:
            niveau_min = niv_d
            dragon_cible = pos_d

    if dragon_cible is None:
        return None

    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])

    file = [(position, [position])]
    visites = {position}

    while len(file) > 0:
        pos_actuelle, chemin = file.pop(0)

        # Si on a atteint le dragon cible
        if pos_actuelle == dragon_cible:
            return chemin

        i, j = pos_actuelle

        # Explorer les 4 directions
        directions = [
            (i - 1, j),  # Haut
            (i, j + 1),  # Droite
            (i + 1, j),  # Bas
            (i, j - 1),  # Gauche
        ]

        for nouvelle_pos in directions:
            ni, nj = nouvelle_pos

            # Vérifier que la position est dans le donjon
            if 0 <= ni < nb_lignes and 0 <= nj < nb_colonnes:
                if nouvelle_pos not in visites:
                    visites.add(nouvelle_pos)
                    nouveau_chemin = chemin + [nouvelle_pos]
                    file.append((nouvelle_pos, nouveau_chemin))

    return None
