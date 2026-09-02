"""
Script de sincronización automática para el repositorio del laboratorio (Jompy).
Extrae la carpeta del framework como raíz y la publica limpia en la rama sarenv-mts.
"""
import subprocess
import sys

def run_command(cmd, desc):
    print(f"-> {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        return False
    return True

def main():
    print("==================================================")
    print("Sincronizando framework con el repositorio de Jompy")
    print("==================================================")
    
    # 1. Eliminar rama temporal local anterior si existe
    subprocess.run(["git", "branch", "-D", "sarenv-mts-clean"], capture_output=True)
    
    # 2. Extraer subárbol limpio del framework
    ok = run_command(
        ["git", "subtree", "split", "--prefix=framwork-MTS/MTS-UncertainEnvironment-Algoritmos-bioinspirados", "-b", "sarenv-mts-clean"],
        "Extrayendo estructura limpia de MTS"
    )
    if not ok:
        sys.exit(1)
        
    # 3. Subir rama limpia al repositorio de Jompy
    ok = run_command(
        ["git", "push", "lab", "sarenv-mts-clean:sarenv-mts", "--force"],
        "Publicando en GitHub (Jompy-GitHub/MTS-UncertainEnvironment -> sarenv-mts)"
    )
    if not ok:
        sys.exit(1)
        
    print("\nRepositorio de Jompy actualizado con exito.")
    print("Estructura en la raiz: busquedas, sarenv, metrics, TFM_JC, sensor, etc. (sin memoria).")

if __name__ == "__main__":
    main()
