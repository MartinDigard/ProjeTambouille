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
<<<<<<< HEAD
=======
from pprint import pprint
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
import numpy as np
import matplotlib.pyplot as plt

# Modules du projet
import evaluation as ev


def recup_temps_espace(recette):
<<<<<<< HEAD
    """
    Calcul le temps total nécessaire pour une recette.
    """
=======
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
    tous_les_temps = [float(tps) for tps in re.findall('<operation temps=(.*?)min', recette)]
    test_espace = re.search('espace=(.*?)>', recette)
    if test_espace:
        espace = test_espace.group(1)
    else:
        espace = 1
    return sum(tous_les_temps), float(espace)


def correlation(liste_de_tuple):
    """
<<<<<<< HEAD
=======
    Calcul corr niveau-temps et niveau-espace.
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
    """
    niveau = [var[0] for var in liste_de_tuple]
    temps = [var[1] for var in liste_de_tuple]
    espace = [var[2] for var in liste_de_tuple]
<<<<<<< HEAD

    plt.scatter(niveau, temps)
    plt.title("Calcul de corrélation entre le niveau et le temps")
    plt.xlabel('temps')
    plt.ylabel('niveau')
    plt.show()

    plt.scatter(niveau, espace)
    plt.title("Calcul de corrélation entre le niveau et le temps")
    plt.xlabel('espace')
    plt.ylabel('niveau')
    plt.show()

    print(np.corrcoef(niveau, temps)[0,1])
    print(np.corrcoef(niveau, espace)[0,1])

    plt.title("Calcul de corrélation")

=======
    for elt1, elt2, elt3 in zip(niveau, temps, espace):
        print(f"{elt1}\t{elt2}\t{elt3}")
    print(np.corrcoef(niveau, temps)[0,1])
    print(np.corrcoef(niveau, espace)[0,1])

    plt.bar(niveau, temps) 
    plt.show()

    plt.bar(niveau, espace) 
    plt.show()
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b


def main():
    """
    Évaluation et corrélation.
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()
    liste_valeurs_locales = []
    axes = []
<<<<<<< HEAD

=======
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
    for chemin_fichier in glob(args.rep_corpus_final + '/*'):
        with open(chemin_fichier) as recette_finale:
            recette = recette_finale.read()
        print(chemin_fichier)
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

        # Les niveaux de recettes pour le calcul de corrélation
        niveau = re.search('<niveau>(.*)</niveau>', recette).group(1)
<<<<<<< HEAD
        print(niveau)

        # Additionner les temps
        temps_total, espace_total = recup_temps_espace(recette)

        # Préparation du tuple
        if niveau == "Très facile":
            niveau = 1
        if niveau == "Facile":
            niveau = 2
        if niveau == "Moyennement difficile":
            niveau = 3
        if niveau == "Difficile":
=======

        # Additionner les temps
        temps_total, espace_total = recup_temps_espace(recette) 

        # Préparation du tuple
        if niveau == 'Très facile':
            niveau = 1
        if niveau == 'Facile':
            niveau = 2
        if niveau == 'Moyennement difficile':
            niveau = 3
        if niveau == 'Difficile':
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
            niveau = 4

        axes.append((round(niveau, 3), round(temps_total, 3),
                     round(espace_total, 3)))

<<<<<<< HEAD
    # Calcul de l'évaluation
=======
    # Calcul de évaluation
>>>>>>> 5646c905d8d31368081436ea76894ab2b0ecec4b
    ev.evaluation_globale(liste_valeurs_locales)

    # Calcul des corrélations
    correlation(axes)


if __name__ == "__main__":

    main()
