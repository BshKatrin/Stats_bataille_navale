import numpy as np
import matplotlib.pyplot as plt
from random import randint, choice
from typing import Self, Dict
from time import time
from constants import *


class Grille:
    def __init__(self, n: int):
        self.n: int = n  # taille d'un cote
        self.grille = np.zeros((n, n), dtype=np.int8)

        # Dict qui sert uniquement pour optimiser la fonction d'égalité entre 2 grilles si pour la fonction eq_alea
        # Associe au triplet (ligne, colonne, direction) un type du bateau
        # (ligne, colonne) indique le début du bateau
        self.bateaux_places: Dict[(int, int, int), int] = dict()

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

            # on verifie s'il y a de la place pour le bateau
            if self.n - col < taille_bat:
                return False

            # on verifie si les cases sont libres
            for i in range(col, col + taille_bat):
                if self.grille[ligne][i] != VIDE:
                    return False

            return True

        if direction == VER:
            # on verifie si il y a de la place pour le bateau
            if self.n - ligne < taille_bat:
                return False

            # on verifie si les cases sont libres
            for i in range(ligne, ligne + taille_bat):
                if self.grille[i][col] != VIDE:
                    return False

            return True

        return False

    def place(self, bateau: int, position: tuple[int, int], direction: int) -> None:
        """Place la bateau sur la grille à la position et en direction données. Attention : le placement doit être possible.

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

        self.bateaux_places[(ligne, col, direction)] = bateau

    def place_alea(self, bateau: int) -> None:
        """Place le bateau aléatoirement dans la grille.

        Args:
            bateau: Type du bateau (constante).
        """

        while True:
            position = (randint(0, self.n-1), randint(0, self.n-1))
            direction = choice([HOR, VER])
            if self.peut_placer(bateau, position, direction):
                self.place(bateau, position, direction)
                return

    def place_alea_list(self, bateaux: list) -> None:
        """Place les bateaux aléatoirement dans la grille.

        Args:
            bateaux: Liste de types de bateau (liste de constantes).
        """

        for bat in bateaux:
            self.place_alea(bat)
        return

    def affiche(self) -> None:
        """Affiche la grille dans une fenêtre séparée."""

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        rgb = (222, 243, 246)  # bleu clair
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
            - les mêmes bateaux sur les mêmes cases

        Args:
            grilleA: La grille avec laquelle il faut vérifier l'égalité.

        Returns:
            Un booléan True ssi les grilles sont égales. Sinon, False.
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

    def _eq_dict_bateaux(self, grilleA: Self) -> bool:
        """Vérifie l'égalité entre deux grilles. Utiliser uniquement pour la fonction eq_alea (pour optimisation).  
            Hypothèse:  
                - Les cases qui ne sont pas stockées dans le dictionnaire self.bateaux_places sont VIDES.

        Args:
            grilleA: La grille avec laquelle il faut vérifier l'égalité.  

        Returns:
            Un booléan True ssi les grilles sont égales. Sinon, False.
        """

        if (grilleA.__class__ != self.__class__):
            return False
        if (self.n != grilleA.n):
            return False
        return self.bateaux_places == grilleA.bateaux_places

    @classmethod
    def genere_grille(cls, n: int) -> Self:
        """Crée une nouvelle grille de la taille n remplie des 5 bateaux (un de chaque type).

        Args:
            n: Taille de la nouvelle grille.

        Returns:
            Une nouvelle instance de la classe Grille dont le tableau 'grille' est rempli des bateaux. 
        """

        nouv_grille = Grille(n)
        for bat_type in BAT_CASES.keys():
            nouv_grille.place_alea(bat_type)
        return nouv_grille

    def retirer_bateau(self, bateau: int, position: tuple[int, int], direction: int) -> None:
        """Retire le bateau de la grille.

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
                self.grille[ligne][i] = VIDE

        if direction == VER:
            for i in range(ligne, ligne + taille_bat):
                self.grille[i][col] = VIDE

    def calc_nb_placements_bateau(self, bateau: int) -> int:
        """Calcule le nombre de placements possibles du bateau sur la grille vide.

        Args:
            bateau: Type du bateau (constante).

        Returns:
            Nombre de placements possibles du bateau sur la grille vide.
        """

        taille_bat = BAT_CASES[bateau]
        cases_possibles = self.n - taille_bat + 1
        return self.n * cases_possibles * 2

    def calc_nb_placements_liste_bateaux(self, bateaux: list[int], count=0) -> int:
        """Calcule le nombre de configurations possibles à partir de la grille vide.  
            Les bateaux ne peuvent pas se superposer.

        Args:
            bateaux: Une liste des bateaux à placer sur la grille.
            count: Un compteur des configurations. Default = 0.

        Returns:
            Le nombre des configurations possibles des bateaux à partir de la grille vide.
        """

        if (len(bateaux) == 0):
            return 1  # configuration grille vide

        bateau = bateaux[0]

        # On est au dernier bateau. Il suffit juste de calculer tous les placements possibles
        if (len(bateaux) == 1):
            # Compteur temporaire pour compter le nombre de placements d'un bateau
            count_tmp = 0
            for i in range(self.n):
                for j in range(self.n):
                    for dir in {HOR, VER}:
                        if self.peut_placer(bateau, (i, j), dir):
                            count_tmp += 1
            return count + count_tmp

        # Placer un bateau
        for i in range(self.n):
            for j in range(self.n):
                for dir in {HOR, VER}:
                    if self.peut_placer(bateau, (i, j), dir):
                        # Placer le bateau
                        self.place(bateau, (i, j), dir)
                        # Passer aux bateaux restants
                        count = self.calc_nb_placements_liste_bateaux(bateaux[1:], count)
                        # Retirer le bateau placé
                        self.retirer_bateau(bateau, (i, j), dir)
        return count

    def generer_meme_grille(self) -> int:
        """Génére aléatoirement des grilles avec 5 bateaux (un de chaque type) la grille de l'instance courante (self.grille).  
            Hypothèse: self.grille ne contient que la liste des 5 bateaux, un de chaque type.

        Returns:
            Le nombre de tirages de grilles aléatoires jusqu'à obtenir la grille égale à self.grille
        """

        # On tire au moins une fois
        count = 1
        # Générer la grille de meme taille que l'instance courante et remplie de 5 bateaux
        grilleB = self.genere_grille(self.n)

        while (self._eq_dict_bateaux(grilleB) == False):
            count += 1
            grilleB = self.genere_grille(self.n)
        return count

    def _maj_grille_placements(self, bateau: int, position: tuple[int, int], dir: int, grille_ps) -> None:
        """On suppose qu'il est possible de placer le bateau donné (i.e. il y aura pas de dépassement)"""
        taille_bat = BAT_CASES[bateau]
        ligne, col = position
        if dir == HOR:
            for j in range(col, col+taille_bat):
                grille_ps[ligne][j] += 1

        if dir == VER:
            for i in range(ligne, ligne+taille_bat):
                grille_ps[i][col] += 1

    def count_nb_placements(self, bateau: int):

        grille_ps = np.zeros((self.n, self.n), dtype=np.int8)
        for i in range(self.n):
            for j in range(self.n):
                for dir in {HOR, VER}:
                    if self.peut_placer(bateau, (i, j), dir):
                        self._maj_grille_placements(bateau, (i, j), dir, grille_ps)
        return grille_ps


if __name__ == "__main__":
    grille = Grille(10)

    print(grille.grille)
    grille_ps = grille.count_nb_placements(PORTE_AVION)
    print(grille_ps)
    # for bat, size in BAT_CASES.items():
    #     grille_ps = grille.count_nb_placements(bat)
    #     print(size)
    #     print(grille_ps)
    # for i in range(10):
    #     print(grille.generer_meme_grille())
    # grille.place_alea(PORTE_AVION)
    # grille.place_alea(CROISEUR)
    # grille.place_alea(CONTRE_TORPILLEURS)
    # grille.place_alea(SOUS_MARIN)
    # grille.place_alea(TORPILLEUR)
