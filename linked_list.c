/* ************************************************************************** */
/*                                                                            */
/*   linked_list.c                                                            */
/*                                                                            */
/*   Démonstration des bases acquises à la Piscine de l'École 42 :            */
/*   - manipulation de pointeurs                                              */
/*   - allocation dynamique de mémoire (malloc) et libération (free)          */
/*   - structures chaînées et logique algorithmique                           */
/*                                                                            */
/*   Le programme construit une liste chaînée d'entiers, l'affiche, la        */
/*   renverse "en place" (manipulation de pointeurs, sans réallouer), puis    */
/*   libère proprement toute la mémoire.                                      */
/*                                                                            */
/*   Compilation :  gcc -Wall -Wextra -Werror linked_list.c -o linked_list   */
/*   Exécution   :  ./linked_list                                             */
/*                                                                            */
/*   Auteur : Peter Mackay — peter-cloud.com                                  */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>

/*
** Un maillon de la liste : une valeur entière et un pointeur vers le
** maillon suivant. Le dernier maillon pointe vers NULL.
*/
typedef struct s_node
{
	int				value;
	struct s_node	*next;
}	t_node;

/*
** Crée un nouveau maillon sur le tas (malloc) et l'initialise.
** Retourne NULL si l'allocation échoue : c'est l'appelant qui décide
** quoi faire de l'erreur (ici, on arrête proprement le programme).
*/
static t_node	*node_new(int value)
{
	t_node	*node;

	node = (t_node *)malloc(sizeof(t_node));
	if (node == NULL)
		return (NULL);
	node->value = value;
	node->next = NULL;
	return (node);
}

/*
** Ajoute un maillon en tête de liste.
** On reçoit l'adresse du pointeur de tête (t_node **) pour pouvoir
** modifier réellement la tête de l'appelant : c'est le point clé de la
** manipulation de pointeurs vue à la Piscine.
** Retourne 0 en cas de succès, 1 en cas d'échec d'allocation.
*/
static int	list_push_front(t_node **head, int value)
{
	t_node	*node;

	node = node_new(value);
	if (node == NULL)
		return (1);
	node->next = *head;
	*head = node;
	return (0);
}

/*
** Renverse la liste "en place" : on ne réalloue rien, on se contente de
** réorienter les pointeurs next maillon par maillon.
** prev / curr / next forment le trio classique du parcours destructif.
*/
static void	list_reverse(t_node **head)
{
	t_node	*prev;
	t_node	*curr;
	t_node	*next;

	prev = NULL;
	curr = *head;
	while (curr != NULL)
	{
		next = curr->next;   /* on mémorise la suite avant de la perdre */
		curr->next = prev;   /* on inverse le lien                      */
		prev = curr;         /* prev avance                             */
		curr = next;         /* curr avance                             */
	}
	*head = prev;            /* la nouvelle tête est l'ancien dernier   */
}

/*
** Affiche la liste sous la forme : 3 -> 2 -> 1 -> NULL
*/
static void	list_print(t_node *head)
{
	while (head != NULL)
	{
		printf("%d -> ", head->value);
		head = head->next;
	}
	printf("NULL\n");
}

/*
** Libère chaque maillon. On mémorise le suivant AVANT de free() le
** maillon courant, sinon on lirait de la mémoire déjà libérée
** (use-after-free) : erreur classique que la Piscine apprend à éviter.
*/
static void	list_free(t_node **head)
{
	t_node	*curr;
	t_node	*next;

	curr = *head;
	while (curr != NULL)
	{
		next = curr->next;
		free(curr);
		curr = next;
	}
	*head = NULL;   /* on évite un pointeur "pendant" (dangling pointer) */
}

int	main(void)
{
	t_node	*list;
	int		i;

	list = NULL;
	/* On insère 1..5 en tête : la liste résultante est 5 -> 4 -> 3 -> 2 -> 1 */
	i = 1;
	while (i <= 5)
	{
		if (list_push_front(&list, i) != 0)
		{
			fprintf(stderr, "Erreur : allocation mémoire échouée\n");
			list_free(&list);
			return (1);
		}
		i++;
	}

	printf("Liste initiale : ");
	list_print(list);

	list_reverse(&list);
	printf("Liste renversée: ");
	list_print(list);

	list_free(&list);
	return (0);
}
