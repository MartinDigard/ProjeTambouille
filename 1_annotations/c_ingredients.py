# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Module d’annotation des ingrédients.
"""

import re
import spacy
nlp = spacy.load('fr_core_news_sm')


def reloutise(ligne, unite):
    """
    Corrige les trucs relous qui ont un '+'.
    """
    if unite in ligne:
        quantite = ligne.split(unite)[0]
        ingr = ligne.split(unite)[1].strip()
    else:
        quantite = ligne.split()[0]
        ingr = ' '.join(ligne.split()[1:]).strip()
    if re.search('[0-9]+', ligne.split()[0]):
        resultat = (quantite, unite, ingr)
    elif re.search('un|une', ligne.split()[0]):
        resultat = ("1", unite, ingr)
    else:
        resultat = (quantite, unite, ingr)
    return resultat


def liste_ingredients(liste_ingr, unites, orga_entete=None):
    """
    Isolement ingrédients.
    """
    if orga_entete is None:
        orga_entete = []
    if len(liste_ingr) != 0:
        line = liste_ingr[0]
        resultat = ''
        if len(unites) != 0:
            unite = unites[0]
            if unite in line:
                prepa = line.split(unite)[1]
                if '+' in prepa and len(line.split('+')[1]) != 0:
                    resultat = [reloutise(line.split('+')[0], unite),
                                reloutise(line.split('+')[1], unite)]
                    orga_entete.extend(resultat)
                else:
                    resultat = (line.split(unite)[0], unite,
                                ' '.join(prepa.split()[1:]).strip())
                    orga_entete.append(resultat)
            else:
                return liste_ingredients(liste_ingr, unites[1:], orga_entete)
        if resultat == '':
            if len(line) != 0:
                if re.search('^[0-9]+', line.split()[0]):
                    nb_ingr = line.split()[0]
                    ingr = ' '.join(line.split()[1:])
                    resultat = (nb_ingr, 'null', ingr)
                else:
                    resultat = ('null', 'null', line)
                orga_entete.append(resultat)
        unites = [' cl ', ' ml ', ' l ', ' dl ', 'g ', ' kg ', ' kilogramme ',
                  ' kilogrammes ', ' gramme ', ' grammes ', 'gr ']
        return liste_ingredients(liste_ingr[1:], unites, orga_entete)
    return orga_entete


def lire_ingr(ingredients, token, ancien_token, futur_token):
    """
    Fonction récursive qui annote surpuissamment les ingrédients.
    """
    if len(ingredients) != 0:
        ingr_courant = [ingr.lemma_ for ingr in ingredients[0]]
        lemme = ''
        if isinstance(ancien_token, str):
            ancien_token = nlp(ancien_token)
        if isinstance(futur_token, str):
            futur_token = nlp(futur_token)
        else:
            lemme = token.lemma_
        if lemme in ingr_courant:
            if token.is_stop or len(lemme) == 1:
                if ancien_token.lemma_ in ingr_courant:
                    if futur_token.lemma_ in ingr_courant:
                        return f"<ingredient>{str(token)}</ingredient>"
            else:
                return f"<ingredient>{str(token)}</ingredient>"
        return lire_ingr(ingredients[1:], token, ancien_token, futur_token)
    return str(token)


def annotation_ingr(tokens_recette, ingredients, ancien_token=None,
                    ingr_annote=None):
    """
    Fonction récursive surpuissante sur les tokens.
    """
    if ingr_annote is None:
        ingr_annote = []
    if ancien_token is None:
        ancien_token = ""
    futur_token = ""
    if len(tokens_recette) != 0:
        if len(tokens_recette) > 1:
            futur_token = tokens_recette[1]
        ingr_annote.append(lire_ingr(ingredients, tokens_recette[0],
                           ancien_token, futur_token))
        return annotation_ingr(tokens_recette[1:], ingredients,
                               tokens_recette[0], ingr_annote)
    return ingr_annote


def annotation(texte_recettes, ingredients):
    """
    Tokeniser
    """
    tokens_recette = nlp(texte_recettes.lower())
    recette_annotee = annotation_ingr(tokens_recette, ingredients)
    return recette_annotee


def create_ingr_list(tri_tuples):
    """
    Liste des noms des ingrédients
    """
    liste_ingr = [nlp(ingr.lower()) for num, unite,
                  ingr in tri_tuples]
    liste_ingr2 = []
    for ingr in liste_ingr:
        ingr2 = []
        for elt in ingr:
            if not elt.is_punct:
                ingr2.append(elt)
        liste_ingr2.append(ingr2)
    return liste_ingr2
