from fltk import *

cree_fenetre(100, 100)
i = 0
while i < 10:
    ev = donne_ev()
    if ev:
        t = type_ev(ev)
        print(type_ev(ev))
ferme_fenetre()
