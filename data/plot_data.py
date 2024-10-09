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
    data = pd.read_csv('data/data.csv', sep=',', header=None)
    nb_jeux = 10000
    b, n = 17, 100

    fig, ax = plt.subplots()

    nb_coups = data.iloc[:, 0]
    proba_data = np.array([val / nb_jeux for val in np.array(data.iloc[:, 1])])

    ax.plot(nb_coups, proba_data, 'b', label='Données')

    ax.set_xlim(17, 100)
    ax.set_ylim(0, max(proba_data))

    # Espérance
    esp = int(calc_esp_formule(b, n))
    proba_esp = calc_proba(esp, b, n)

    x_esp = np.arange(b, esp+1, 1)
    # Ligne horizontale
    y_esp_hor = np.array([proba_esp] * len(x_esp))
    ax.plot(x_esp, y_esp_hor, '--r')
    # Ligne verticale
    ax.vlines(x=x_esp[-1], ymin=0, ymax=proba_esp, linestyles='dashed', colors='r')
    # Point
    ax.plot(esp, proba_esp, 'r.', label="Espérance")

    ax.set_xticks(np.append(np.arange(20, 100+1, 10), esp))

    # Probabilité calculée
    x_modelisation = np.arange(b, n + 1, 1)
    y_modelisation = np.array([calc_proba(i, b, n) for i in x_modelisation])
    ax.plot(x_modelisation, y_modelisation, 'gray', label='Modélisation')

    ax.set_title('Distribution de la variable aléatoire X (10000 jeux)')
    ax.set_xlabel('Nombre de coups i')
    ax.set_ylabel('Probabilité P(X = i)')
    ax.legend()

    plt.show()
