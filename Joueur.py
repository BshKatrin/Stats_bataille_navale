import numpy as np
from grille import Grille
from bataille import Bataille
from random import randint
from constants import *
from typing import Dict


class Joueur:
    def __init__(self, nom: str):
        self.nom = nom
        self.score = 0

    def jouer(self, taille_grille: int) -> int:
        """Joue un jeu de bataille navale jusqu'à la victore, i.e. jusqu'à couler tous les bateaux.
            La grille est générée aléatoirement. Elle contient 5 bateaux (un de chaque type).
            Stratégie: aucune, choix des cases de façon aléatoire.

        Args:
            taille_grille : taille de la grille du jeu

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        # on génère une grille de jeu
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

    def _cases_connexes(self, bataille: Bataille, position: tuple[int, int], nb_coupe: int=0) -> tuple[np.ndarray, int]:
        """Joue les cases connexes de la case position non jouées si possible,
            au maximum peut jouer 4 coups sur les 4 cases connexes. Fonction auxiliaire de jouer_heuristique().
            Si une case connexe est une case bateau, alors récursion de la fonction sur la case connexe.

        Args:
            bataille: la grille de jeu
            position: (ligne, col) représentant la position de la case jouée
            nb_coup: nombre de coup pour la récursion, à 0 par défaut

        Returns:
            La grille modifiée et le nombre de coups jouées
        """

        ligne, col = position
        grille_jeu = bataille.plat.grille
        n = bataille.plat.n
        nb_coup = nb_coupe

        # case connexe droite
        if col < n-1: 
            if grille_jeu[ligne][col+1] not in {BAT_TOUCHE, RATE}:
                # si case vide
                if grille_jeu[ligne][col+1] == 0: 
                    bataille.joue((ligne, col+1))
                    nb_coup += 1
                    
                # sinon case bateau
                else:  
                    bataille.joue((ligne, col+1))
                    nb_coup += 1
                    return self._cases_connexes(bataille, (ligne, col+1), nb_coup)

        # case connexe gauche
        if 0 < col:
            if grille_jeu[ligne][col-1] not in {BAT_TOUCHE, RATE}:
                # si case vide
                if grille_jeu[ligne][col-1] == 0: #si vide
                    bataille.joue((ligne, col-1))
                    nb_coup += 1

                # sinon case bateau
                else:   
                    bataille.joue((ligne, col-1))
                    nb_coup += 1
                    return self._cases_connexes(bataille, (ligne, col-1), nb_coup)


        # case connexe haut
        if 0 < ligne:
            if grille_jeu[ligne - 1][col] not in {BAT_TOUCHE, RATE}:
                # si case vide
                if grille_jeu[ligne-1][col] == 0: 
                    bataille.joue((ligne-1, col))
                    nb_coup += 1

                # sinon case bateau       
                else:   
                    bataille.joue((ligne-1, col))
                    nb_coup += 1
                    return self._cases_connexes(bataille, (ligne-1, col), nb_coup)

        # case connexe bas
        if ligne < n-1:
            if grille_jeu[ligne + 1][col] not in {BAT_TOUCHE, RATE}:
                # si case vide
                if grille_jeu[ligne+1][col] == 0: #si vide
                    bataille.joue((ligne+1, col))
                    nb_coup += 1

                # sinon case bateau     
                else:   
                    bataille.joue((ligne+1, col))
                    nb_coup += 1
                    return self._cases_connexes(bataille, (ligne+1, col), nb_coup)     
                
        return (grille_jeu, nb_coup)

    def jouer_heuristique(self, taille_grille: int) -> int:
        """Joue un jeu de bataille navale jusqu'à la victore, i.e. jusqu'à couler tous les bateaux.
            La grille est générée aléatoirement. Elle contient 5 bateaux (un de chaque type).
            Stratégie: Si une case bateau est touchée lors d'un tour, la case du prochain tour sera connexe a la
            case précédente. Sinon la prochaine case est choisie aléatoirement.
            Augmente le score du joueur de 1 point.

        Args:
            taille_grille : taille de la grille du jeu. Doit être supérieure ou égale à 5.

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        if taille_grille < 5:
            print("jouer_heuristique : taille_grille < 5")
            return 0

        # on génère une grille de jeu
        grille = Grille.genere_grille(taille_grille)
        bataille = Bataille(grille)
        nb_coups = 0

        while not bataille.victoire():
            # choix aléatoire
            ligne, col = randint(0, taille_grille - 1), randint(0, taille_grille - 1)

            # Si la case n'était pas encore tirée
            if grille.grille[ligne][col] not in {BAT_TOUCHE, RATE}:
                # cas vide
                if grille.grille[ligne][col] == VIDE:
                    bataille.joue((ligne, col))
                    nb_coups += 1
                # cas bateau
                else:
                    bataille.joue((ligne, col))
                    # on joue les cases connexes
                    grille.grille, coup_addi = self._cases_connexes(bataille, (ligne, col))
                    nb_coups += coup_addi + 1
        return nb_coups

    def _init_bateaux_grilles(self, bateaux: list[int], taille_grille: int) -> Dict[int, np.ndarray]:
        """Initialise pour chaque bateau dans une liste 'bateaux' un tableau (2D).
            Chaque case de la grille (nommée grille-probabilité) contiendra le nombre de configurations
            qui passent par cette case. Fonction auxilière pour 'jouer_proba_simple'.

        Args:
            bateaux : liste des constantes associées aux bateaux.
            taille_grille : taille de la grille du jeu.

        Returns:
            Un tableau (2D) de numpy repmpli de 0.
        """

        bateaux_grilles = dict()
        for bateau in bateaux:
            bateaux_grilles[bateau] = np.zeros((taille_grille, taille_grille), dtype=np.int8)
        return bateaux_grilles

    def _choisir_max(self, bateaux_grilles: Dict[int, np.ndarray],
                     bateaux_pos_max: Dict[int, tuple[int, int]]) -> tuple[int, int]:
        """Choisit la position qui correpond au nombre maximal parmi toutes les grilles associées aux bateaux.
            Fonction auxilière pour 'jouer_proba_simple'.

        Args:
            bateaux_grilles : dictionnaire associant une constante du bateau sa grille-probabilité.
            bateaux_pos_max : dictionnaire associant une constante du bateau la position (ligne, col) telle que 
                pour la grille associée au bateau on a grille[ligne][col] contient au nombre maximal parmi toutes les autres cases.

        Returns:
            Une position qui correspond au nombre maximale parmi toutes les grilles associées aux bateaux.
        """

        mx = 0
        pos_max = (0, 0)

        for bateau, (ligne, col) in bateaux_pos_max.items():
            grille = bateaux_grilles[bateau]
            valeur = grille[ligne][col]
            if valeur > mx:
                mx = valeur
                pos_max = (ligne, col)

        return pos_max

    def jouer_proba_simple(self, taille_grille: int) -> int:
        """Joue un jeu de bataille navale jusqu'à la victore, i.e. jusqu'à couler tous les bateaux.
            La grille est générée aléatoirement. Elle contient 5 bateaux (un de chaque type).
            Stratégie: On considère que les positions des bateaux sont indépendantes.
            Pour chaque bateau on calcule la probabilié jointe entre la case et le bateau. 
            À chaque tour on choisit la case qui à la probabilité maximale de contenir le bateau.
            Augmente le score du joueur de 1 point.

        Args:
            taille_grille : taille de la grille du jeu. Doit être supérieure ou égale à 5.

        Returns:
            Le nombre de coups qu'il fallait faire pour couler tous les bateaux.
        """

        if taille_grille < 5:
            print("'jouer_proba_simple' : taille_grille < 5")
            return 0

        nb_coups = 0
        # Grille avec 5 bateaux
        grille_remplie = Grille.genere_grille(taille_grille)
        bataille = Bataille(grille_remplie)

        # Grille vide
        grille_vide = Grille(taille_grille)

        # Bateau non encore coulés
        bateaux_restants = {bat for bat in BATEAUX}

        # Initialisation des grilles-probas pour chaque bateaux
        bateaux_grilles = self._init_bateaux_grilles(bateaux_restants, taille_grille)
        bateaux_pos_max = dict()

        # Remplie les grilles-probas, choisir les cases avec la proba max
        for bateau in bateaux_restants:
            grille_ps = bateaux_grilles[bateau]
            pos_max = grille_vide.calc_nb_placements(bateau, grille_ps)
            bateaux_pos_max[bateau] = pos_max

        while (not bataille.victoire()):
            nb_coups += 1

            # Choisir la case avec la proba la plus élevée parmi toutes les grilles-probas
            (ligne, col) = self._choisir_max(bateaux_grilles, bateaux_pos_max)
            # Type_case = BAT_TOUCHE ou RATE
            type_case = bataille.joue((ligne, col))
            grille_vide.grille[ligne][col] = type_case

            # Vérifier si le bateau a été coulé
            bateau_coule_flag, type_bat = bataille.bateaux_coules(bateaux_restants)

            # Eliminer le bateau s'il a été coulé, éliminer sa grille-proba
            if bateau_coule_flag:
                ligne, col, dir = grille_remplie.bateaux_places[type_bat]
                # Placer le bateau coulé sur la grille_vide
                grille_vide.place(type_bat, (ligne, col), dir)
                # Éliminter le bateau
                bateaux_restants.remove(type_bat)
                # Éliminer la grille
                del bateaux_grilles[type_bat]
                # Éliminer la case max associée à la grille
                del bateaux_pos_max[type_bat]

            # MAJ des grilles-probas restantes
            for bateau in bateaux_restants:
                grille_ps = bateaux_grilles[bateau]
                # Annuler toutes les cases pour le recalcul des configurations
                grille_ps.fill(0)
                # MAJ des max
                pos_max = grille_vide.calc_nb_placements(bateau, grille_ps)
                bateaux_pos_max[bateau] = pos_max

        self.score += 1
        return nb_coups


if __name__ == "__main__":
    joueur = Joueur("Joueur")
    for i in range(5):
        print(joueur.jouer_heuristique(10))
