from fltk import cree_fenetre, ferme_fenetre
from graphique import (
    afficher_menu,
    afficher_donjon_fenetre,
    editeur_donjon,
    lancer_niveau_aleatoire,
)
from moteur import charger_niveau_complet, charger_partie

cree_fenetre(1248, 832)

# Boucle principale du programme
while True:
    choix = afficher_menu()

    if choix == "quit":
        break

    elif choix == "facile":
        donjon, aventurier, dragons, nb_tresors = charger_niveau_complet(
            "donjon_facile.txt"
        )
        resultat = afficher_donjon_fenetre(
            donjon, aventurier, dragons, nb_tresors, None
        )

        if resultat != "menu":
            break

    elif choix == "durt":
        donjon, aventurier, dragons, nb_tresors = charger_niveau_complet(
            "donjon_durt.txt"
        )
        resultat = afficher_donjon_fenetre(
            donjon, aventurier, dragons, nb_tresors, None
        )

        if resultat != "menu":
            break

    elif choix == "charger":
        resultat_chargement = charger_partie()

        if resultat_chargement[0] is not None:
            donjon, aventurier, dragons, tresors_restants, pos_tresor_initial = (
                resultat_chargement
            )
            print("Partie chargée depuis sauvegarde.txt")
            resultat = afficher_donjon_fenetre(
                donjon, aventurier, dragons, tresors_restants, pos_tresor_initial
            )

            if resultat != "menu":
                break

    elif choix == "editeur":
        resultat = editeur_donjon()
        # Continue automatiquement au menu

    elif choix == "generateur":
        # Générer et lancer un niveau aléatoire
        donjon, aventurier, dragons, nb_tresors = lancer_niveau_aleatoire()
        resultat = afficher_donjon_fenetre(
            donjon, aventurier, dragons, nb_tresors, None
        )

        if resultat != "menu":
            break
        # Si resultat == "menu", la boucle continue et réaffiche le menu

    else:
        break

ferme_fenetre()
