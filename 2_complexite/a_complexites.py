# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Calculer la complexité en temps et en espace.
"""

# Modules
import re
import argparse
import glob

# Modules du projet
import b_espace_temps as et
import c_quantites as qt


def recup_temps(fichier_ref):
    """
    Récupère le temps.
    """
    with open(fichier_ref) as ref_temps:
        ref_temps = ref_temps.read().split('\n')
    refs_tps = []
    for ref in ref_temps:
        if len(ref) >= 3:
            ope, tps = ref.split('\t')[1:]
            refs_tps.append((ope, tps))
    return refs_tps


def recup_ingr(fichier_ingr):
    """
    Récupère les infos des ingrédients.
    """
    with open(fichier_ingr) as infos_ingr:
        infos_ingredients = infos_ingr.read().split('\n\n')
    infos_ingr = {}
    for block in infos_ingredients:
        nom = block.split('\n')[0].split('/')[-1]
        ingr = block.split('\n')[1:]
        infos_ingr[nom] = ingr
    return infos_ingr


def main():
    """
    - Arguments
    - Fichiers ref
    - Tests
    - Calcul des complexités
    - Ajouts des attributs aux balises
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_annote')
    parser.add_argument('rep_corpus_final')
    args = parser.parse_args()

    # Fichier de références temps-opération et quantité-ingrédient
    refs_tps = recup_temps('z_temps_operations.tsv')
    infos_ingr = recup_ingr('z_infos_ingredients.tsv')

    # Lecture des recettes annotées sans attributs
    compteur = 0
    for fichier in glob.glob(args.rep_corpus_annote + '*/*'):
        print(f'\n\n==> {compteur}\nTraitement de la recette {fichier} en '
              'cours…\n')

        # Limitation pour les tests
        compteur += 1

        # Lecture de la recette courante
        with open(fichier) as input_file:
            recette_annotee = input_file.read()

        # Nom du fichier pour la lecture de la clef du dico
        fichier = fichier.split('/')[-1]

        # Annotation des balises ingrédients
        recette_annotee = qt.annotation_qtt(recette_annotee,
                                            infos_ingr[fichier])

        # Récupération des annotations en listes.
        prepa_complexite = et.decompte_annotation(recette_annotee)

        # Récupération des annotations en listes.
        prepa_complexite = et.decompte_annotation(recette_annotee)

        # Calcul de la complexité en temps
        oper_temps = et.temps(prepa_complexite[0], refs_tps)

        # Calcul de la complexité en espace
        nb_recipients = len(prepa_complexite[1]) + len(infos_ingr[fichier])

        # Annotation du temps et de l’espace
        recette = et.annot_espace_temps(recette_annotee, oper_temps,
                                        nb_recipients)

        # Debug annotation opération (reloutise 3 hé hé)
        recette = re.sub('(<operation[^>]+>.*?)</ingredient>(.*?)<operation>'
                         '(.*?</operation>)', '\\1\\2\\3', recette)

        # Écriture du corpus final
        with open(f"{args.rep_corpus_final}/{fichier}", 'w') as recette_finale:
            recette_finale.write(recette)


if __name__ == "__main__":

    main()
