import statistics as stat

with open('tous_les_temps') as nb:
    nombres = nb.read()

liste_nb = [float(nb) for nb in nombres.split('\n') if not nb == '']

print(liste_nb)

print(round(stat.mean(liste_nb), 3))

