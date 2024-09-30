import numpy as np
from grille import Grille
from constants import BAT_TOUCHE, RATE, VIDE


class Bataille:
    def __init__(self, grille: Grille):
        self.plat = grille

    def joue(self, position: tuple[int, int]) -> None:
        """Joue la case de la grille à la position. Si il y avait un bateau, alors case = BAT_TOUCHE, sinon case = RATE.

        Args:
            position: tuple (ligne, col) qui désigne la case à jouer
        """
        ligne, col = position

        if self.plat.grille[ligne][col] == VIDE:
            self.plat.grille[ligne][col] = RATE
            return

        self.plat.grille[ligne][col] = BAT_TOUCHE
        return

    def victoire(self) -> bool:
        """Vérifie si tous les bateaux ont été coulés dans la grille (i.e. une victoire dans le jeu).

        Return:
            Un booléen True s'il n y a plus des bateaux restants, i.e. toutes les cases de la grille sont à 0, -1 ou -2.
        """

        for ligne in range(0, self.plat.n):
            # si différent de BAT_TOUCHE, VIDE, et RATE
            if not np.all(self.plat.grille[ligne] <= VIDE):
                return False
        return True

    def reset(self) -> None:
        """Commence le jeu dès le début. Recommencer sur la meme grille mais avec les bateaux sans pannes.
        Reinitialise la grille avec les bateaux à la même position qu'avant avec aucun coup joué.
        """
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
