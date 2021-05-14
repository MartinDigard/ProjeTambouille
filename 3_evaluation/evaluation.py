# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Évalue la performance de la fonction de reconnaissance d’ingrédients par
rapport à la liste d’ingrédients mentionnés dans la recette avec les mesures de
précision et de rappel.
"""


def prepa_eval(balises_ingr, entete_ingr, trouves, corrects):
    """
    Sortie : matrice (vpos, fpos, fneg)
    """
    if len(balises_ingr) != 0:
        ingredient_balises = balises_ingr[0].lower()

        def lire_entete(liste_entete, nouvelle_liste=None):
            if nouvelle_liste is None:
                nouvelle_liste = []
            if len(liste_entete) != 0:
                ingredient_entete = liste_entete[0].lower()
                if ingredient_balises in ingredient_entete:
                    return lire_entete(liste_entete[1:], nouvelle_liste)
                nouvelle_liste.append(ingredient_entete)
                return lire_entete(liste_entete[1:], nouvelle_liste)
            return nouvelle_liste
        entete_ingr = lire_entete(entete_ingr)
        return prepa_eval(balises_ingr[1:], entete_ingr, trouves, corrects)
    fneg = len(entete_ingr)
    vpos = corrects - fneg
    fpos = trouves - vpos
    return vpos, fpos, fneg


class Evaluation:
    """
    Classe dédiée aux calculs de précision, rappel et f-mesure.
    """

    def __init__(self, vpos, fpos, fneg):
        self.vpos = vpos
        self.fpos = fpos
        self.fneg = fneg

    def precision(self):
        """
        Mesure le nombre d’éléments correctement étiquetés en tant que
        « vrais positifs ».
        """
        precision = 0
        if self.vpos != 0:
            precision = self.vpos / (self.vpos + self.fpos)
        return precision

    def rappel(self):
        "Mesure le taux de vrais positifs."
        rappel = 0
        rappel = self.vpos / (self.vpos + self.fneg)
        return rappel

    def fmesure(self):
        """
        Moyenne harmonique pondérée du rappel et de la précision.
        Ici, ß=1.
        """
        fmesure = 0
        if (self.precision() and self.rappel()) != 0:
            fmesure = (2 * self.precision() * self.rappel()) / (
                       self.precision() + self.rappel())
        return fmesure


def evaluation_globale(liste_valeurs_locales):
    """
    Calcul et affichage de l'évaluation globale
    """
    # Calcul à partir des valeurs totales récupérées dans les tuples locaux
    vpos_total = sum([val[0] for val in liste_valeurs_locales])
    fpos_total = sum([val[1] for val in liste_valeurs_locales])
    fneg_total = sum([val[2] for val in liste_valeurs_locales])

    print(f"\nvpos_total : {vpos_total}\nfpos_total : {fpos_total}\n"
          f"fneg_total : {fneg_total}\n")

    # Évaluation globale à partir des valeurs vpos/fpos/fneg
    evaluation = Evaluation(vpos_total, fpos_total, fneg_total)
    print(f"Précision : {round(evaluation.precision(), 3)}")
    print(f"Rappel : {round(evaluation.rappel(), 3)}")
    print(f"F-mesure : {round(evaluation.fmesure(), 3)}\n")
