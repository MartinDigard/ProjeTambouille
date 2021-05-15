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
import numpy as np
import matplotlib.pyplot as plt

# Modules du projet
import b_evaluation as ev


def recup_temps_espace(recette):
    """
    Calcul le temps et l’espace nécessaires pour une recette.
    """
    tous_les_temps = [float(tps) for tps in re.findall(
                            '<operation temps=(.*?)min', recette)]
    test_espace = re.search('espace=(.*?)>', recette)
    if test_espace:
        espace = test_espace.group(1)
    else:
        espace = 1
    return sum(tous_les_temps), float(espace)


def correlation(liste_de_tuple):
    """
    Calcul corr niveau-temps et niveau-espace.
    """
    niveau = [var[0] for var in liste_de_tuple]
    temps = [var[1] for var in liste_de_tuple]
    espace = [var[2] for var in liste_de_tuple]

    fig, axes = plt.subplots()
    axes.scatter(niveau, temps, label="Temps")
    axes.scatter(niveau, espace, label="Espace")
    axes.set_title("Calcul de corrélation entre le niveau et le temps et l'espace")
    axes.set_xlabel('Temps et espace')
    axes.set_ylabel('Niveau')
    axes.legend()
    plt.savefig('graphiques/correlation.png')

    print("Coefficients de corrélation :")
    print(f"Niveau et temps : {round(np.corrcoef(niveau, temps)[0, 1], 3)}")
    print(f"Niveau et espace : {round(np.corrcoef(niveau, espace)[0, 1], 3)}")
    print("\nLe fichier « correlation.png » a été créé dans le répertoire "
          "« graphiques ».\n")


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
        vpos, fpos, fneg = ev.prepa_eval(ingredients_corps, ingredients_entete,
                                         len(ingredients_corps),
                                         len(ingredients_entete))

        # Préparer les évaluations globales
        liste_valeurs_locales.append((vpos, fpos, fneg))

        # Les niveaux de recettes pour le calcul de corrélation
        niveau = re.search('<niveau>(.*)</niveau>', recette).group(1)

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
            niveau = 4

        axes.append((round(niveau, 3), round(temps_total, 3),
                     round(espace_total, 3)))

    # Calcul de l'évaluation
    ev.evaluation_globale(liste_valeurs_locales)

    # Calcul des corrélations
    correlation(axes)


if __name__ == "__main__":

    main()
