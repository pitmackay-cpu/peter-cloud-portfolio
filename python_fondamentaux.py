#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
python_fondamentaux.py
======================

Petit programme illustrant les bases de Python attendues au programme :
variables, structures de contrôle (if / for / while), listes, tuples,
chaînes de caractères, fonctions et rattrapage d'exceptions.

Thème : gestion simple d'un relevé de notes.

Exécution :
    python3 python_fondamentaux.py
"""


def moyenne(notes):
    """Renvoie la moyenne d'une liste de notes (0 si la liste est vide)."""
    if len(notes) == 0:          # structure de contrôle : if
        return 0.0
    total = 0.0                  # variable
    for note in notes:           # structure de contrôle : for
        total += note
    return total / len(notes)


def mention(moy):
    """Associe une mention à une moyenne (utilise if / elif / else)."""
    if moy >= 16:
        return "Très bien"
    elif moy >= 14:
        return "Bien"
    elif moy >= 12:
        return "Assez bien"
    elif moy >= 10:
        return "Passable"
    else:
        return "Insuffisant"


def lire_note(texte):
    """
    Convertit une chaîne en note valide (0 à 20).
    Démontre le rattrapage d'exceptions : on intercepte ValueError si
    l'utilisateur saisit autre chose qu'un nombre.
    """
    try:
        valeur = float(texte)          # chaîne -> nombre
    except ValueError:
        raise ValueError(f"'{texte}' n'est pas un nombre valide")
    if valeur < 0 or valeur > 20:
        raise ValueError("la note doit être comprise entre 0 et 20")
    return valeur


def main():
    # tuple : un enregistrement (nom, liste de notes) — les tuples sont
    # immuables, parfaits pour regrouper des données qui vont ensemble.
    etudiants = [
        ("Alice", ["15", "12", "17"]),
        ("Bob", ["8", "11", "9"]),
        ("Chloé", ["14", "16", "abc", "13"]),  # contient une saisie invalide
    ]

    print("=== Relevé de notes ===")
    for nom, notes_texte in etudiants:         # parcours d'une liste de tuples
        notes = []                             # liste (mutable)
        for t in notes_texte:
            try:
                notes.append(lire_note(t))     # on ne garde que les notes valides
            except ValueError as e:
                print(f"  [{nom}] note ignorée : {e}")

        moy = moyenne(notes)
        # chaînes de caractères : formatage et méthode .upper()
        print(f"{nom.upper():<8} | moyenne = {moy:5.2f} | {mention(moy)}")


if __name__ == "__main__":
    main()
