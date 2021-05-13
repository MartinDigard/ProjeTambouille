# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Récupération des ingrédients en récursif.
"""

# Modules
import sys
import argparse
import re
from glob import glob

# Modules du projet
import b_autocuiseur as ac
import c_ingredients as ingred
import d_operations as oper
import e_recipients as recip

# Préparation
sys.setrecursionlimit(10**6)
unites_de_mesure = [' cl ', ' ml ', ' l ', ' dl', 'g ', ' kg ', ' kilogramme ',
                    ' kilogrammes ', ' gramme ', ' grammes ', 'gr ']


def bouteille_a_la_mer(input_file, infos_ingredients, target_file):
    """
    Les cuisiniers envoient une bouteille contenant les infos des ingrédients à
<<<<<<< HEAD
    l’équipe de calcul.
    Écrit un fichier tsv au format (qtt, unité, ingr) dans le répertoire
    « 2_complexite ».
=======
    l'équipe de calcul.
    Écrit un fichier tsv au format (qtt, unite, ingr) dans le répertoire
    "2_complexite".
>>>>>>> e4c7ff0c37bdcbf028f8acffddc5736168a822e7
    """
    infos_ingr_tsv = []
    for qtt, unite, ingr in infos_ingredients:
        infos_ingr_tsv.append(f"{qtt}\t{unite}\t{ingr}")
    infos_ingr_tsv = '\n'.join(infos_ingr_tsv)

    with open(target_file, 'a') as tsv:
        tsv.write(input_file)
        tsv.write('\n')
        tsv.write(infos_ingr_tsv)
        tsv.write('\n\n')


def nettoyage_balises_ope(recette):
    """
<<<<<<< HEAD
    Debug des balises opérations
    """
    recette = re.sub('(<operation>+[^<]*)<operation>([^<]*</operation>)',
=======
    Debug balises opérations, (reloutise 2)
    """
    recette = re.sub('(<operation>[^<]*)<operation>([^<]*</operation>)',
>>>>>>> e4c7ff0c37bdcbf028f8acffddc5736168a822e7
                     '\\1\\2', recette)
    recette = re.sub('(<operation>[^<]*)</operation>([^<]*</operation>)+',
                     '\\1\\2', recette)
    recette = re.sub('<operation><operation>', '<operation>', recette)
    return recette


def main():
    """
    Chaîne de traitement réalisée sur une seule recette.
    """
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus')
    parser.add_argument('corpus_annote')
    args = parser.parse_args()

    # Lecture du corpus
    def read_corpus(file_list, corpus_annote):
        """
        Annotations
        """
        if len(file_list) == 0:
            return 'Fin du traitement.'
        with open(file_list[0]) as input_file:
            print(f"Traitement de la recette {file_list[0]} en cours ...")
            recette = input_file.read()
        recette = ac.ponctuation(recette)

        # Découper la recette
        entete = recette.split('<![CDATA[')[0]
        texte_recette = recette.split('<![CDATA[')[1].split(']]>')[0]
        fin = recette.split('<![CDATA[')[1].split(']]>')[1]

        # Liste des ingrédients de l’entête de la recette
        liste_de_l_entete = ac.liste_entete(entete.split('\n'))

        # Liste de tuple au format (quantité, unité, nom_de_l_ingrédient)
        infos_ingredients = ingred.liste_ingredients(liste_de_l_entete,
                                                     unites_de_mesure)

        # Écriture des infos ingrédients dans le répertoire complexité
        bouteille_a_la_mer(file_list[0], infos_ingredients,
                           '../2_complexite/z_infos_ingredients.tsv')

        liste_ingredients = ingred.create_ingr_list(infos_ingredients)

        # Annotation des ingrédients
        recette_annotee = ingred.annotation(texte_recette, liste_ingredients)
        recette_annotee = re.sub('</ingredient> <ingredient>', ' ',
                                 ' '.join(recette_annotee))

        # Annotation des opérations
        recette_annotee = oper.annotation(recette_annotee)

        # Annotation des récipients
        recette_annotee = recip.annotation(recette_annotee)
        recette_annotee = re.sub('</recipient> <recipient>', ' ',
                                 recette_annotee)

<<<<<<< HEAD
        # Debug annotations
=======
        # Debug annotation
>>>>>>> e4c7ff0c37bdcbf028f8acffddc5736168a822e7
        recette_annotee = nettoyage_balises_ope(recette_annotee)

        # Recoller le recette
        entete = ac.recoller(entete)
        recette_annotee = ac.recoller(recette_annotee)
        final = entete + '<![CDATA[\n' + recette_annotee + '\n]]>' + fin

        # Écriture corpus annoté
        new_file = corpus_annote + file_list[0].split('/')[-1]
        with open(new_file, 'w') as corpus_ann:
            corpus_ann.write(final)

        return read_corpus(file_list[1:], corpus_annote)

    corpus = glob(args.corpus + '*')
    read_corpus(corpus, args.corpus_annote)


if __name__ == "__main__":

    main()
