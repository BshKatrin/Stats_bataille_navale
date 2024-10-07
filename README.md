# Statistiques en Informatique.

## Projet 1 : Bataille navale

### Langage utilisée

- Python >= 3.11.4

### Bibliothèques utilisées

- `Pandas` >= 2.1.1
- `Numpy` >= 1.26.4
- `Matplotlib` >= 3.8.0

Si ces bibliothèques ne sont pas installées sur votre ordinateur, on recommande d'utiliser l'environement virtuel avec de les installer.
Il est possible d'optimiser l'installation avec la commande `pip install -r requirements.txt`.

### Structure des fichiers

Le dossier `data` contient les scripts Python et les fichiers avec les données pour les données (les fichiers `.csv`).

- Script `calc_data.py` permet de générer les données
- Scripts `plot_data.py`, `plot_data2_courbes.py` permettent de visualiser les données générées.

Les fichiers `grille.py`, `joueur.py`, `constants.py`, `bataille.py`, `ObjPerdu.py` contient le code principale pour implémenter
le jeu _Bataille navale_ (voir le Rapport pour plus de détails).

#### Commandes

1. Les scripts dans le dossier `data` : `python3 -m data.<nom_fichier>` _(sans .py)_. Par exemple, `python3 -m data.calc_data`.
2. Les fichiers `grille.py`, `joueur.py`, `constants.py`, `bataille.py`, `ObjPerdu.py` peuvent être lancés avec la commande
   `python3 <nom-fichier.py>`. Par exemple, `python3 grille.py`
