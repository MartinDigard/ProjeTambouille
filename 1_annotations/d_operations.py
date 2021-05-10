# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Module d’annotation des opérations.
"""

import re
import spacy
nlp = spacy.load('fr_core_news_sm')


def triingre(texte_initial, nouveau_texte=None):
    """
    Récursion sur le texte initial.
    Renvoie le nouveau format d’annotation.
    """
    if nouveau_texte is None:
        nouveau_texte = []
    if len(texte_initial) != 0:
        string = texte_initial[0]
        if re.search('<ingredient>[^<]+</ingredient>', string):
            nom_ingr = re.sub('<ingredient>([^<]+)</ingredient>', '\\1',
                              string)
            nom_ingr = re.sub(' ', '$$', nom_ingr)
            nom_ingr = nom_ingr + 'INGR'
            nouveau_texte.append(nom_ingr)
        else:
            nouveau_texte.append(string)
        return triingre(texte_initial[1:], nouveau_texte)
    return nouveau_texte


def detection_ingr(texte):
    """
    Entrée : le texte avec les ingrédients annotés
    Sortie : le texte avec les annotations normalisé pour spacy
    """
    texte = re.sub('(<ingredient>[^<]+</ingredient>)', '$$\\1$$', texte)
    texte = texte.split('$$')
    nouveau_texte = triingre(texte)
    texte = ' '.join(nouveau_texte)
    return texte


def etiquetage(tokens, string_tagged=None):
    """
    Entrée : Les tokens normalisés pour spacy
    Sortie : La liste des tokens étiquetés morpho-syntaxiquement (type string).
    """
    if string_tagged is None:
        string_tagged = []
    if len(tokens) == 0:
        return string_tagged
    token = tokens[0]
    if not token.is_space:
        if re.search('INGR', str(token)):
            token = str(token)
            token = re.sub('INGR', '_INGR', token)
            string_tagged.append(token)
        else:
            string_tagged.append(f"{token}_{token.pos_}")
        return etiquetage(tokens[1:], string_tagged)
    return etiquetage(tokens[1:], string_tagged)


def syntagme_oper(tokens_tagged, syntagme):
    """
    Détection d’un syntagme verbal à partir d’une liste de tokens.
    """
    if len(tokens_tagged) != 1:
        token_tagged_courant = tokens_tagged[0]
        token_tagged_suivant = tokens_tagged[1]
        token_courant = token_tagged_courant.split('_')[0]
        token_suivant = token_tagged_suivant.split('_')[0]
        pos_suivant = token_tagged_suivant.split('_')[1]
        aux = r'laisse(z|r)?|fai(re|tes|s)'
        if re.search(aux, token_courant):
            syntagme.append(token_tagged_suivant)
            return syntagme_oper(tokens_tagged[1:], syntagme)
        if not (pos_suivant == 'VERB' or re.search(aux, token_suivant)
                or token_suivant == '.'):
            syntagme.append(token_tagged_suivant)
            return syntagme_oper(tokens_tagged[1:], syntagme)
        return ' '.join(syntagme)
    return ' '.join(syntagme)


def detection_oper(tokens_tagged, tempo=None):
    """
    Entrée : Liste de tokens etiquetes
    Sortie : Texte annoté en opération et ingrédient
    """
    if tempo is None:
        tempo = []
    if len(tokens_tagged) == 0:
        return tempo
    token_tag = tokens_tagged[0]
    aux = r'laisse(z|r)?|fai(re|tes|s)'
    verbes = r'.*(ez|i(r|s))_VERB'
    token = token_tag.split('_')[0]
    stop = r'pouvez|ecrivez|utilisez|aurez|hésitez|souhaitez|frais|'\
           'pouvoir|devez|allez|voulez|coulis|chablis|préférez|'\
           'épais|aimez|pourrez|voir|affaire'
    if (re.search(aux,
                  token) or re.search(verbes,
                                      token_tag)) and not re.search(stop,
                                                                    token):
        operation = syntagme_oper(tokens_tagged, [token_tag])
        taille = len(operation.split())
        tempo.append(operation)
    else:
        taille = 1
    return detection_oper(tokens_tagged[taille:], tempo)


def annot_operation(operations, recette_postagged):
    """
    Annote les opérations.
    """
    if len(operations) != 0:
        syntagme = operations[0]
        syntagme = re.sub(r'\(', r'\\(', syntagme)
        syntagme = re.sub(r'\)', r'\\)', syntagme)
        syntagme = re.sub(r'\[', r'\\[', syntagme)
        syntagme = re.sub(r'\]', r'\\]', syntagme)
        syntagme = re.sub(r'\+', r'\\+', syntagme)
        recette_postagged = re.sub(f'({syntagme})',
                                   '<operation>\\1</operation>',
                                   recette_postagged)
        return annot_operation(operations[1:], recette_postagged)
    return recette_postagged


def annotation(recette):
    """
    Entrée : une recette dont les ingrédients ont été annotés.
    Sortie : une recette dont les opérations ont également été annotés.
    """
    # Normalisation de l’annotation des ingrédients pour spacy.
    prepa_tokens = detection_ingr(recette)

    # Étiquetage morpho-syntaxique des tokens et conversion en string.
    tokens = nlp(prepa_tokens)
    tokens_tagged = etiquetage(tokens)
    recette_postagged = ' '.join(tokens_tagged)

    # Annotation des opérations
    liste_operation = detection_oper(tokens_tagged)
    recette_annotee = annot_operation(liste_operation, recette_postagged)
    recette_annotee = re.sub(r' ([^_]+)_INGR', ' <ingredient>\\1</ingredient>',
                             recette_annotee)
    recette_annotee = re.sub(r'\$\$', ' ', recette_annotee)
    recette_annotee = re.sub(r'( [^_]+_(PUNCT))</operation>',
                             '</operation>\\1', recette_annotee)
    recette_annotee = re.sub(r'( [^_]+_(CCONJ))</operation>',
                             '</operation>\\1', recette_annotee)
    recette_annotee = re.sub(r'_[^(<| )]+', '', recette_annotee)
    recette_annotee = re.sub('<operation><operation>', '<operation>',
                             recette_annotee)
    recette_annotee = re.sub('</operation></operation>', '</operation>',
                             recette_annotee)

    return recette_annotee
