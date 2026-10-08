import sys
from pathlib import Path

# Ajoute le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.model.mesures import Poste, MesureResistance, GestionnaireTypesSondes

def main():
    """Fonction principale pour tester les mesures."""
    print("🔧 Initialisation du système de mesure...")
    print("-" * 70)

    # Initialisation du gestionnaire de types de sondes
    gestionnaire_types = GestionnaireTypesSondes()

    # Création du poste avec le gestionnaire de types
    poste_abe = Poste("SP", gestionnaire_types)

    # Vérification que des sondes ont été chargées
    if not poste_abe.sondes:
        print("❌ Aucune sonde chargée pour ce poste!")
        return

    # Lancement des mesures
    print(f"\n📊 Mesures pour le poste {poste_abe.nom} ({len(poste_abe.sondes)} sondes):")
    print("-" * 70)

    for sonde in poste_abe.sondes:
        sonde.operateur = "RhiRhi"
        try:
            resultat = sonde.simuler_mesure()
            print(f"🔹 Sonde: {resultat.id_sondes}")
            print(f"   Type: {resultat.type_sonde}")
            print(f"   Valeur: {resultat.valeur:.2f} Ω")
            print(f"   Statut: {'✅ OK' if resultat.statut == 'OK' else '❌ ERREUR'}")
            print(f"   Opérateur: {resultat.operateur}")
            print(f"   Date/Heure: {resultat.date_heure}")
            print("-" * 70)
        except Exception as e:
            print(f"❌ Erreur lors de la mesure de {sonde.id_sondes}: {e}")
            print("-" * 70)

if __name__ == "__main__":
    main()