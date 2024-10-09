import matplotlib.pyplot as plt
import numpy as np
from math import comb
import pandas as pd


def calc_esp_sum(b: int, n: int) -> int:
    # Calcul d'espérance à l'aide d'une formule non simplifiée (avec la somme)
    sum = 0
    for i in range(b, n+1):
        up = comb(i-1, b-1)
        low = comb(n, b)
        sum += i * (up / low)
    return sum


def calc_esp_formule(b: int, n: int) -> int:
    # Calcul d'espérance à l'aide d'une formule simplifiée
    return b * comb(n+1, b+1) / comb(n, b)


def calc_proba(i, b, n):
    # Calcul du P(X = i)
    up = comb(i-1, b-1)
    low = comb(n, b)
    return up / low


if __name__ == '__main__':
    # Deux courbes ensemble
    data = pd.read_csv("data/data.csv", sep=',', header=None)    #version aléa
    data2 = pd.read_csv('data/data2.csv', sep=',', header=None)  #version heuristique
    data3 = pd.read_csv('data/data3.csv', sep=',', header=None)  #version proba

    b, n = 17, 100

    fig, ax = plt.subplots()

    nb_coups = data.iloc[:, 0]
    proba_data = np.array([val / 10000 for val in np.array(data.iloc[:, 1])])
    proba_data2 = np.array([val / 10000 for val in np.array(data2.iloc[:, 1])])
    proba_data3 = np.array([val / 1000 for val in np.array(data3.iloc[:, 1])])

    ax.plot(nb_coups, proba_data, 'b', label='Ver. aléatoire (10 000 jeux)')
    ax.plot(nb_coups, proba_data2, 'r', label='Ver. heuristique (10 000 jeux)')
    ax.plot(nb_coups, proba_data3, 'g', label='Ver. proba simple (1000 jeux)')

    ax.set_xlim(17, 100)
    ax.set_ylim(0, max(max(max(proba_data), max(proba_data2)), max(proba_data3)+0.01))
    ax.set_ylim(0, max(max(proba_data), max(proba_data2)))

    ax.set_title('Distribution de la variable aléatoire X')
    ax.set_xlabel('Nombre de coups i')
    ax.set_ylabel('Probabilité P(X = i)')
    ax.legend()

    plt.show()
