import psutil
import platform
import os
import time
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info_str():
    lines = []
    lines.append("="*40 + " Información del Sistema " + "="*40)
    uname = platform.uname()
    lines.append(f"Sistema: {uname.system}")
    lines.append(f"Nombre del nodo: {uname.node}")
    lines.append(f"Release: {uname.release}")
    lines.append(f"Versión: {uname.version}")
    lines.append(f"Máquina: {uname.machine}")
    lines.append(f"Procesador: {uname.processor}")
    return "\n".join(lines)

def get_cpu_info_str():
    lines = []
    lines.append("="*40 + " Información de CPU " + "="*40)
    lines.append(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    lines.append(f"Total núcleos: {psutil.cpu_count(logical=True)}")
    cpufreq = psutil.cpu_freq()
    if cpufreq:
        lines.append(f"Frecuencia Máxima: {cpufreq.max:.2f}Mhz")
        lines.append(f"Frecuencia Actual: {cpufreq.current:.2f}Mhz")
    lines.append(f"Uso de CPU: {psutil.cpu_percent()}%")
    return "\n".join(lines)

def get_memory_info_str():
    lines = []
    lines.append("="*40 + " Información de Memoria " + "="*40)
    svmem = psutil.virtual_memory()
    lines.append(f"Total: {get_size(svmem.total)}")
    lines.append(f"Disponible: {get_size(svmem.available)}")
    lines.append(f"Usada: {get_size(svmem.used)}")
    lines.append(f"Porcentaje: {svmem.percent}%")
    return "\n".join(lines)

def get_disk_info_str():
    lines = []
    lines.append("="*40 + " Información del Disco " + "="*40)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        lines.append(f"Dispositivo: {partition.device}")
        lines.append(f"  Punto de montaje: {partition.mountpoint}")
        lines.append(f"  Tipo de sistema de archivos: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        lines.append(f"  Total: {get_size(partition_usage.total)}")
        lines.append(f"  Usado: {get_size(partition_usage.used)}")
        lines.append(f"  Libre: {get_size(partition_usage.free)}")
        lines.append(f"  Porcentaje: {partition_usage.percent}%")
    return "\n".join(lines)

def generate_snapshot():
    """Genera el texto del reporte y lo guarda."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_header = f"\n{'#'*20} REPORTE: {timestamp} {'#'*20}\n"
    
    sys_info = get_system_info_str()
    cpu_info = get_cpu_info_str()
    mem_info = get_memory_info_str()
    dsk_info = get_disk_info_str()
    
    full_report = f"{report_header}\n{sys_info}\n{cpu_info}\n{mem_info}\n{dsk_info}"
    
    # Guardar
    with open("reporte_sistema.txt", "a", encoding="utf-8") as f:
        f.write(full_report + "\n\n")
        
    return full_report

def main():
    print("Iniciando monitorización... (Guardando en reporte_sistema.txt)")
    while True:
        clear_screen()
        
        # Generamos y guardamos usando la función compartida
        full_report = generate_snapshot()
        print(full_report)
        
        print("\nInformación guardada en 'reporte_sistema.txt'")
        print("Presiona Ctrl+C para salir.")
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
