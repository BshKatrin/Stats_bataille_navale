from random import randint
from math import floor
import numpy as np

class ObjPerdu:
    def __init__(self, n: int, ps: float): 
        self.grille_proba = np.zeros((n, n), dtype=float) 
        self.ps = ps 
        self.n = n

        #placement de l'objet
        self.obj_pos = (randint(0, n-1), randint(0, n-1))

    def init_proba_uniform(self):
        """Initialise la grille_proba avec les probabilités de chaque case de manière uniforme"""
        prob = (1/(self.n)**2)

        for ligne in range(self.n):
            for col in range(self.n):
                self.grille_proba[ligne][col] = prob
        return
    
    def init_proba_center(self):
        """Initialise la grille_prob avec une probabilité élevée au centre et faible aux bords de la grille
        Hypothese: self.n > 2

        Répartition des probabilités
        Somme proba pi des bords = 0.2
        Somme proba pi des centres = 0.8

        Les bords de la grille représentent 2/3 des lignes et des colonnes de la grille
        """
        longb = self.n//3 #longueur d'un bord
        nb_cases_bords = 2*(self.n*longb) + 2*(self.n - 2*longb)

        proba_bord = 0.2/nb_cases_bords
        proba_centre = 0.8/(self.n**2 - nb_cases_bords)

        for ligne in range(self.n):
            for col in range(self.n):
                if (ligne < longb or self.n - longb <= ligne) or (col < longb or self.n - longb <= col):
                    self.grille_proba[ligne][col] = proba_bord
                else:
                    self.grille_proba[ligne][col] = proba_centre
        return
    
    def init_proba_bords(self):
        """Initialise la grille_prob avec une probabilité élevée au centre et faible aux bords de la grille
        Hypothese: self.n > 2

        Répartition des probabilités
        Somme proba pi des bords = 0.8
        Somme proba pi des centres = 0.2

        Nombre de cases aux bords: 2*self.n + 2*(self.n - 2)
        """
        longb = self.n//3 #longueur du bord
        nb_cases_bords = 2*(self.n*longb) + 2*(self.n - 2*longb)

        proba_bord = 0.8/nb_cases_bords
        proba_centre = 0.2/(self.n**2 - nb_cases_bords)

        for ligne in range(self.n):
            for col in range(self.n):
                if (ligne < longb or self.n - longb <= ligne) or (col < longb or self.n - longb <= col):
                    self.grille_proba[ligne][col] = proba_bord
                else:
                    self.grille_proba[ligne][col] = proba_centre
        return

    def senseur(self, position: tuple[int, int]) -> int: #done
        """Fonction qui va renvoyer la réponse du senseur: 
        Renvoie 0 si la case est vide
        Renvoie 1 avec une proba ps si la case contient l'objet, 0 sinon"""

        if position == self.obj_pos:
            return 1 if randint(0, 100)/100 < self.ps else 0 
        return 0

    def maj_grille_prob(self, position: tuple[int, int]):
        """Fonction qui met à jour la grille de proba après visite d'une case et le senseur a renvoyé 0.
        Args:
            position: (ligne, col) de la case visité
        """
        
        ligne, col = position
        pi_k = self.grille_proba[ligne][col] 

        proba_y1_z0 = ((1 - self.ps)*pi_k) / (1 - pi_k*self.ps)

        #on redistribue la difference de proba sur les autres cases
        diff_div = (pi_k - proba_y1_z0)/(self.n**2-1)

        #pik <- P(Y=1|Z=0)
        self.grille_proba[ligne][col] = proba_y1_z0

        #on redistribue
        for i in range(0, self.n):
            for j in range(0, self.n):
                if (i, j) != position:
                    self.grille_proba[i][j] += diff_div
        return 

    def tmp_sum(self):
        """somme de grille proba"""
        count = 0.0
        for i in range(self.n):
            for j in range(self.n):
                count += self.grille_proba[i][j]
        return count

    def max_proba_grille(self, old_pos: tuple[int, int] = (0, 0))-> tuple[int, int]: #done
        """Fonction qui cherche la probabilité maximum dans le tableau de probabilité 
        et renvoie la position de la case avec cette proba max

        Args:
            old_pos: position (ligne, col) de la case avec proba max avant MAJ de la grille
        
        Returns:
            Renvoie nouvelle position (ligne, col) de la case avec proba max
        """

        ligne, col = old_pos
        new_pos = (ligne, col)
        
        val_max = self.grille_proba[ligne][col]

        for i in range(self.n):
            for j in range(self.n):
                if self.grille_proba[i][j] > val_max:
                    new_pos = (i, j)
                    val_max = self.grille_proba[i][j]

                if self.grille_proba[i][j] == val_max:
                    #cas égalité pour ne pas prendre la premiere case cas uniforme
                    if (randint(0,100)/100<0.1):
                        new_pos = (i, j)
        return new_pos

    def recherche(self)->int:
        """Algorithme qui va chercher l'objet perdu dans la grille et renvoie le nombre de cases cherchées avant
        de trouver l'objet

        Returns:
            int: le nombre de cases visitées pendant la recherche  
        """

        count = 1
        ligne_max, col_max = self.max_proba_grille()

        while not (self.senseur((ligne_max, col_max))):     
            self.maj_grille_prob((ligne_max, col_max))                          #MAJ grille proba
            ligne_max, col_max = self.max_proba_grille((ligne_max, col_max))    #nouvelle case à choisir
            count += 1
    
        return count

if __name__ == '__main__':
    
    jeu = ObjPerdu(20, 0.5)
    jeu.init_proba_center()
    print(jeu.grille_proba)
    
    """
    for j in [0.1, 0.3, 0.5, 0.7, 0.9]:
        count = 0
        print("for :", j)
        jeu = ObjPerdu(20, j)
        jeu.init_proba_uniform()
        for i in range(1000):
            count += jeu.recherche()   
        print("nb coups pour ", j, " uniform ",count/1000)"""
        