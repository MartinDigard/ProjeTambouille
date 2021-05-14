# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Programme principal de ce répertoire :
- Évaluation de la performance de la fonction de reconnaissance d’ingrédients.
- Corrélation entre les niveaux de difficulté et de complexité de chaque
  recette.
"""

# Modules
import argparse
from glob import glob
import re

# Modules du projet
import evaluation as ev


def main():
    """
    Évaluation et corrélation.
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()
    liste_valeurs_locales = []
    for chemin_fichier in glob(args.rep_corpus_final + '/*'):
        with open(chemin_fichier) as recette_finale:
            recette = recette_finale.read()

        # Récupérer le contenu des balises ingrédients
        ingredients_corps = re.findall(r'<ingredient[^>]+>(.*?)</ingredient>',
                                       recette)
        ingredients_corps = list(set(ingredients_corps))

        # Récupérer le contenu de la liste d’ingrédients de l’entête
        ingredients_entete = re.findall(r'<p>(.*)</p>', recette)

        # Préparer les évaluations locales
        corrects = len(ingredients_entete)
        trouves = len(ingredients_corps)
        vpos, fpos, fneg = ev.prepa_eval(ingredients_corps, ingredients_entete,
                                         trouves, corrects)

        # Préparer les évaluations globales
        liste_valeurs_locales.append((vpos, fpos, fneg))

    ev.evaluation_globale(liste_valeurs_locales)


if __name__ == "__main__":

    main()
