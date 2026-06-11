# ============================================================================
#  Makefile — compilation séparée (modularité .c -> .o -> exécutable)
#
#  Cibles :
#    make            compile les deux programmes (pile_demo et linked_list)
#    make pile_demo  compile la démo de pile (pile.o + main.o)
#    make clean      supprime les fichiers générés (.o et exécutables)
#
#  Le drapeau -Werror traite tout avertissement comme une erreur :
#  le code doit donc être strictement propre pour compiler.
# ============================================================================

CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -std=c11

all: pile_demo linked_list

# --- Programme modulaire : interface (pile.h) + implémentation (pile.c) ---
pile_demo: pile.o main.o
	$(CC) $(CFLAGS) -o pile_demo pile.o main.o

# Chaque .o dépend de son .c et des en-têtes qu'il inclut.
pile.o: pile.c pile.h
	$(CC) $(CFLAGS) -c pile.c

main.o: main.c pile.h
	$(CC) $(CFLAGS) -c main.c

# --- Programme autonome (bonus) ---
linked_list: linked_list.c
	$(CC) $(CFLAGS) -o linked_list linked_list.c

clean:
	rm -f *.o pile_demo linked_list

.PHONY: all clean
