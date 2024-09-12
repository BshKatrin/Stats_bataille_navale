import numpy

from random import randint
from bateau import BAT_CASES

class Grille:
    def __init__(self, n:int)->None:
        self.n: int = n
        self.grille = numpy.zeros((n,n), dtype = numpy.int8)
    

    def peut_placer(self, bateau: int, position: tuple, direction: int)-> bool:
        """
        Renvoie True si peut placer le bateau sur la grille, False sinon.

        Args:
            bateau: [1, 5]
            position: tuple (ligne, col)
                la position concerne la partie la plus a gauche ou la partie la plus en haut du bateau
            direction: 1 horizontale, 2 verticale
        """

        ligne, col = position 
        taille_bat = BAT_CASES[bateau]   

        #cas horizontale
        if direction == 1:

            #cas tout a droite
            if ligne == self.n - 1: 
                return False

            #on verifie si il y a de la place pour le bateau
            if self.n - col < taille_bat:
                return False

            #on verifie si les cases sont libres
            for i in range(col, col + taille_bat):
                if self.grille[ligne][i] != 0:
                    return False
            
            return True


        #cas verticale
        if direction == 2:

            #cas tout en bas
            if col == self.n-1: 
                return False

            #on verifie si il y a de la place pour le bateau
            if self.n - ligne < BAT_CASES[bateau]:
                return False
            
            #on verifie si les cases sont libres
            for i in range(ligne, ligne + taille_bat):
                if self.grille[i][col] != 0:
                    return False
            
            return True


    def place(self, bateau: int, position: tuple, direction: int):
        """
        Renvoie la grille avec le bateau placé dessus.

        Args:
            bateau: [1, 5]
            position: tuple (ligne, col)
                la position concerne la partie la plus a gauche ou la partie la plus en haut du bateau
            direction: 1 horizontale, 2 verticale
        """

        ligne, col = position
        taille_bat = BAT_CASES[bateau] 

        #cas horizontale
        if direction == 1:
            for i in range(col, col + taille_bat):
                self.grille[ligne][i] = bateau

        #cas verticale
        if direction == 2:
            for i in range(ligne, ligne + taille_bat):
                self.grille[i][col] = bateau
        
        return self.grille


    def place_alea(self, bateau: int)-> None:
        """Place le bateau aléatoirement dans la grille."""
    
        while True:
            position = (randint(0, self.n), randint(0, self.n))
            direction = randint(1,2)

            if self.peut_placer(bateau, position, direction) == True:
                self.grille = self.place(bateau, position, direction)
                break
        
        return


if __name__ == "__main__":
    g = Grille(10)
    assert(g.peut_placer(5, (0,0), 1)) == True
    g.place(5, (0,0), 1)
    assert(g.peut_placer(5, (0,0), 1)) == False
    assert(g.peut_placer(5, (0,1), 1)) == False
    assert(g.peut_placer(5, (0,2), 1)) == True

    g.place_alea(3)
            


                






