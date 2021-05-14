# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Analyse de la complexité en temps de la fonction d'annotation
"""

import matplotlib.pyplot as plt

# Création du graphique
fig, axes = plt.subplots()
axes.plot([1000, 2000, 4000, 7691], [115, 214, 414, 795], 'r-', lw=2,
          label="Anaëlle")  # Red Anaëlle Line
axes.plot([1000, 2000, 4000, 7691], [175, 300, 625, 1100], 'b--',
          lw=2, label="Martin")  # Blue Martin line
axes.set_title("Analyse de la complexité en temps de la fonction d'annotation")
axes.set_ylabel("Temps (s)")
axes.set_xlabel("Nombre de recettes")
axes.legend()
plt.savefig('analyse_complexite.png')
