"""
Comparaison récursif vs itératif
"""

nombre = input('entre un nombre : ')
nombre = int(nombre)


def factorielle(num):
    """ Itératif """
    fac = 1
    for i in range(num):
        fac = fac * (num - i)
    return fac


def factorec(num):
    """ Récursif """
    if num == 1:
        return 1
    return num * factorec(num - 1)


print(f"récursif: {factorec(nombre)}")
print (f"itératif: {factorielle(nombre)}")
