# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Module d’annotation des récipients.
"""

import re

with open('z_lexique_recipients') as lex:
    lexique = lex.read().strip().split('\n')


def detect_recipients(texte, recipients):
    """
    Détection des récipients.
    """
    if len(recipients) != 0:
        recipient = recipients[0]
        texte = re.sub(fr'\b{recipient}\b',
                       f"<recipient>{recipient}</recipient>", texte)
        return detect_recipients(texte, recipients[1:])
    return texte


def annotation(texte):
    """
    Annotation générale.
    """
    recette_annotee = detect_recipients(texte, lexique)
    return recette_annotee
