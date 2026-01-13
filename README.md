# OptimizarPC para Big Data

Este proyecto es una herramienta integral para auditar y visualizar los recursos de tu sistema (CPU, Memoria, Disco) con el objetivo de determinar si tu PC está preparado para cargas de trabajo de **Big Data** (Hadoop, Spark, Docker, etc.).

## 🚀 Características

*   **Monitorización en Tiempo Real:** Script de Python que captura el estado actual del hardware.
*   **Reporte Histórico:** Guarda automáticamente los datos en `reporte_sistema.txt`.
*   **Dashboard Web:** Una interfaz web moderna (Flask) que analiza tus datos y te ofrece:
    *   **Índice de Potencia:** Un velocímetro visual que califica tu PC del 0 al 100%.
    *   **Comparativa Versus:** Tabla que enfrenta tu hardware contra un Servidor Ideal de Big Data.
    *   **Exportación PDF:** Descarga tu reporte completo con un solo clic.
    *   Recomendaciones de compra de hardware (RAM, CPU, SSD).
*   **Soporte Multiplataforma:** Detecta correctamente procesadores en Windows, macOS y Linux.

## 📦 Instalación

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/alxz0212/OptimizarPC.git
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Uso en Windows

### Generar Ejecutable (.exe)
Hemos automatizado el proceso de compilación. Simplemente ejecuta:

```bash
python build.py
```

Esto creará el archivo `OptimizarPC.exe` dentro de la carpeta `dist/`.

**Ubicación del ejecutable:**
Una vez finalizado el proceso, podrás encontrar el archivo `.exe` en una ruta similar a esta (dependiendo de dónde clonaste el proyecto):

> `C:\Users\TuUsuario\PycharmProjects\OptimizarPC\dist\OptimizarPC.exe`

## 🍎 Uso en macOS (Mac)

Dado que los archivos `.exe` son exclusivos de Windows, en una Mac debes ejecutar el script directamente desde la terminal. El código ya está optimizado para detectar procesadores Intel y Apple Silicon (M1/M2/M3).

1.  Abre tu Terminal.
2.  Navega a la carpeta del proyecto.
3.  Ejecuta el monitor:
    ```bash
    python3 main.py
    ```
    *(Esto generará el archivo `reporte_sistema.txt`)*

4.  Para ver el Dashboard Web:
    ```bash
    python3 app.py
    ```

### Crear una aplicación ejecutable en Mac (Opcional)
Si deseas crear un ejecutable independiente para Mac (un archivo binario Unix), puedes usar PyInstaller desde tu Mac:

```bash
pyinstaller --onefile --name=OptimizarPC --clean main.py
```
El ejecutable resultante estará en la carpeta `dist/` (será un archivo sin extensión `.exe`).

## 📊 Visualización Web (Dashboard)

Para ver el análisis gráfico y las recomendaciones de experto:

1.  Asegúrate de tener un archivo `reporte_sistema.txt` (se genera al ejecutar el monitor).
2.  Ejecuta la aplicación web:
    ```bash
    python app.py
    ```
3.  Abre tu navegador en: `http://127.0.0.1:5000`
4.  **Exportar a PDF:** Haz clic en el botón "Descargar Reporte PDF" en la parte superior para guardar tu análisis.

## 📂 Estructura del Proyecto

*   **`main.py`**: El motor de monitorización. Captura datos de `psutil` y detecta hardware (Windows/Mac/Linux).
*   **`build.py`**: Script de automatización (Windows). Ejecuta el análisis y compila el `.exe`.
*   **`app.py`**: Servidor web Flask. Lee el reporte y muestra la web con recomendaciones.
*   **`templates/index.html`**: La interfaz visual con Bootstrap, alertas y consejos.
*   **`dist/`**: Carpeta donde se generan los ejecutables.

## 💡 Recomendaciones Incluidas

El sistema analiza automáticamente si necesitas:
*   Más memoria RAM (crítico para Spark).
*   Un procesador con más núcleos (para paralelismo).
*   Almacenamiento rápido (NVMe).
*   **SSD Externo:** Se incluye una sección especial sobre cómo usar discos externos para manejar Terabytes de datos sin saturar tu sistema operativo.
