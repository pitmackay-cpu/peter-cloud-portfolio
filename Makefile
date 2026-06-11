# ============================================================================
#  Makefile — compilation séparée (modularité .c -> .o -> exécutable)
#
#  Cibles :
#    make            compile le programme pile_demo
#    make clean      supprime les fichiers générés (.o et exécutable)
#
#  Le drapeau -Werror traite tout avertissement comme une erreur :
#  le code doit donc être strictement propre pour compiler.
# ============================================================================

CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -std=c11

all: pile_demo

# Programme modulaire : interface (pile.h) + implémentation (pile.c)
pile_demo: pile.o main.o
	$(CC) $(CFLAGS) -o pile_demo pile.o main.o

# Chaque .o dépend de son .c et des en-têtes qu'il inclut.
pile.o: pile.c pile.h
	$(CC) $(CFLAGS) -c pile.c

main.o: main.c pile.h
	$(CC) $(CFLAGS) -c main.c

clean:
	rm -f *.o pile_demo

.PHONY: all clean
