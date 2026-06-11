#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
algo_lineaire_vs_quadratique.py
===============================

Illustration concrète de la différence entre un algorithme LINÉAIRE
(une seule boucle, complexité O(n)) et un algorithme QUADRATIQUE
(deux boucles imbriquées, complexité O(n²)).

On mesure le temps d'exécution pour des tailles croissantes : quand on
double n, l'algorithme linéaire double environ son temps, tandis que le
quadratique le multiplie par ~4. C'est tout l'intérêt de savoir
distinguer les deux.

Exécution :
    python3 algo_lineaire_vs_quadratique.py
"""

import time


def somme_lineaire(valeurs):
    """
    Algorithme LINÉAIRE — O(n).
    Une seule boucle qui parcourt la liste une fois.
    """
    total = 0
    for v in valeurs:          # n itérations
        total += v
    return total


def compte_doublons(valeurs):
    """
    Algorithme QUADRATIQUE — O(n²).
    Deux boucles imbriquées : pour chaque élément, on le compare à tous
    les éléments suivants. Le nombre de comparaisons croît comme n².

    (Volontairement naïf : une version efficace utiliserait un ensemble
    'set' pour redescendre en O(n). Le but ici est d'illustrer le coût
    des boucles imbriquées.)
    """
    doublons = 0
    n = len(valeurs)
    for i in range(n):             # n itérations
        for j in range(i + 1, n):  # ... chacune fait ~n itérations -> n²
            if valeurs[i] == valeurs[j]:
                doublons += 1
    return doublons


def mesure(fonction, valeurs):
    """Renvoie le temps d'exécution (en secondes) d'une fonction."""
    debut = time.perf_counter()
    fonction(valeurs)
    return time.perf_counter() - debut


def main():
    print(f"{'n':>7} | {'linéaire O(n)':>16} | {'quadratique O(n²)':>20}")
    print("-" * 50)

    for n in (1000, 2000, 4000, 8000):
        # liste de 0 à n-1 (modulo pour créer quelques doublons)
        valeurs = [k % 50 for k in range(n)]

        t_lin = mesure(somme_lineaire, valeurs)
        t_quad = mesure(compte_doublons, valeurs)

        print(f"{n:>7} | {t_lin*1000:>13.3f} ms | {t_quad*1000:>17.3f} ms")

    print("\nObservation : en doublant n, le temps linéaire ~x2,")
    print("le temps quadratique ~x4. C'est la signature du O(n²).")


if __name__ == "__main__":
    main()
