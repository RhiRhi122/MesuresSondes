# find_devices.py
import pyvisa

def main():
    rm = pyvisa.ResourceManager()
    print("Appareils connectés :")
    for device in rm.list_resources():
        print(f"- {device}")

if __name__ == "__main__":
    main()