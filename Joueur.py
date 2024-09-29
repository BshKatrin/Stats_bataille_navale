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
            Stratégie: auncune, choix des cases de façon aléatoire.

        Args:
            taille_grille : taille de la grille du jeu

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        #on génère une grille de jeu
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

    def cases_connexes(self, bataille: Bataille, position: tuple) -> int:
        """Fonction auxiliaire de jouer_strat(), joue les cases connexes de la case position non jouées si possible.
        
        Args:
            bataille: la grille de jeu
            position: tuple (ligne, col) représentant la position de la case jouée
        
        Returns:
            Retourne le nombre de cases annexes jouées    
        """
        ligne, col = position
        grille_jeu = bataille.plat.grille
        n = bataille.plat.n 
        nb_coup = 0
        
        # a droite
        if col < n-1:
            if grille_jeu[ligne][col+1] not in {BAT_TOUCHE, RATE}:
                bataille.joue((ligne, col+1)) 
                nb_coup += 1
        # a gauche
        if 0 < col:
            if grille_jeu[ligne][col-1] not in {BAT_TOUCHE, RATE}:
                bataille.joue((ligne, col-1)) 
                nb_coup += 1
        # en haut
        if 0 < ligne:
            if grille_jeu[ligne - 1][col] not in {BAT_TOUCHE, RATE}:
                bataille.joue((ligne - 1, col))
                nb_coup += 1
        # en bas
        if ligne < n-1:
            if grille_jeu[ligne + 1][col] not in {BAT_TOUCHE, RATE}:
                bataille.joue((ligne + 1, col))
                nb_coup += 1
        return nb_coup

    def jouer_strat(self, taille_grille: int) -> int:
        """Joue un jeu de bataille navale jusqu'à la victore, i.e. jusqu'à couler tous les bateaux.
            La grille est générée aléatoirement. Elle contient 5 bateaux (un de chaque type).
            Stratégie: Si une case bateau est touchée lors d'un tour, la case du prochain tour sera connexe a la 
            case précédente. Sinon la prochaine case est choisie aléatoirement.

        Args:
            taille_grille : taille de la grille du jeu

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        #on génère une grille de jeu
        grille = Grille.genere_grille(taille_grille)
        bataille = Bataille(grille)
        nb_coups = 0

        while not bataille.victoire():
            #choix aléatoire
            ligne, col = randint(0, taille_grille - 1), randint(0, taille_grille - 1)

            # Si la case n'était pas encore tirée
            if grille.grille[ligne][col] not in {BAT_TOUCHE, RATE}:
                if grille.grille[ligne][col] == 0:  # cas vide
                    bataille.joue((ligne, col))
                    nb_coups += 1
                else:                               # cas bateau
                    bataille.joue((ligne, col))
                    #on joue les cases connexes
                    nb_coups += self.cases_connexes(bataille, (ligne, col)) + 1

        self.score += 1
        return nb_coups


if __name__ == "__main__":
    joueur = Joueur("Joueur")

    tot = 0
    for i in range(10000):
        tot += joueur.jouer_strat(10)
    print(tot/10000) #retourne 87.3
