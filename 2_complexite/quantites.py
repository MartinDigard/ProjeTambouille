# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Attributs « quantite » pour les balises ingrédients.
"""

import re


def moyenne_qtt(signe, qtt):
    """
<<<<<<< HEAD
    Fait les moyennes.
=======
    Fait les moyennes
>>>>>>> 08f4e3999013315e7ea696389c8b9bc1215bdae6
    """
    nb1, nb2 = qtt.split(signe)
    if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
        qtt = float(nb1) + float(nb2) / 2
    return qtt


def division_qtt(signe, qtt):
    """
<<<<<<< HEAD
    Fait les divisions.
=======
    Fait les divisions
>>>>>>> 08f4e3999013315e7ea696389c8b9bc1215bdae6
    """
    nb1, nb2 = qtt.split(signe)
    if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
        qtt = float(nb1) / float(nb2)
    return qtt


def conc_add(qtt):
    """
<<<<<<< HEAD
    Concatène ou additionne en focntion du contexte
=======
    Concatène ou additionne en fonction du contexte
>>>>>>> 08f4e3999013315e7ea696389c8b9bc1215bdae6
    """
    if ' ' in qtt:
        nb1, nb2 = qtt.split(' ')
        if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
            qtt = float(nb1 + nb2)
    if "+" in str(qtt):
        nb1, nb2 = qtt.split('+')
        if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
            qtt = float(nb1) + float(nb2)
    return qtt


def nettoyage_qtt(qtt, unite):
    """
    Nettoyage qtt
    """
    qtt_ingr = 0
    if unite == 'null' and qtt != "null":
<<<<<<< HEAD
        # Concaténation et addition
        if re.search(r" |\+", str(qtt)):
            qtt = conc_add(qtt)

        # Mutliplication
=======

        # concaténation et addition
        if re.search(r' |\+', str(qtt)):
            print(qtt)
            qtt = conc_add(qtt)

        # multiplications
>>>>>>> 08f4e3999013315e7ea696389c8b9bc1215bdae6
        if ("x" or "X") in str(qtt):
            nb1, nb2 = qtt.lower().split('x')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) * float(nb2)

<<<<<<< HEAD
        # Division
        if re.search(r"/|\\", str(qtt)):
            symbole = re.sub(r'[^/\\]', '', str(qtt))
            qtt = division_qtt(symbole, qtt)

        # Moyenne
        if re.search(r"-|à|\|", str(qtt)):
            symbole = re.sub('[^-à|]', '', str(qtt))
=======
        # divisions
        if re.search(r"/|\\", str(qtt)):
            symbole = re.sub(r'([^/\\])', '', str(qtt))
            qtt = division_qtt(symbole, qtt)

        # moyennes
        if re.search(r"-|à|\|", str(qtt)):
            symbole = re.sub('([^-à|])', '', str(qtt))
>>>>>>> 08f4e3999013315e7ea696389c8b9bc1215bdae6
            qtt = moyenne_qtt(symbole, qtt)

        # Un ingrédient liquide, en poudre ou inconnu est égal à 1 unité
        if not re.search(r'^[0-9]+(\.[0-9]+)?$', str(qtt)):
            qtt_ingr += 1
        else:
            if float(qtt) < 10:
                qtt_ingr += float(qtt)
            else:
                qtt_ingr += 1
    else:
        qtt_ingr += 1.
    return qtt_ingr


def annotation_qtt(recette, infos_ingr):
    """
    Nettoyage et annotation des qtt dans les balises ingrédients.
    """
    if len(infos_ingr) != 0:
        if len(infos_ingr[0].split('\t')) != 3:
            return annotation_qtt(recette, infos_ingr[1:])
        qtt, unite, ingr = infos_ingr[0].split('\t')
        qtt = nettoyage_qtt(qtt, unite)
        if float(int(qtt)) != float(qtt):
            qtt = int(qtt) + 1
        else:
            qtt = int(qtt)

        for token in ingr.split():
            if len(token) > 2 and "/" not in token:
                recette = re.sub(f'<ingredient>([^<]*{token}[^<]*)'
                                 '</ingredient>',
                                 f'<ingredient quantite={qtt}>\\1'
                                 '</ingredient>',
                                 recette)
        return annotation_qtt(recette, infos_ingr[1:])
    recette = re.sub('<ingredient>', '<ingredient quantite=1>', recette)
    return recette
