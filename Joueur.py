from grille import Grille
from bataille import Bataille
from random import randint
from constants import RATE, BAT_TOUCHE


class Joueur:
    def __init__(self, nom: str):
        self.nom = nom
        self.score = 0

    def jouer(self, taille_grille: int) -> int:
        """Joue un jeu de bataille navale jusqu'à la victore, i.e. jusqu'à couler tous les bateaux.
            La grille est générée aléatoirement. Elle contient 5 bateaux (un de chaque type).

        Args:
            taille_grille : taille de la grille du jeu

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        grille = Grille.genere_grille(taille_grille)
        bataille = Bataille(grille)
        nb_coups = 0

        while not bataille.victoire():
            ligne, col = randint(0, taille_grille - 1), randint(0, taille_grille - 1)
            # Si la case n'était pas encore tirée
            if grille.grille[ligne][col] not in {BAT_TOUCHE, RATE}:
                bataille.joue((ligne, col))
                nb_coups += 1

        self.score += 1
        return nb_coups


if __name__ == "__main__":
    joueur = Joueur("Joueur")
    nb_coups = joueur.jouer(10)
    print(nb_coups)
