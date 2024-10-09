import pandas as pd
import numpy as np
from joueur import Joueur

# DATA GENERATION
if __name__ == '__main__':
    j = Joueur("Joueur")
    resultats_jeux = np.array([0] * 101)

    for i in range(10000):
        nb_coup = j.jouer_heuristique(10)
        print(i, nb_coup)
        # nb_coup = j.jouer_strat(10)
        resultats_jeux[nb_coup] += 1

    df = pd.DataFrame(resultats_jeux)
    df.to_csv('data_1.csv')
