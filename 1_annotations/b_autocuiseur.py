# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Module d’annotation des opérations.
"""

import re


def ponctuation(chaine):
    """Normalise la ponctuation sans déformer le xml."""
    chaine = re.sub(r'(\D)(\.)(\D)', '\\1 \\2 \\3', chaine)
    chaine = re.sub(r'([,:\(\)])', ' \\1 ', chaine)
    chaine = re.sub(r'\'', '’', chaine)
    chaine = re.sub(r'’', '’ ', chaine)
    chaine = re.sub(r'([^<])(!)([^\[CDATA\[])', '\\1 \\2 \\3', chaine)
    chaine = re.sub(r' +', ' ', chaine)
    return chaine


def liste_entete(recette, liste=None):
    """
    Génération de la liste.
    """
    if liste is None:
        liste = []
    if len(recette) != 0:
        line = recette[0]
        if re.search('<p>(.*)</p>', line):
            phrase_ingredients = re.search('<p>(.*)</p>', line).group(1)
            phrase_ingredients = re.sub(r'\(.*\)', '',
                                        phrase_ingredients).strip()
            liste.append(phrase_ingredients)
        return liste_entete(recette[1:], liste)
    return liste


def recoller(texte):
    """
    Recoller le texte.
    """
    texte = re.sub(' ’', '’', texte)
    texte = re.sub(r' \.', '.', texte)
    texte = re.sub(r' ([,!:])', '\\1', texte)
    texte = re.sub(r'\( ', '(', texte)
    texte = re.sub(r' \)', ')', texte)
    texte = texte.strip()
    texte = re.sub('<preparation>', '<preparation>\n', texte)
    return texte
