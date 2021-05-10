# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Attributs « quantite » pour les balises ingrédients.
"""

import re


def annot_espace_temps(recette, oper_temps, nb_recipients):
    return recette


def decompte_annotation(recette):
    """
    Sortie : Un tuple au format (nb_ingr, nb_oper, nb_recip)
    """
    operations = re.findall('<operation>.*?</operation>', recette)
    recipients = re.findall('<recipient>.*?</recipient>', recette)
    return operations, recipients


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
