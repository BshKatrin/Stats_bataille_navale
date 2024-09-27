import pandas as pd
import numpy as np
from joueur import Joueur

# DATA GENERATION
if __name__ == '__main__':
    j = Joueur("Joueur")
    nb_jeux = 20
    resultats_jeux = np.array([0] * 101)

    # count_jeux = [0] * 101
    for i in range(10000):
        nb_coup = j.jouer(10)
        # print(nb_coup)
        resultats_jeux[nb_coup] += 1
    df = pd.DataFrame(resultats_jeux)
    df.to_csv('data.csv')
