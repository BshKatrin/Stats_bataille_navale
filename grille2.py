import numpy as np
import matplotlib.pyplot as plt

from typing import Dict

PORTE_AVION: int = 1
CROISEUR: int = 2
CONTRE_TORPILLEURS: int = 3
SOUS_MARIN: int = 4
TORPILLEUR: int = 5

BAT_CASES = {PORTE_AVION: 5, CROISEUR: 4, CONTRE_TORPILLEURS: 3, SOUS_MARIN: 3, TORPILLEUR: 2}


class Grille:
    def __init__(self, n: int):
        self.n: int = n  # taille d'une cote

        self.grille = np.zeros((n, n), dtype=np.int8)

    def affiche(self) -> None:
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        rgb = (222, 243, 246)
        image_tab = [[rgb for _ in range(self.n)] for _ in range(self.n)]
        self.ax.imshow(image_tab, cmap="coolwarm", )

        self.ax.set_xticks(np.arange(0, self.n, 1))
        self.ax.set_yticks(np.arange(0, self.n, 1))

        self.ax.set_xlim(0, self.n-1)
        self.ax.set_ylim(9, 0)

        self.ax.grid()

        plt.title("Bataille bateau. Grille")
        plt.show()

    # Revoir. Ajouter une exception?
    def get_val_case(self, ligne: int, col: int) -> int:
        return self.grille[ligne][col]

    def eq(self, grilleA, grilleB) -> bool:
        if (grilleA.__class__ != self.__class__):
            return False
        if (grilleB.__class__ != self.__class__):
            return False
        # Vérifier la taille des grilles
        if (grilleA.n != grilleB.n):
            return False
        # Vérifier que toutes les cases ont les mêmes valeurs
        for i in range(grilleA.n):
            for j in range(grilleA.n):
                if (grilleA.get_val_case(i, j) != grilleB.get_val_case(i, j)):
                    return False
        return True


if __name__ == "__main__":
    grille = Grille(10)
