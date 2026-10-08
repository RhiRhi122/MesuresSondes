# test_appareil.py
from model.appareils import AppareilKeysight

def test_appareil():
    appareil = AppareilKeysight("USB0::0x0957::0x1807::MY57206438::INSTR")
    if appareil.est_connecte():
        print("✅ Appareil connecté !")
        print(f"ID : {appareil.instrument.query('*IDN?')}")
    else:
        print("❌ Appareil non détecté.")

if __name__ == "__main__":
    test_appareil()