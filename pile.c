/* ************************************************************************** */
/*  pile.c — Implémentation de la pile déclarée dans pile.h.                   */
/*                                                                            */
/*  Compilation séparée :                                                     */
/*      gcc -Wall -Wextra -Werror -c pile.c     ->  produit pile.o            */
/* ************************************************************************** */

#include "pile.h"

void	pile_init(t_pile *p)
{
	p->sommet = 0;
}

int	pile_est_vide(const t_pile *p)
{
	return (p->sommet == 0);
}

int	pile_est_pleine(const t_pile *p)
{
	return (p->sommet == PILE_MAX);
}

int	pile_empiler(t_pile *p, int valeur)
{
	if (pile_est_pleine(p))
		return (1);
	p->donnees[p->sommet] = valeur;
	p->sommet++;
	return (0);
}

int	pile_depiler(t_pile *p, int *valeur)
{
	if (pile_est_vide(p))
		return (1);
	p->sommet--;
	*valeur = p->donnees[p->sommet];
	return (0);
}

int	pile_taille(const t_pile *p)
{
	return (p->sommet);
}
