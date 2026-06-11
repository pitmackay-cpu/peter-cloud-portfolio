/* ************************************************************************** */
/*  pile.h — Interface d'une pile (LIFO) d'entiers à capacité fixe.           */
/*                                                                            */
/*  Démontre la MODULARITÉ : l'interface (prototypes + type) est séparée      */
/*  de l'implémentation (pile.c). Les fichiers qui utilisent la pile          */
/*  incluent uniquement ce .h ; la compilation se fait séparément (.o).       */
/* ************************************************************************** */

#ifndef PILE_H
# define PILE_H

# define PILE_MAX 100   /* capacité maximale de la pile */

/*
** Structure représentant une pile :
** - donnees : tableau stockant les valeurs
** - sommet  : index du prochain emplacement libre (donc aussi la taille)
*/
typedef struct s_pile
{
	int	donnees[PILE_MAX];
	int	sommet;
}	t_pile;

/* Initialise une pile vide. */
void	pile_init(t_pile *p);

/* Renvoie 1 si la pile est vide, 0 sinon. */
int		pile_est_vide(const t_pile *p);

/* Renvoie 1 si la pile est pleine, 0 sinon. */
int		pile_est_pleine(const t_pile *p);

/* Empile une valeur. Renvoie 0 si succès, 1 si la pile est pleine. */
int		pile_empiler(t_pile *p, int valeur);

/* Dépile dans *valeur. Renvoie 0 si succès, 1 si la pile est vide. */
int		pile_depiler(t_pile *p, int *valeur);

/* Renvoie le nombre d'éléments actuellement dans la pile. */
int		pile_taille(const t_pile *p);

#endif
