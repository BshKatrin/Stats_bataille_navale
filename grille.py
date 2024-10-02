import numpy as np
import matplotlib.pyplot as plt
from random import randint, choice
from typing import Self, Dict
from time import time
from constants import *


class Grille:
    def __init__(self, n: int):
        self.n: int = n  # taille d'un côté
        self.grille = np.zeros((n, n), dtype=np.int8)

        # Dict qui associe au triplet (ligne, colonne, direction) un type du bateau
        # (ligne, colonne) indique le début du bateau
        self.bateaux_places: Dict[int, (int, int, int)] = dict()

    def peut_placer(self, bateau: int, position: tuple[int, int], direction: int, proba_simple: bool = False) -> bool:
        """Vérifie s'il est possible de placer le bateau à la position dans la direction donnée sur la grille.

        Args:
            bateau: Type du bateau (constante).
            position: (ligne, colonne) indique la position sur la grille à laquelle placer la bateau.
                (0, 0) représente le coin supérieur gauche.
            direction: Direction (constante) dans laquelle placer le bateau.
            proba_simple: Un booléen qui doit être à True si la stratégie (ver. proba simple) est utilisée.
                Sinon, doit être à False. Default = False.

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
                if proba_simple:
                    if self.grille[ligne][i] not in {VIDE, BAT_TOUCHE}:
                        return False
                else:
                    if self.grille[ligne][i] != VIDE:
                        return False

            return True

        if direction == VER:
            # on verifie si il y a de la place pour le bateau
            if self.n - ligne < taille_bat:
                return False

            # on verifie si les cases sont libres
            for i in range(ligne, ligne + taille_bat):
                if self.grille[i][col] not in {VIDE, BAT_TOUCHE}:
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

        self.bateaux_places[bateau] = (ligne, col, direction)

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

    def _choisir_max_pos(self, pos_cour: tuple[int, int], max_cour: int,
                         pos_nouv: tuple[int, int], grille_ps: np.ndarray) -> tuple[int, tuple[int, int]]:
        """Choisit la position (ligne, col) telle que grille_ps[ligne][col] contient le nombre maximale 
            parmi toutes les autres cases. Fonction auxilière pour 'Joueur.jouer_proba_simple'.

        Args:
            pos_cour: position (ligne, col) sur la grille telle que grille_ps[ligne][col] = le nombre maximale
                (avant MAJ de la grille)
            max_cour: le nombre maximale (avant MAJ de la grille)
            pos_nouv: position (ligne, col) sur la grille avec laquelle il faudra choisir le nouveau nombre maximale.
            grille_ps: grille-probabilité associée à un bateau.

        Returns:
            La position P sur la grille. P = pos_nouv si max_cour n'est plus le maximum. Sinon, P = pos_cour.
        """

        ligne, col = pos_nouv
        val_grille = grille_ps[ligne][col]
        if val_grille > max_cour:
            return val_grille, pos_nouv
        return max_cour, pos_cour

    def _maj_nb_placements(self, bateau: int, position: tuple[int, int], dir: int, grille_ps: np.ndarray) -> tuple[int, int]:
        """MAJ de la grille-probabilité pour un bateau qui peut être placé sur la position donnée.
            Fonction auxiliaire pour 'calc_nb_placements'.

        Args:
            bateau: Type du bateau (constante).
            position: Position (ligne, colonne) sur la grille. Le placement du bateau sur cette position doit être possible.
            direction: Direction (constante) dans laquelle placer le bateau.
            grille_ps: Grille-probablité associée à un bateau donné.

        Returns:
            La position (ligne, col) sur la grille telle que grille_ps[ligne][col] contient le nombre maximale
                parmi les cases mises à jour.
        """

        ligne, col = position
        taille = BAT_CASES[bateau]
        nb_cases_bat_touche = 0

        val_max = -1
        pos_max = (-1, -1)
        if dir == HOR:
            for j in range(col, col + taille):
                if self.grille[ligne][j] == BAT_TOUCHE:
                    nb_cases_bat_touche += 1
                else:
                    grille_ps[ligne][j] += 1
                    val_max, pos_max = self._choisir_max_pos(pos_max, val_max, (ligne, j), grille_ps)

            # Augmenter les probas
            if nb_cases_bat_touche:
                for j in range(col, col + taille):
                    if not self.grille[ligne][j] == BAT_TOUCHE:
                        grille_ps[ligne][j] += nb_cases_bat_touche
                    val_max, pos_max = self._choisir_max_pos(pos_max, val_max, (ligne, j), grille_ps)

        if dir == VER:
            for i in range(ligne, ligne+taille):
                if self.grille[i][col] == BAT_TOUCHE:
                    nb_cases_bat_touche += 1
                else:
                    grille_ps[i][col] += 1
                    val_max, pos_max = self._choisir_max_pos(pos_max, val_max, (i, col), grille_ps)

            # Augmenter les probas
            if nb_cases_bat_touche:
                for i in range(ligne, ligne+taille):
                    if not self.grille[i][col] == BAT_TOUCHE:
                        grille_ps[i][col] += nb_cases_bat_touche
                    val_max, pos_max = self._choisir_max_pos(pos_max, val_max, (i, col), grille_ps)
        return pos_max

    def calc_nb_placements(self, bateau: int, grille_ps: np.ndarray) -> tuple[int, int]:
        """MAJ de la grille-probabilité. La fonction calcule toutes les configurations possibles.

        Args:
            bateau: Type du bateau (constante).
            grille_ps: Grille-probabilité. Toutes ces valeurs doivent être à 0.

        Returns:
            La position (ligne, col) sur la grille telle que grille_ps[ligne][col] contient le nombre maximale
                parmi toutes ces autres cases.
        """

        mx = -1
        pos_max = (-1, -1)
        for i in range(self.n):
            for j in range(self.n):
                for dir in {VER, HOR}:
                    if self.peut_placer(bateau, (i, j), dir, proba_simple=True):
                        pos_nouv = self._maj_nb_placements(bateau, (i, j), dir, grille_ps)
                        mx, pos_max = self._choisir_max_pos(pos_max, mx, pos_nouv, grille_ps)
        return pos_max


if __name__ == "__main__":
    pass
