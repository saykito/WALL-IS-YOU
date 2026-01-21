# sauvegarde.py
import json

NOM_FICHIER_SAUVEGARDE = "sauvegarde.json"


def sauver_partie(donjon, aventurier, dragons, mode):
    """
    Sauvegarde la partie dans un fichier JSON.
    - donjon : liste de listes de salles (tuples de 4 booléens)
    - aventurier : [ (i, j), niveau ]
    - dragons : [ [(i, j), niveau], ... ]
    - mode : "facile" ou "durt"
    """

    data = {
        "mode": mode,
        "donjon": donjon,
        "aventurier": aventurier,
        "dragons": dragons,
    }

    with open(NOM_FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def charger_partie():
    """
    Charge la partie depuis le fichier JSON.
    Retourne (mode, donjon, aventurier, dragons) ou None s'il n'y a pas de fichier.
    """

    try:
        with open(NOM_FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None

    mode = data["mode"]

    # donjon : on reconvertit les salles en tuples (haut, droite, bas, gauche)
    donjon_liste = data["donjon"]
    donjon = []
    for ligne in donjon_liste:
        nouvelle_ligne = []
        for salle in ligne:
            nouvelle_ligne.append(tuple(salle))
        donjon.append(nouvelle_ligne)

    # aventurier : [ [i, j], niveau ] -> [ (i, j), niveau ]
    pos_av_liste, niveau_av = data["aventurier"]
    aventurier = [tuple(pos_av_liste), niveau_av]

    # dragons : [ [[i, j], niveau], ... ] -> [ [(i,j), niveau], ... ]
    dragons_liste = data["dragons"]
    dragons = []
    for dr in dragons_liste:
        pos, niv = dr
        dragons.append([tuple(pos), niv])

    return mode, donjon, aventurier, dragons
