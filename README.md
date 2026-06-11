# peter-cloud-portfolio — Exemples de programmation (C & Python)

Ce dépôt rassemble de petits programmes, autonomes et commentés, qui
illustrent les **bases de programmation** attendues à l'entrée de la
Licence Professionnelle **ADSILLH** : programmation de base en C et en
Python, modularité, et algorithmique élémentaire.

Chaque fichier est volontairement simple et lisible : l'objectif est de
montrer la maîtrise des notions fondamentales, pas d'empiler des
fonctionnalités.

---

## Contenu

```
.
├── Makefile                          # Compilation séparée (.c -> .o -> exécutable)
├── pile.h                            # Interface C : type + prototypes
├── pile.c                            # Implémentation de la pile
├── main.c                            # Démo : variables, contrôle, fonctions, printf
├── python_fondamentaux.py            # Listes, tuples, chaînes, fonctions, exceptions
└── algo_lineaire_vs_quadratique.py   # O(n) vs O(n²), avec mesure de temps
```

---

## Exemples C

Une pile (LIFO) d'entiers, organisée en **modules** : l'interface
(`pile.h`) est séparée de l'implémentation (`pile.c`), et le `Makefile`
réalise la **compilation séparée** (`.c` → `.o` → exécutable).

Notions couvertes : variables, structures de contrôle (`if`, `for`,
`while`), fonctions, `printf`, structures (`struct`), modularité
(`.h` / `.o`).

```bash
make            # compile pile_demo
./pile_demo
```

## Exemples Python

`python_fondamentaux.py` — petit relevé de notes illustrant variables,
structures de contrôle, listes, tuples, chaînes de caractères, fonctions
et rattrapage d'exceptions (`try` / `except`).

`algo_lineaire_vs_quadratique.py` — comparaison concrète d'un algorithme
linéaire `O(n)` (une boucle) et d'un algorithme quadratique `O(n²)` (deux
boucles imbriquées), avec mesure du temps d'exécution.

```bash
python3 python_fondamentaux.py
python3 algo_lineaire_vs_quadratique.py
```

---

## Correspondance avec les prérequis ADSILLH

| Prérequis | Démontré dans |
|---|---|
| C — variables, `if`/`for`/`while`, fonctions, `printf`, structures | `pile.h`, `pile.c`, `main.c` |
| C — modularité : compilation séparée `.o`, interface `.h` | `Makefile`, `pile.h` |
| Python — variables, structures de contrôle, fonctions | `python_fondamentaux.py` |
| Python — listes, tuples, chaînes de caractères | `python_fondamentaux.py` |
| Python — rattrapage d'exceptions | `python_fondamentaux.py` |
| Algorithmique — linéaire `O(n)` vs quadratique `O(n²)` | `algo_lineaire_vs_quadratique.py` |
| Compilation vs interprétation (C compilé / Python interprété) | l'ensemble du dépôt |

---

## À propos

Peter Mackay — Titre Professionnel **TSSR**, candidat à la L3 Pro ADSILLH.
Bases de programmation acquises lors de la **spécialité NSI** au
Baccalauréat et de la **Piscine de l'École 42 Angoulême** (2022, langage
C), puis mises en pratique dans un home lab personnel (`peter-cloud.com`).
