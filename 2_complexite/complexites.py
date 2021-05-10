# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Calculer la complexité en temps et en espace.
"""

import os
import matplotlib.pyplot as plt
from scipy import stats
import argparse
import glob
import re

recettes_problematiques = []


def decompte_annotation(recette):
    """
    Sortie : Un tuple au format (nb_ingr, nb_oper, nb_recip)
    """
    operations = re.findall('<operation>.*?</operation>', recette)
    recipients = re.findall('<recipient>.*?</recipient>', recette)
    return operations, recipients


def nettoyage_qtt(qtt, unite):
    """
    Nettoyage qtt
    """
    qtt_ingr = 0
    if unite == 'null' and qtt != "null":
        if ' ' in qtt:
            nb1, nb2 = qtt.split(' ')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1 + nb2)
        if "+" in str(qtt):
            nb1, nb2 = qtt.split('+')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) + float(nb2)
        if "/" in str(qtt):
            nb1, nb2 = qtt.split('/')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) / float(nb2)
        if "\\" in str(qtt):
            nb1, nb2 = qtt.split('\\')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) / float(nb2)
        if ("x" or "X") in str(qtt):
            nb1, nb2 = qtt.lower().split('x')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) * float(nb2)
        if "-" in str(qtt):
            nb1, nb2 = qtt.split('-')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) + float(nb2) / 2
        if "à" in str(qtt):
            nb1, nb2 = qtt.split('à')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) + float(nb2) / 2
        if "|" in str(qtt):
            nb1, nb2 = qtt.split('|')
            if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                qtt = float(nb1) + float(nb2) / 2
        if not re.search(r'^[0-9]+(.[0-9]+)?$', str(qtt)):
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
        if len(infos_ingr[0].split('\t')) < 3:
            return annotation_qtt(infos_ingr[1:])
        qtt, unite, ingr = infos_ingr[0].split('\t')
        qtt = nettoyage_qtt(qtt, unite)
        if float(int(qtt)) != float(qtt): 
            qtt = int(qtt) + 1
        else:
            qtt = int(qtt)
        for elt in re.findall('<ingredient>[^<]+</ingredient>', recette):
            elt = re.sub('<ingredient>([^<]+)</ingredient>', '\\1', elt)
            if elt == ingr:
                recette = re.sub(f'<ingredient>([^<]*{ingr}[^<]*)</ingredient>',
                                 f'<ingredient quantite={qtt}>\\1</ingredient>',
                                 recette)
        return annotation_qtt(recette, infos_ingr[1:])
    return recette

        # ingr_recette = re.search(f'<ingredient>([^<]*{ingr}[^<]*)</ingredient>', recette)
        # if ingr_recette:
        #     ingr_recette = ingr_recette.group(1)
        #     if ingr_recette in ingr and ingr_recette != ingr:
        #         print(f"ingr_recette({ingr_recette}) est dans ingr({ingr})")
        #     if ingr in ingr_recette and ingr_recette != ingr:
        #         print(f"ingr({ingr}) est dans ingr_recette({ingr_recette})")




def decompte_ingredients(infos_ingr, nb_ingr):
    """
    Renvoie le nombre total d'ingrédients pour une recette
    """
    if len(infos_ingr) != 0:
        if len(infos_ingr[0].split('\t')) > 3:
            return decompte_ingredients(infos_ingr[1:], nb_ingr)
        qtt, unite, _ = infos_ingr[0].split('\t')
        if unite == 'null' and qtt != "null":
            if ' ' in qtt:
                nb1, nb2 = qtt.split(' ')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1 + nb2)
            if "+" in str(qtt):
                nb1, nb2 = qtt.split('+')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) + float(nb2)
            if "/" in str(qtt):
                nb1, nb2 = qtt.split('/')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) / float(nb2)
            if "\\" in str(qtt):
                nb1, nb2 = qtt.split('\\')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) / float(nb2)
            if ("x" or "X") in str(qtt):
                nb1, nb2 = qtt.lower().split('x')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) * float(nb2)
            if "-" in str(qtt):
                nb1, nb2 = qtt.split('-')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) + float(nb2) / 2
            if "à" in str(qtt):
                nb1, nb2 = qtt.split('à')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) + float(nb2) / 2
            if "|" in str(qtt):
                nb1, nb2 = qtt.split('|')
                if re.search(r'^[0-9]+$', nb1) and re.search(r'^[0-9]+$', nb2):
                    qtt = float(nb1) + float(nb2) / 2
            if not re.search(r'^[0-9]+(.[0-9]+)?$', str(qtt)):
                nb_ingr += 1
            else:
                if float(qtt) < 10:
                    nb_ingr += float(qtt)
                else:
                    nb_ingr += 1
        else:
            nb_ingr += 1.
        return decompte_ingredients(infos_ingr[1:], nb_ingr)
    return nb_ingr


def temps(operations, refs_tps, oper_temps=None):
    """
    Pour chaque opération : définir son temps unitaire
    Pour chaque ingrédient de l’opération : faire la somme de leur qtt
    Calculer le produit de cette somme et du temps unitaire.
    somme(nb_unité(ingr) for ingr in opération) * temps unitaire
    """
    if oper_temps is None:
        oper_temps = []
    if len(operations) != 0:
        oper = operations[0]

        def reference_temps(refs_tps):
            if len(refs_tps) != 0:
                ref = refs_tps[0]
                if re.search('[0-9]+ (minute(s)?|min|mn)( |<)', oper):
                    tps = re.search('([0-9]+) (minute(s)?|min|mn)( |<)',
                                    oper).group(1)
                    oper_temps.append((oper, float(tps)))
                    return oper_temps
                if ref[0] == oper:
                    oper_temps.append((oper, float(ref[1].split()[0])))
                    return oper_temps
                return reference_temps(refs_tps[1:])
            oper_temps.append((oper, 6.86))
            return oper_temps

        oper_temps = reference_temps(refs_tps)
        return temps(operations[1:], refs_tps, oper_temps)
    return oper_temps


def main():
    """Documentation"""
    parser = argparse.ArgumentParser()
    parser.add_argument('rep_corpus_annote')
    args = parser.parse_args()

    with open('z_temps_operations.tsv') as ref_temps:
        ref_temps = ref_temps.read().split('\n')

    refs_tps = []
    for ref in ref_temps:
        if len(ref) >= 3:
            ope, tps = ref.split('\t')[1:]
            refs_tps.append((ope, tps))

    nb_ingr_oper_all = []
    compteur = 0
    # if os.path.exists('recettes_problematiques'):
    #     os.remove('recettes_problematiques')
    for fichier in glob.glob(args.rep_corpus_annote + '*/*'):
        print(f"\n\n==> {compteur}\nTraitement de la recette {fichier} en cours…\n")
        compteur += 1
        if compteur > 100:
            break
        with open(fichier) as input_file:
            recette_annotee = input_file.read()

        # Récupération des annotations en listes.
        prepa_complexite = decompte_annotation(recette_annotee)
        with open('z_infos_ingredients.tsv') as infos_ingr:
            infos_ingredients = infos_ingr.read().split('\n\n')

        # Dico contenant clés : les noms de fichier, valeurs : les nb_ingr
        infos_ingr = {}
        for block in infos_ingredients:
            nom = block.split('\n')[0].split('/')[-1]
            ingr = block.split('\n')[1:]
            infos_ingr[nom] = ingr

        # for k,v in infos_ingr.items():
        #     print(k)
        #     for elt in v:
        #         print(elt)
        #     print()

        # Nom du fichier pour la lecture de la clef du dico
        fichier = fichier.split('/')[-1]

        # Annotation des balises ingrédients
        qtt_annotee = annotation_qtt(recette_annotee, infos_ingr[fichier])
        print(qtt_annotee)
        
        qtt_ingredients = decompte_ingredients(infos_ingr[fichier], 0)

        nb_ingredients = len(infos_ingr[fichier])

        if nb_ingredients > 20:
            recettes_problematiques.append((fichier, nb_ingredients))
        #     continue
        
        # print(f"Nombre d’ingrédients : {nb_ingredients}")


        # L’association du temps aux opérations
        oper_temps = temps(prepa_complexite[0], refs_tps)
        # for elt in oper_temps:
        #     print(elt)

        # print(f"Nombre d’opérations de base : {len(oper_temps)}")
        
        nb_recipients = len(prepa_complexite[1]) + len(infos_ingr[fichier])
        # print(f"Nombre total de récipients pour cette recette : {nb_recipients}\n\n")

        # with open('recettes_problematiques', 'a') as rp:
        #     rp.write(f"{fichier}\ningr : {nb_ingredients}\noper : {len(oper_temps)}\nrecip : {nb_recipients}\n\n")

        nb_ingr_oper_all.append((nb_ingredients, len(oper_temps)))

if __name__ == "__main__":

    main()


###############################################################################


# Calcul du temps de recettes
# somme = sum([tps for ope, tps in oper_temps])
# moyenne = 0
# if len(oper_temps) != 0:
#     moyenne = somme / len(oper_temps)


# print("Durée de préparation :")
# print(("\t- Par somme des temps des chaque opérations : "),
#       (f"{round(somme, 2)}"))
# print("\t- Complexité en temps : ???\n")
# print()

# # Stockage de tous les nombres
#     nb_ingr_oper_all.append((len(prepa_complexite[0]),
#                              len(prepa_complexite[1])))
# moyenne_ingr_all = sum(
#         [elt[0] for elt in nb_ingr_oper_all]) / len(nb_ingr_oper_all)
# moyenne_oper_all = sum(
#         [elt[1] for elt in nb_ingr_oper_all]) / len(nb_ingr_oper_all)
# print(f"\n{moyenne_ingr_all}")
# print(moyenne_oper_all)
    # # HYPOTHÈSE DE LINÉARITÉ

    # # Générer les axes
    # x = [elt[0] for elt in nb_ingr_oper_all]
    # y = [elt[1] for elt in nb_ingr_oper_all]

    # # Dessiner un nuage de points
    # plt.scatter(x, y)
    # plt.show()

    # # Dessiner la ligne de régression linéaire
    # slope, intercept, r, p, std_err = stats.linregress(x, y)

    # def myfunc(x_axis):
    #     """ Calcul de la régression linéaire ?? """
    #     return slope * x_axis + intercept

    # mymodel = list(map(myfunc, x))
    # plt.scatter(x, y)
    # plt.plot(x, mymodel)
    # plt.show()

    # print(f"stp_err : {std_err}")
    # print(f"r : {r}")
