# OptimizarPC

Este proyecto es una herramienta para visualizar los recursos del sistema (CPU, Memoria, Disco) para ayudar en tareas de Big Data.

Además de mostrar la información en pantalla, **guarda automáticamente un historial en `reporte_sistema.txt`**.

## Instalación

1. Asegúrate de tener Python instalado.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Crear el ejecutable (.exe)

Para convertir el script `main.py` en un archivo ejecutable `.exe`, utiliza `pyinstaller`:

```bash
pyinstaller --onefile main.py
```

El archivo ejecutable se generará en la carpeta `dist/`.

## Ejecución

Ejecuta el archivo `main.py` directamente con Python o abre el `.exe` generado en la carpeta `dist`.

Cada 5 segundos, el programa actualizará la pantalla y añadirá una nueva entrada al archivo `reporte_sistema.txt` con la fecha y hora actuales.
