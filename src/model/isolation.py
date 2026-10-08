import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import time

@dataclass
class ResultatIsolement:
    """Représente un résultat de test d'isolement."""
    id_sondes: str
    resistance: float  # en ohms
    statut: str  # "OK" ou "ERREUR"
    limite_min: float = 1000000.0  # 1 Mohm
    operateur: str = ""
    date_heure: str = ""

class IsolationTester:
    """Classe pour gérer les tests d'isolement avec le 34461A."""

    def __init__(self, simulateur: bool = True):
        """
        Initialise le testeur d'isolement.

        Args:
            simulateur: Si True, utilise des valeurs simulées. Si False, utiliserait le vrai 34461A.
        """
        self.simulateur = simulateur
        self.limite_min = 1000000.0  # 1 Mohm

    def mesurer_isolement(self, id_sondes: str, operateur: str = "") -> ResultatIsolement:
        """
        Effectue une mesure d'isolement sur une sonde.

        Args:
            id_sondes: L'identifiant de la sonde (ex: "TX-101")
            operateur: Le nom de l'opérateur

        Returns:
            ResultatIsolement: Le résultat de la mesure
        """
        if not id_sondes:
            raise ValueError("ID de sonde vide!")

        # Simulation ou mesure réelle
        if self.simulateur:
            resistance = self._simuler_mesure_isolement(id_sondes)
        else:
            resistance = self._mesurer_avec_34461A(id_sondes)

        # Détermination du statut
        statut = "OK" if resistance >= self.limite_min else "ERREUR"

        return ResultatIsolement(
            id_sondes=id_sondes,
            resistance=resistance,
            statut=statut,
            operateur=operateur,
            date_heure=self._get_date_heure()
        )

    def _simuler_mesure_isolement(self, id_sondes: str) -> float:
        """Simule une mesure d'isolement avec le 34461A."""
        # Génère une valeur aléatoire autour de 10 Mohm avec une variation possible
        base_value = 10000000.0  # 10 Mohm
        variation = random.uniform(-5000000.0, 5000000.0)  # ±5 Mohm
        return base_value + variation

    def _mesurer_avec_34461A(self, id_sondes: str) -> float:
        """
        Mesure réelle avec le 34461A (à implémenter avec PyVISA ou autre).
        Pour l'instant, retourne une valeur simulée.
        """
        print(f"🔌 Connexion au 34461A pour mesurer {id_sondes}...")
        time.sleep(1)  # Simulation du temps de mesure
        return self._simuler_mesure_isolement(id_sondes)

    def _get_date_heure(self) -> str:
        """Retourne la date et heure actuelle au format lisible."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")