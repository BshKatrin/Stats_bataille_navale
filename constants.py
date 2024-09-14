from typing import Dict


PORTE_AVION: int = 1
CROISEUR: int = 2
CONTRE_TORPILLEURS: int = 3
SOUS_MARIN: int = 4
TORPILLEUR: int = 5

VIDE: int = 0

BAT_CASES: Dict[int, int] = {PORTE_AVION: 5, CROISEUR: 4, CONTRE_TORPILLEURS: 3, SOUS_MARIN: 3, TORPILLEUR: 2}

# Directions
HOR: int = 1
VER: int = 2
