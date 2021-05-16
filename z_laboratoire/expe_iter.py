# -*- coding: utf-8 -*-
# Anaëlle Pierredon, Martin Digard

"""
Base pour le test de fonction imbriquée « expe_recursif.py ».
"""

alpha = ['a', 'b', 'c', 'd']
num = [1, 2, 3, 4]

for lettre in alpha:
    for nb in num:
        print(f"{lettre} : {nb}")
