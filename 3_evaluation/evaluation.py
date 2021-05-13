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


def prepa_eval(balises_ingr, entete_ingr):
    """
    Sortie : matrice (vpos, fp, vn, fn)
    """
    return "matrice"


class Evaluation:
    """
    eee
    """

    def __init__(self, matrice):
        self.matrice = matrice

    def rappel(self, row):
        "Mesure le taux de vrais positifs."
        rappel = 0
        for elt in self.matrice:
            if elt['categories'] == row:
                vpos, fneg = int(elt['vrais positifs']), int(
                                 elt['faux négatifs'])
                rappel = vpos / (vpos + fneg)
        return rappel

    def precision(self, row):
        """
        Mesure le nombre d’éléments correctement étiquetés en tant que
        « vrais positifs ».
        """
        precision = 0
        for elt in self.matrice:
            if elt['categories'] == row:
                vpos, fpos = int(elt['vrais positifs']), int(
                                 elt['faux positifs'])
                precision = vpos / (vpos + fpos)
        return precision

    def fmesure(self, row):
        """
        Moyenne harmonique pondérée du rappel et de la précision.
        Ici, ß=1.
        """
        fmesure = 0
        precision = 0
        rappel = 0
        for elt in self.matrice:
            if elt['categories'] == row:
                fmesure = (2 * self.precision(row) * self.rappel(row)) / (
                      self.precision(row) + self.rappel(row))
        return fmesure


def main():
    """
    Évaluation
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()

    for chemin_fichier in glob(args.rep_corpus_final + '/*'):
        nom_fichier = chemin_fichier.split('/')[-1]
        print(f"\nChemin fichier : "
              f"{chemin_fichier}\tNom du fichier : {nom_fichier}\n")
        with open(chemin_fichier) as recette_finale:
            recette = recette_finale.read()

        # Découper la recette
        entete_recette = recette.split('<![CDATA[')[0]
        corps_recette = recette.split('<![CDATA[')[1].split(']]>')[0]

        # Récupérer le contenu des balises ingrédients
        ingredients_corps = re.findall(r'<ingredient[^>]+>.*?</ingredient>',
                                       corps_recette)
        ingredients_corps = set(ingredients_corps)
        for balises in ingredients_corps:
            print(balises)

        # Récupérer le contenu de la liste d’ingrédients de l’entête
        ingredients_entete = re.findall(r'<p>(.*)</p>', entete_recette)
        print()
        for balises in ingredients_entete:
            print(balises)
        print("\n**********************************************************\n")


if __name__ == "__main__":

    main()
