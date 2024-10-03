from random import randint
import numpy as np

class ObjPerdu:
    def __init__(self, n: int, ps: float): 
        self.grille = np.zeros((n, n), dtype=np.int8)
        self.grille_proba = np.zeros((n, n), dtype=float)
        self.ps = ps  
        self.n = n

        #placement de l'objet
        self.obj_pos = (randint(0, n-1), randint(0, n-1))
        self.grille[self.obj_pos[0]][self.obj_pos[1]] = 1 

    def init_proba(self): #autres config done
        """Initialise la grille_proba avec les probabilités de chaque case
        de manière uniforme : pi = 1/nb_cases"""

        prob = 1/(self.n)**2

        for ligne in range(self.n):
            for col in range(self.n):
                self.grille_proba[ligne][col] = prob
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
        proba_y1_z0 = ((1 - self.ps)*pi_k)/(1 - pi_k*self.ps)

        difference = abs(pi_k - proba_y1_z0) #le reste a distribuer aux N-1
        diff_div = difference / (self.n -1)

        #on change proba pik en P(Y=1|Z=0)
        self.grille_proba[ligne][col] = proba_y1_z0

        #on redistribue
        for i in range(0, self.n):
            for j in range(0, self.n):
                if (i==ligne and j==col):
                    pass
                else:
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
        et renvoie la position de la case du tableau avec cette proba max

        Args:
            old_pos: position (ligne, col) de la case avec proba max avant MAJ de la grille
        
        Returns:
            Renvoie (ligne, col) de la case avec proba max     
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
                    #cas égal, pour ne pas prendre la premiere case cas uniforme
                    if (randint(0,100)/100<0.1):
                        new_pos = (i, j)
        return new_pos

    def recherche(self)->int:
        """Algorithme qui va chercher l'objet perdu dans la grille et renvoie le nombre de cases cherchées avant
        de trouver l'objet

        Returns:
            int: le nombre de cases visitées dans la recherche  
        """
        count = 1
        ligne_max, col_max = self.max_proba_grille()

        while not (self.senseur((ligne_max, col_max))):     #tant qu'on ne trouve pas obj
            #print(ligne_max, col_max, "\nbefore maj\n",self.grille_proba, "\n", self.tmp_sum())
            self.maj_grille_prob((ligne_max, col_max))      #MAJ grille proba
            
            ligne_max, col_max = self.max_proba_grille((ligne_max, col_max)) #nouvelle case à choisir
            #print("\n\n apres maj\n",self.grille_proba, "\n",ligne_max, col_max,"\n\n")
            count += 1

        return count

if __name__ == '__main__':
    jeu = ObjPerdu(5, .5)
    print(jeu.grille)
    jeu.init_proba()
    print(jeu.recherche())