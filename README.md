# OptimizarPC para Big Data

Este proyecto es una herramienta integral para auditar y visualizar los recursos de tu sistema (CPU, Memoria, Disco) con el objetivo de determinar si tu PC está preparado para cargas de trabajo de **Big Data** (Hadoop, Spark, Docker, etc.).

## 🚀 Características

*   **Monitorización en Tiempo Real:** Script de Python que captura el estado actual del hardware.
*   **Reporte Histórico:** Guarda automáticamente los datos en `reporte_sistema.txt`.
*   **Dashboard Web:** Una interfaz web moderna (Flask) que analiza tus datos y te ofrece:
    *   Semáforo de viabilidad para Big Data.
    *   Recomendaciones de compra de hardware (RAM, CPU, SSD).
    *   **Plus:** Guía sobre el uso de SSDs Externos para datasets masivos.
*   **Generador de Ejecutables:** Script automatizado para compilar el programa.

## 📦 Instalación

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/alxz0212/OptimizarPC.git
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Cómo Generar el Ejecutable (.exe)

Hemos automatizado el proceso de compilación para asegurar que siempre tengas los datos más recientes. **Ya no necesitas usar `pyinstaller` manualmente.**

Simplemente ejecuta el script de construcción:

```bash
python build.py
```

Este script realizará dos acciones automáticamente:
1.  **Analiza tu PC:** Genera una instantánea actual de tu sistema y actualiza `reporte_sistema.txt`.
2.  **Compila:** Crea el archivo `OptimizarPC.exe` dentro de la carpeta `dist/`.

> **Nota:** El ejecutable final se llama `OptimizarPC.exe`. Puedes borrar cualquier versión antigua llamada `main.exe`.

## 📊 Visualización Web (Dashboard)

Para ver el análisis gráfico y las recomendaciones de experto:

1.  Asegúrate de tener un archivo `reporte_sistema.txt` (se genera al ejecutar `build.py` o `OptimizarPC.exe`).
2.  Ejecuta la aplicación web:
    ```bash
    python app.py
    ```
3.  Abre tu navegador en: `http://127.0.0.1:5000`

## 📂 Estructura del Proyecto

*   **`main.py`**: El motor de monitorización. Captura datos de `psutil`.
*   **`build.py`**: Script de automatización. Ejecuta el análisis y luego compila el `.exe`.
*   **`app.py`**: Servidor web Flask. Lee el reporte y muestra la web con recomendaciones.
*   **`templates/index.html`**: La interfaz visual con Bootstrap, alertas y consejos.
*   **`dist/OptimizarPC.exe`**: Tu programa portable listo para usar (generado tras correr `build.py`).

## 💡 Recomendaciones Incluidas

El sistema analiza automáticamente si necesitas:
*   Más memoria RAM (crítico para Spark).
*   Un procesador con más núcleos (para paralelismo).
*   Almacenamiento rápido (NVMe).
*   **SSD Externo:** Se incluye una sección especial sobre cómo usar discos externos para manejar Terabytes de datos sin saturar tu sistema operativo.
