from typing import Dict

# Types des bateaux
PORTE_AVION: int = 1
CROISEUR: int = 2
CONTRE_TORPILLEURS: int = 3
SOUS_MARIN: int = 4
TORPILLEUR: int = 5

# Taille des bateaux
BAT_CASES: Dict[int, int] = {PORTE_AVION: 5, CROISEUR: 4, CONTRE_TORPILLEURS: 3, SOUS_MARIN: 3, TORPILLEUR: 2}

# Tous les bateaux rangés par leurs tailles de manière décroissante
BATEAUX = [PORTE_AVION, CROISEUR, CONTRE_TORPILLEURS, SOUS_MARIN, TORPILLEUR]

# Marquage de la case vide
VIDE: int = 0

# Simulation du jeu
BAT_TOUCHE = -1
RATE = -2

# Directions
HOR: int = 1
VER: int = 2
