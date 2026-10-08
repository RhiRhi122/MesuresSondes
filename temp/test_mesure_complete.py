from pathlib import Path
import sys


# Ajoute le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.model.mesures import Poste, MesureResistance, GestionnaireTypesSondes
from src.model.isolation import IsolationTester

def main():
    """Fonction principale pour tester les mesures complètes (résistance + isolement)."""
    print("🔧 Initialisation du système de mesure complet...")
    print("-" * 70)

    # Initialisation
    gestionnaire_types = GestionnaireTypesSondes()
    isolation_tester = IsolationTester(simulateur=True)

    # Création du poste
    poste_abe = Poste("A-ABE", gestionnaire_types)

    if not poste_abe.sondes:
        print("❌ Aucune sonde chargée pour ce poste!")
        return

    # Lancement des mesures complètes
    print(f"\n📊 Mesures complètes pour le poste {poste_abe.nom} ({len(poste_abe.sondes)} sondes):")
    print("-" * 70)

    for sonde in poste_abe.sondes:
        sonde.operateur = "RhiRhi"
        try:
            # Mesure de résistance
            mesure_resistance, resultat_isolement = sonde.simuler_mesure()

            # Affichage des résultats
            print(f"🔹 Sonde: {mesure_resistance.id_sondes}")
            print(f"   Type: {mesure_resistance.type_sonde}")
            print(f"   Résistance: {mesure_resistance.valeur:.2f} Ω")
            print(f"   Statut résistance: {'✅ OK' if mesure_resistance.statut == 'OK' else '❌ ERREUR'}")

            print(f"   Résistance d'isolement: {resultat_isolement.resistance/1000000:.2f} MΩ")
            print(f"   Statut isolement: {'✅ OK' if resultat_isolement.statut == 'OK' else '❌ ERREUR'}")

            print(f"   Opérateur: {mesure_resistance.operateur}")
            print(f"   Date/Heure: {mesure_resistance.date_heure}")
            print("-" * 70)

        except Exception as e:
            print(f"❌ Erreur lors de la mesure de {sonde.id_sondes}: {e}")
            print("-" * 70)

if __name__ == "__main__":
    main()