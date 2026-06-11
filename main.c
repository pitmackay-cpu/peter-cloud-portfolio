/* ************************************************************************** */
/*  main.c — Programme de démonstration de la pile.                           */
/*                                                                            */
/*  Illustre : variables, structures de contrôle (for / while), appels de     */
/*  fonctions, printf, et utilisation d'une structure (t_pile).               */
/*                                                                            */
/*  Compilation séparée puis édition de liens :                               */
/*      gcc -Wall -Wextra -Werror -c main.c     ->  produit main.o            */
/*      gcc -o pile_demo pile.o main.o          ->  produit l'exécutable      */
/*  (voir le Makefile)                                                        */
/* ************************************************************************** */

#include <stdio.h>
#include "pile.h"

int	main(void)
{
	t_pile	p;
	int		i;
	int		valeur;

	pile_init(&p);

	/* On empile les entiers de 1 à 5 (structure de contrôle : for). */
	printf("Empilage : ");
	i = 1;
	for (i = 1; i <= 5; i++)
	{
		if (pile_empiler(&p, i) == 0)
			printf("%d ", i);
		else
			printf("[pile pleine] ");
	}
	printf("\nTaille de la pile : %d\n", pile_taille(&p));

	/*
	** On dépile tout : une pile est LIFO (Last In, First Out),
	** on doit donc récupérer 5, 4, 3, 2, 1 dans cet ordre.
	** Structure de contrôle : while.
	*/
	printf("Dépilage : ");
	while (pile_depiler(&p, &valeur) == 0)
		printf("%d ", valeur);
	printf("\nTaille finale : %d\n", pile_taille(&p));

	return (0);
}
