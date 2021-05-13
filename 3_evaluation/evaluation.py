# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Évalue la performance de votre fonction de reconnaissance d’ingrédients par
rapport à la liste d’ingrédients mentionné dans la recette avec les mesures de
précision et de rappel.
"""

# Modules
import argparse


def main():
    """
    Évaluation
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()


if __name__ == "__main__":

    main()
