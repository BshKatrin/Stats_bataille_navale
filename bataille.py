import numpy as np
from grille import Grille
from constants import *


class Bataille:
    def __init__(self):
        self.plat = Grille.genere_grille(10)
        

    def joue(self, position: tuple):
        """ Joue la case de la grille à la position. Si il y avait un bateau, alors case = -1, sinon rien ne se passe.
        
        Args:
            position: tuple (ligne, col) qui désigne la case à jouer
        """
        ligne, col = position
        
        #cas vide
        if self.plat[ligne][col] == 0:
            return
        
        self.plat[ligne][col] = -1
        return

    def victoire(self) -> bool:
        """Retourne True si il n'y a plus de bateau dans la grille

        Return:
            Un booléen True si toutes les cases vaut -1 ou 0 (plus de bateaux restants)
        """
        
        for ligne in range(0, self.plat.n):
            #si différent de -1 et 0
            if not np.all(self.plat.grille[ligne] <= 0): 
                return False
        return True
        
    
if __name__ == "__main__":
    bat = Bataille()
    bat.plat.affiche()
    print(bat.victoire())