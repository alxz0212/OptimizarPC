import PyInstaller.__main__
import main
import os

def build():
    print("--- 1. Generando reporte actualizado del sistema ---")
    # Llamamos a la función de main.py que genera y guarda el reporte
    main.generate_snapshot()
    print("Reporte actualizado en 'reporte_sistema.txt'.")

    print("\n--- 2. Creando ejecutable con PyInstaller ---")
    
    # Ejecutamos PyInstaller desde Python
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--name=OptimizarPC',
        '--clean'
    ])
    
    print("\n--- ¡PROCESO COMPLETADO! ---")
    print(f"El ejecutable está en: {os.path.abspath('dist/OptimizarPC.exe')}")
    print(f"El reporte actualizado está en: {os.path.abspath('reporte_sistema.txt')}")

if __name__ == "__main__":
    build()
