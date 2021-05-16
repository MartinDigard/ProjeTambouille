# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Test de fonctions imbriquées
"""
alpha = ['a', 'b', 'c', 'd']
num = [1, 2, 3, 4]


def alpha_num(liste1, liste2):
    """Lire des chiffres et des lettres"""
    if len(liste1) != 0:
        letter = liste1[0]

        def lire_nb(liste2):
            if len(liste2) != 0:
                number = liste2[0]
                print(f"{letter} : {number}")
                return lire_nb(liste2[1:])
            return 0
        lire_nb(liste2)
        return alpha_num(liste1[1:], liste2)
    return 0


alpha_num(alpha, num)
