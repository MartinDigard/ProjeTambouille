"""
Séparer les données et affichage :
- Créer une fonction pour l’affichage
- Toutes les autres fonctions sont considérées comme étant des données.
"""


def branches(dico):
    """Affichage"""
    print()
    for k, val in dico.items():
        print(f"Station possibles pour {k} :")
        for stations in val:
            print(stations)
    print()


def chatelet():
    """À une station de chatelet."""
    print()
    print("Station possibles pour Chatelet :")

    def sub_chatelet(sub=None):
        if sub is None:
            sub = []
        if len(sub) != 0:
            current_station = sub[0]
            print(current_station)
            return sub_chatelet(sub[1:])
        return "rien"
    sub_chatelet(['Louvre-Rivoli', 'Les Halles', 'cité', 'Hotel de ville'])


chatelet()
print()
