import numpy as np
from grille import Grille
from constants import BAT_TOUCHE, RATE, VIDE, BAT_CASES, HOR, VER


class Bataille:
    def __init__(self, grille: Grille):
        self.plat = grille

    def joue(self, position: tuple[int, int]) -> int:
        """Joue la case de la grille à la position. Si il y avait un bateau, alors case = BAT_TOUCHE, sinon case = RATE.

        Args:
            position: (ligne, col) qui désigne la case sur la grille à jouer.
                (0, 0) représente le coin supérieur gauche.
        """

        ligne, col = position

        if self.plat.grille[ligne][col] == VIDE:
            self.plat.grille[ligne][col] = RATE
            return RATE

        self.plat.grille[ligne][col] = BAT_TOUCHE
        return BAT_TOUCHE

    def _bateau_coule(self, bateau: int) -> bool:
        """Vérifie si le bateau donné a été coulé.

        Args:
            bateau : Type du bateau (constante).

        Returns:
            Un booléen True si le bateau a été coulé. Sinon, False.
        """

        (ligne, col, dir) = self.plat.bateaux_places[bateau]
        taille = BAT_CASES[bateau]
        if dir == HOR:
            for j in range(col, col + taille):
                if self.plat.grille[ligne][j] != BAT_TOUCHE:
                    return False
            return True

        if dir == VER:
            for i in range(ligne, ligne+taille):
                if self.plat.grille[i][col] != BAT_TOUCHE:
                    return False
            return True

        return False

    def bateaux_coules(self, bateaux: list[int]) -> tuple[bool, int]:
        """Trouve les bateaux qui ont été coulés. Hypothèse : il n'y a qu'un seul bateau coulé parmi bateaux donnés.

        Args:
            bateaux : Liste des bateaux (des constantes) parmi lesquels il faut trouver les bateaux coulés.

        Returns:
            Un booléen True et le type de bateau coulé. False et -1 si aucun bateau est coulé.
        """

        for bateau in bateaux:
            if self._bateau_coule(bateau):
                return True, bateau
        return False, -1

    def victoire(self) -> bool:
        """Vérifie si tous les bateaux ont été coulés dans la grille (i.e. une victoire dans le jeu).

        Return:
            Un booléen True s'il n y a plus des bateaux restants, i.e. toutes les cases de la grille sont à 0, -1 ou -2.
            Sinon, False.
        """

        for ligne in range(0, self.plat.n):
            # si différent de BAT_TOUCHE, VIDE, et RATE
            if not np.all(self.plat.grille[ligne] <= VIDE):
                return False
        return True

    def reset(self) -> None:
        """Commence le jeu depuis le début. Recommence sur la même grille, mais avec les bateaux sans avarie.
        Réinitialise la grille avec les bateaux à leur position initiale, sans aucun coup joué."""

        self.plat.grille.fill(0)
        for (ligne, col, dir), bateau in self.plat.bateaux_places.items():
            self.plat.place(bateau, (ligne, col), dir)
        return


if __name__ == "__main__":
    bat = Bataille(Grille.genere_grille(10))
    print(bat.plat.grille)
    for i in range(0, 10):
        for j in range(0, 10):
            bat.joue((i, j))
    print("apres jeu")
    print(bat.plat.grille)
    print(bat.victoire())
    bat.reset()
    print("apres reset")
    print(bat.plat.grille)
