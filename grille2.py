import numpy
from random import randint
from bateau import BAT_CASE


class Grille:
    def __init__(self, n:int)->None:
        self.grille = numpy.zeros((n,n), dtype = numpy.int8)
    

    def peut_placer(self, grille, bateau: int, position: tuple, direction: int)-> bool:
        """
        Renvoie True si peut placer le bateau sur la grille, False sinon.

        Args:
            grille: n*n à valeurs [0, 5]
            bateau: [1, 5]
            position: tuple (ligne, col)
                la position concerne la partie la plus a gauche ou la partie la plus en haut du bateau
            direction: 1 horizontale, 2 verticale
        """

        ligne, col = position 
        taille_g = len(grille)
        taille_bat = BAT_CASE[bateau]   

        #cas horizontale
        if direction == 1:

            #cas tout a droite
            if ligne == taille_g-1: 
                return False

            #on verifie si il y a de la place pour le bateau
            if taille_g - col < taille_bat:
                return False

            #on verifie si les cases sont libres
            for i in range(col, col + taille_bat):
                if grille[ligne][i] != 0:
                    return False
            
            return True


        #cas verticale
        if direction == 2:

            #cas tout en bas
            if col == taille_g-1: 
                return False

            #on verifie si il y a de la place pour le bateau
            if taille_g - ligne < BAT_CASE[bateau]:
                return False
            
            #on verifie si les cases sont libres
            for i in range(ligne, ligne + taille_bat):
                if grille[i][col] != 0:
                    return False
            
            return True


    def place(self, grille, bateau: int, position: tuple, direction: int):
        """
        Renvoie la grille avec le bateau placé dessus.

        Args:
            grille: n*n à valeurs [0, 5]
            bateau: [1, 5]
            position: tuple (ligne, col)
                la position concerne la partie la plus a gauche ou la partie la plus en haut du bateau
            direction: 1 horizontale, 2 verticale
        """

        ligne, col = position
        taille_bat = BAT_CASE[bateau] 

        #cas horizontale
        if direction == 1:
            for i in range(col, col + taille_bat):
                grille[ligne][i] = bateau

        #cas verticale
        if direction == 2:
            for i in range(ligne, ligne + taille_bat):
                grille[i][col] = bateau
        
        return grille


    def place_alea(self, grille, bateau: int)-> None:
        """Place le bateau aléatoirement dans la grille."""

        taille = len(grille)
    
        while True:
            position = (randint(0, taille), randint(0, taille))
            direction = randint(1,2)

            if self.peut_placer(self.grille, bateau, position, direction) == True:
                self.grille = self.place(grille, bateau, position, direction)
                break
        
        return


            


                






