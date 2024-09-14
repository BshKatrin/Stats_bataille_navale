import numpy as np
import matplotlib.pyplot as plt
from random import randint, choice
from typing import Self

from constants import *


class Grille:
    def __init__(self, n: int):
        self.n: int = n  # taille d'une cote
        self.grille = np.zeros((n, n), dtype=np.int8)

    def peut_placer(self, bateau: int, position: tuple[int, int], direction: int) -> bool:
        """Vérifie s'il est possible de placer le bateau à la position dans la direction donnée sur la grille.

        Args:
            bateau: Type du bateau (constante).
            position: (ligne, colonne) indique la position sur la grille à laquelle placer la bateau.
                (0, 0) représente le coin supérieur gauche.
            direction: Direction (constante) dans laquelle placer le bateau.

        Returns:
            bool: True si le placement est possible, False sinon.

        """

        ligne, col = position
        taille_bat = BAT_CASES[bateau]  # taille du bateau

        if direction == HOR:
            # cas tout a droite
            # Pourquoi nécessaire? 2ième if va le checker normalement
            # if col == self.n - 1:
            #     return False

            # on verifie si il y a de la place pour le bateau
            if self.n - col < taille_bat:
                return False

            # on verifie si les cases sont libres
            for i in range(col, col + taille_bat):
                if self.grille[i][col] != VIDE:
                    return False

            return True

        if direction == VER:

            # cas tout en bas
            # Pourquoi nécessaire? 2ième if va le checker normalement
            # if ligne == self.n-1:
            #     return False

            # on verifie si il y a de la place pour le bateau
            if self.n - ligne < taille_bat:
                return False

            # on verifie si les cases sont libres
            for i in range(ligne, ligne + taille_bat):
                if self.grille[i][col] != VIDE:
                    return False

            return True

    # Pas nécessaire de renvoyer la grille, le tableau est dans la classe
    def place(self, bateau: int, position: tuple[int, int], direction: int) -> None:
        """Place la bateau sur la grille à la position et en diretion données. Attention : le placement doit être possible.

        Args:
            bateau: Type du bateau (constante).
            position: (ligne, colonne) indique la position sur la grille à laquelle placer la bateau.
                (0, 0) représente le coin supérieur gauche.
            direction: Direction (constante) dans laquelle placer le bateau.
        """

        ligne, col = position
        taille_bat = BAT_CASES[bateau]

        if direction == HOR:
            for i in range(col, col + taille_bat):
                self.grille[ligne][i] = bateau

        if direction == VER:
            for i in range(ligne, ligne + taille_bat):
                self.grille[i][col] = bateau

    def place_alea(self, bateau: int) -> None:
        """Place le bateau aléatoirement dans la grille.

        Args:
            bateau: Type du bateau (constante).
        """

        while True:
            position = (randint(0, self.n-1), randint(0, self.n-1))
            direction = choice([HOR, VER])

            if self.peut_placer(bateau, position, direction):
                # self.grille = self.place(bateau, position, direction)  # Pas nécesaire
                self.place(bateau, position, direction)
                return

    def affiche(self) -> None:
        """Affiche la grille dans une fenêtre séparée."""

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        rgb = (222, 243, 246)  # bleu claire
        image_tab = [[rgb for _ in range(self.n+1)] for _ in range(self.n+1)]

        self.ax.imshow(image_tab)

        # Valeurs des axes x, y
        self.ax.set_xticks(np.arange(0, self.n))
        self.ax.set_yticks(np.arange(0, self.n))

        # Limites des axes
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(self.n, 0)

        # Dessiner la grille en arrière
        self.ax.grid()

        # Dessiner les bateux (nombres associés) dans les cases
        self._affiche_bateaux()

        plt.title("Bataille bateau. Grille")
        plt.show()

    def _affiche_bateaux(self) -> None:
        """Dessine les bateaux (les numéros associés) sur la grille de matplotlib."""
        for (col, ligne), label in np.ndenumerate(self.grille):
            if label != VIDE:
                self.ax.text(ligne+0.5, col+0.5, label, ha='center', va='center')

    def eq(self, grilleA: Self) -> bool:
        """Vérifie l'égalité entre deux grilles. L'égalité entre deux grilles est considérés vérifiée ssi elles ont:
            - la même taille 
            - les mêmes cases vides
            - les mêmes bateux sur les mêmes cases

        Args:
            grilleA: La grille avec laquelle il faut vérifier l'égalité.  
        """

        # Meme classe
        if (grilleA.__class__ != self.__class__):
            return False
        # Vérifier la taille des grilles
        if (self.n != grilleA.n):
            return False
        # Vérifier que toutes les cases ont les mêmes valeurs
        for i in range(grilleA.n):
            for j in range(grilleA.n):
                if self.grille[i][j] != grilleA.grille[i][j]:
                    return False
        return True

    @ classmethod
    def genere_grille(cls, n: int) -> Self:
        """Créer une nouvelle grille de la taille n remplie de 5 bateux (un de chaque type).

        Args:
            n: Taille de la nouvelle grille.

        Returns:
            Une nouvelle instance de la classe Grille dont le tableau 'grille' est rempli des bateux. 
        """

        nouv_grille = Grille(n)
        for bat_type in BAT_CASES.keys():
            nouv_grille.place_alea(bat_type)
        return nouv_grille


if __name__ == "__main__":
    grille = Grille.genere_grille(10)
    for i in range(grille.n):
        print(grille.grille[i])
    grille.affiche()
