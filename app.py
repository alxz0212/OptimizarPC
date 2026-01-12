from flask import Flask, render_template
import os
import re

app = Flask(__name__)

def parse_last_report(filepath):
    """Lee el archivo y extrae el último bloque de reporte."""
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    reports = content.split("#################### REPORTE:")
    if len(reports) < 2:
        return None
    
    last_report = reports[-1]
    
    data = {
        "timestamp": last_report.split("\n")[0].strip(),
        "cpu_cores": 0,
        "ram_total_gb": 0.0,
        "disk_free_gb": 0.0,
        "raw_text": last_report
    }

    # CPU
    cpu_match = re.search(r"Total núcleos:\s+(\d+)", last_report)
    if cpu_match:
        data["cpu_cores"] = int(cpu_match.group(1))

    # RAM
    ram_match = re.search(r"Total:\s+([\d\.]+)([KMGTP]?B)", last_report)
    if ram_match:
        val = float(ram_match.group(1))
        unit = ram_match.group(2)
        if unit == "GB":
            data["ram_total_gb"] = val
        elif unit == "MB":
            data["ram_total_gb"] = val / 1024
        elif unit == "TB":
            data["ram_total_gb"] = val * 1024

    # Disco Libre
    disk_matches = re.findall(r"Libre:\s+([\d\.]+)([KMGTP]?B)", last_report)
    total_free_gb = 0
    for val_str, unit in disk_matches:
        val = float(val_str)
        if unit == "GB":
            total_free_gb += val
        elif unit == "MB":
            total_free_gb += val / 1024
        elif unit == "TB":
            total_free_gb += val * 1024
    data["disk_free_gb"] = total_free_gb

    return data

def get_hardware_upgrades(data):
    """Genera sugerencias de compra/mejora de hardware."""
    upgrades = []

    # RAM
    if data["ram_total_gb"] < 16:
        upgrades.append({
            "component": "Memoria RAM",
            "priority": "Alta",
            "suggestion": "Añadir módulos para llegar al menos a 16GB (idealmente 32GB). Busca DDR4 o DDR5 según tu placa."
        })
    elif data["ram_total_gb"] < 32:
        upgrades.append({
            "component": "Memoria RAM",
            "priority": "Media",
            "suggestion": "Si vas a usar Spark o máquinas virtuales, amplía a 32GB o 64GB."
        })

    # Disco
    if data["disk_free_gb"] < 250:
        upgrades.append({
            "component": "Almacenamiento (SSD)",
            "priority": "Alta",
            "suggestion": "Te queda poco espacio. Compra un SSD NVMe M.2 de 1TB o 2TB para velocidad en lectura de datos."
        })
    
    # CPU
    if data["cpu_cores"] < 6:
        upgrades.append({
            "component": "Procesador (CPU)",
            "priority": "Media/Alta",
            "suggestion": "Tu CPU tiene pocos núcleos para paralelismo. Busca un i7/i9 o Ryzen 7/9 compatible con tu placa base."
        })

    # SSD Externo (Siempre sugerido como plus)
    upgrades.append({
        "component": "SSD Externo (USB-C / Thunderbolt)",
        "priority": "Plus Recomendado",
        "suggestion": "Ideal para almacenar datasets masivos sin llenar tu disco principal. Úsalo para backups fríos o datasets históricos."
    })

    if not upgrades:
        upgrades.append({
            "component": "Todo correcto",
            "priority": "Baja",
            "suggestion": "Tu hardware base es sólido. Invierte en un segundo monitor o mejor refrigeración."
        })

    return upgrades

def generate_analysis(data):
    recs = []
    score = 0
    
    # RAM
    if data["ram_total_gb"] >= 32:
        recs.append({"type": "success", "msg": "RAM Excelente (>32GB)."})
        score += 3
    elif data["ram_total_gb"] >= 16:
        recs.append({"type": "warning", "msg": "RAM Decente (16GB)."})
        score += 2
    else:
        recs.append({"type": "danger", "msg": "RAM Insuficiente (<16GB)."})
        score += 1

    # CPU
    if data["cpu_cores"] >= 8:
        recs.append({"type": "success", "msg": "CPU Potente (>8 núcleos)."})
        score += 3
    elif data["cpu_cores"] >= 4:
        recs.append({"type": "warning", "msg": "CPU Estándar (4-6 núcleos)."})
        score += 2
    else:
        recs.append({"type": "danger", "msg": "CPU Limitada."})
        score += 1

    # Disco
    if data["disk_free_gb"] > 500:
        recs.append({"type": "success", "msg": "Buen espacio en disco."})
        score += 3
    elif data["disk_free_gb"] > 100:
        recs.append({"type": "warning", "msg": "Espacio en disco moderado."})
        score += 2
    else:
        recs.append({"type": "danger", "msg": "Poco espacio en disco."})
        score += 1

    return recs, score

@app.route('/')
def index():
    report_path = "reporte_sistema.txt"
    data = parse_last_report(report_path)
    
    if not data:
        return render_template('index.html', error="No se encontró reporte_sistema.txt")

    recommendations, score = generate_analysis(data)
    upgrades = get_hardware_upgrades(data)
    
    # Veredicto y Conclusión
    if score >= 8:
        verdict = "LISTO PARA BIG DATA"
        verdict_class = "text-success"
        conclusion = "Tu equipo es una máquina potente. Puedes desplegar clústeres locales de Hadoop/Spark y entrenar modelos de Machine Learning sin problemas graves de rendimiento."
    elif score >= 5:
        verdict = "APTO PARA APRENDIZAJE"
        verdict_class = "text-warning"
        conclusion = "Tu equipo sirve para aprender y desarrollar prototipos. Sin embargo, si intentas procesar Terabytes de datos o levantar muchos contenedores Docker a la vez, notarás lentitud."
    else:
        verdict = "NECESITA ACTUALIZACIÓN"
        verdict_class = "text-danger"
        conclusion = "Actualmente tu equipo sufrirá con cargas de trabajo de Big Data. Se recomienda encarecidamente actualizar la RAM y el disco antes de empezar proyectos serios."

    tools = [
        {"name": "Docker Desktop", "desc": "Contenedores para Hadoop/Spark."},
        {"name": "Anaconda", "desc": "Entornos de Data Science."},
        {"name": "WSL 2", "desc": "Linux dentro de Windows."},
        {"name": "DBeaver", "desc": "Gestor de Bases de Datos."},
        {"name": "Visual Studio Code", "desc": "Editor de código."}
    ]

    # Información extra sobre SSD Externo
    ssd_info = {
        "title": "Beneficios de un SSD Externo para Big Data",
        "benefits": [
            "Portabilidad: Lleva tus datasets (GBs o TBs) a cualquier lugar sin depender de la nube.",
            "Velocidad: Con USB 3.2 o Thunderbolt, las velocidades de lectura/escritura son casi nativas.",
            "Seguridad: Mantén tus datos sensibles desconectados cuando no trabajes.",
            "Espacio: Evita llenar tu disco principal (C:) con logs y archivos temporales masivos."
        ],
        "usage": "Conéctalo y configura tus herramientas (Hadoop/Spark) para que lean los datos directamente desde la unidad externa (ej. D:/datasets).",
        "recommendation": "Busca modelos como Samsung T7 o SanDisk Extreme."
    }

    return render_template('index.html', 
                           data=data, 
                           recs=recommendations, 
                           upgrades=upgrades,
                           verdict=verdict, 
                           verdict_class=verdict_class, 
                           conclusion=conclusion,
                           tools=tools,
                           ssd_info=ssd_info)

if __name__ == '__main__':
    app.run(debug=True)
