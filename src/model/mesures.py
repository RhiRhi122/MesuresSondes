import json
import re
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from src.model.isolation import IsolationTester, ResultatIsolement
import random

# ==================== CLASSES DE DONNÉES ====================

@dataclass
class TypeSonde:
    """Représente un type de sonde avec ses caractéristiques."""
    pattern: str
    type: str
    valeur_cible: float
    ecart_acceptable: float

@dataclass
class Mesure:
    """Représente une mesure effectuée."""
    id_sondes: str
    type: str
    valeur: float
    statut: str
    poste: str
    type_sonde: str
    operateur: str
    date_heure: str

# ==================== CLASSES PRINCIPALES ====================

class GestionnaireTypesSondes:
    """Gère le chargement et la détection des types de sondes avec patterns exacts."""

    def __init__(self, config_dir: Path = None):
        """Initialise avec le chemin vers le répertoire config."""
        if config_dir is None:
            config_dir = Path(__file__).resolve().parent.parent.parent / "config"
        self.config_dir = config_dir
        self.config_path = config_dir / "types_sondes.json"
        self.types: Dict[str, TypeSonde] = self._charger_types()

    def _charger_types(self) -> Dict[str, TypeSonde]:
        """Charge les types de sondes depuis le fichier JSON."""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            print(f"📂 Fichier types_sondes.json chargé: {self.config_path}")

            types = {}
            for pattern, data in config.items():
                # Convertit le pattern en regex (remplace xxx par \d+)
                regex_pattern = pattern.replace("xxx", r"\d+")
                types[pattern] = TypeSonde(
                    pattern=regex_pattern,
                    type=data["type"],
                    valeur_cible=float(data["valeur_cible"]),
                    ecart_acceptable=float(data["ecart_acceptable"])
                )
            print(f"🔧 {len(types)} types de sondes chargés:")
            for pattern, t in types.items():
                print(f"   - {pattern} → {t.type}")
            return types
        except FileNotFoundError:
            print(f"❌ Fichier introuvable: {self.config_path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Fichier JSON invalide: {self.config_path}")
            return {}
        except Exception as e:
            print(f"❌ Erreur lors du chargement des types de sondes: {e}")
            return {}

    def detecter_type(self, id_sonde: str) -> Optional[TypeSonde]:
        """Détecte le type de sonde à partir de son ID en utilisant les patterns."""
        if not id_sonde:
            print("⚠️ ID de sonde vide!")
            return None

        # Teste chaque pattern pour trouver une correspondance
        for pattern, type_info in self.types.items():
            if re.fullmatch(type_info.pattern, id_sonde):
                return type_info

        print(f"❌ Aucun type trouvé pour la sonde: {id_sonde}")
        print(f"   Patterns disponibles: {list(self.types.keys())}")
        return None

class MesureResistance:
    """Représente une mesure de résistance avec simulation et test d'isolement."""

    def __init__(
        self,
        id_sondes: str,
        type_mesure: str,
        poste: str,
        operateur: str,
        gestionnaire_types: GestionnaireTypesSondes,
        isolation_tester: IsolationTester = None
    ):
        self.id_sondes = id_sondes
        self.type_mesure = type_mesure
        self.poste = poste
        self.operateur = operateur
        self.gestionnaire_types = gestionnaire_types
        self.type_sonde = self.gestionnaire_types.detecter_type(id_sondes)
        self.isolation_tester = isolation_tester or IsolationTester(simulateur=True)

    def simuler_mesure(self) -> tuple[Mesure, ResultatIsolement]:
        """Simule une mesure avec détection automatique du type et test d'isolement."""
        if not self.type_sonde:
            raise ValueError(f"Type de sonde inconnu pour {self.id_sondes}")

        # Mesure de résistance
        valeur_resistance = random.uniform(
            self.type_sonde.valeur_cible - self.type_sonde.ecart_acceptable,
            self.type_sonde.valeur_cible + self.type_sonde.ecart_acceptable
        )

        # Test d'isolement
        resultat_isolement = self.isolation_tester.mesurer_isolement(
            self.id_sondes, self.operateur
        )

        # Détermine les statuts
        statut_resistance = "OK" if abs(valeur_resistance - self.type_sonde.valeur_cible) <= self.type_sonde.ecart_acceptable else "ERREUR"

        mesure = Mesure(
            id_sondes=self.id_sondes,
            type=self.type_mesure,
            valeur=valeur_resistance,
            statut=statut_resistance,
            poste=self.poste,
            type_sonde=self.type_sonde.type,
            operateur=self.operateur,
            date_heure=self._get_date_heure()
        )

        return mesure, resultat_isolement

    def _get_date_heure(self) -> str:
        """Retourne la date et heure actuelle au format lisible."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Poste:
    """Représente un poste de mesure avec ses sondes."""

    def __init__(self, nom: str, gestionnaire_types: GestionnaireTypesSondes):
        self.nom = nom
        self.gestionnaire_types = gestionnaire_types
        self.sondes = self._charger_sondes()

    def _charger_sondes(self) -> List[MesureResistance]:
        """Charge la liste des sondes pour ce poste."""
        config_path = Path(__file__).resolve().parent.parent.parent / "config" / "postes.json"

        try:
            with open(config_path) as f:
                postes_config = json.load(f)
            print(f"📂 Fichier postes.json chargé: {config_path}")
        except FileNotFoundError:
            print(f"❌ Fichier introuvable: {config_path}")
            return []
        except json.JSONDecodeError:
            print(f"❌ Fichier JSON invalide: {config_path}")
            return []
        except Exception as e:
            print(f"❌ Erreur lors du chargement des postes: {e}")
            return []

        sondes_config = postes_config.get(self.nom, {}).get("sondes", [])
        print(f"📊 {len(sondes_config)} sondes configurées pour le poste {self.nom}")

        return [
            MesureResistance(
                id_sondes=id_sonde,
                type_mesure="resistance_4fils",
                poste=self.nom,
                operateur="",
                gestionnaire_types=self.gestionnaire_types
            )
            for id_sonde in sondes_config
        ]

