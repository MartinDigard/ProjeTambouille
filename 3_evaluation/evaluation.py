# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Évalue la performance de notre fonction de reconnaissance d’ingrédients par
rapport à la liste d’ingrédients mentionnés dans la recette avec les mesures de
précision et de rappel.
"""

# Modules
import argparse
from glob import glob
import re


def prepa_eval(balises_ingr, entete_ingr, trouves, corrects):
    """
    Sortie : matrice (vpos, fpos, vneg, fneg)
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


def main():
    """
    Évaluation
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()
    compteur = 0
    for chemin_fichier in glob(args.rep_corpus_final + '/*'):
        nom_fichier = chemin_fichier.split('/')[-1]
        print(f"\n{compteur}\nChemin fichier : "
              f"{chemin_fichier}\tNom du fichier : {nom_fichier}\n")
        compteur += 1
        with open(chemin_fichier) as recette_finale:
            recette = recette_finale.read()

        # Récupérer le contenu des balises ingrédients
        ingredients_corps = re.findall(r'<ingredient[^>]+>(.*?)</ingredient>',
                                       recette)
        ingredients_corps = list(set(ingredients_corps))

        # Récupérer le contenu de la liste d’ingrédients de l’entête
        ingredients_entete = re.findall(r'<p>(.*)</p>', recette)

        # Préparer l’évaluation
        corrects = len(ingredients_entete)
        trouves = len(ingredients_corps)
        vpos, fpos, fneg = prepa_eval(ingredients_corps, ingredients_entete,
                                      trouves, corrects)
        print(f"vpos : {vpos}\nfpos : {fpos}\nfneg : {fneg}\n")

        # Évaluation
        evaluation = Evaluation(vpos, fpos, fneg)
        print(f"Précision : {round(evaluation.precision(), 3)}")
        print(f"Rappel : {round(evaluation.rappel(), 3)}")
        print(f"F-mesure : {round(evaluation.fmesure(), 3)}")

        print("\n**********************************************************\n")


if __name__ == "__main__":

    main()
