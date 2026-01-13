import psutil
import platform
import os
import time
import subprocess
from datetime import datetime
import cpuinfo
import traceback
import multiprocessing

# Variable global para cachear el nombre del procesador y no buscarlo en cada ciclo
_CPU_NAME_CACHE = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_cpu_name():
    global _CPU_NAME_CACHE
    if _CPU_NAME_CACHE:
        return _CPU_NAME_CACHE

    cpu_name = None
    
    # Intento 1: Usar py-cpuinfo (Funciona en Windows, Mac y Linux)
    try:
        info = cpuinfo.get_cpu_info()
        cpu_name = info.get('brand_raw')
    except Exception:
        pass
    
    # Intento 2: Estrategias específicas por sistema operativo si falla el anterior
    if not cpu_name:
        system_name = platform.system()
        
        if system_name == "Windows":
            try:
                command = "wmic cpu get name"
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output = subprocess.check_output(command, startupinfo=startupinfo, shell=False).decode()
                lines = [line.strip() for line in output.split('\n') if line.strip() and line.strip() != 'Name']
                if lines:
                    cpu_name = lines[0]
            except Exception:
                pass
                
        elif system_name == "Darwin": # macOS
            try:
                # Comando nativo de macOS para obtener el nombre exacto del CPU
                command = "sysctl -n machdep.cpu.brand_string"
                output = subprocess.check_output(command, shell=True).decode().strip()
                if output:
                    cpu_name = output
            except Exception:
                pass
                
        elif system_name == "Linux":
            try:
                # Intentar leer /proc/cpuinfo en Linux
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_name = line.split(":")[1].strip()
                            break
            except Exception:
                pass

    # Fallback: Usar información básica genérica
    if not cpu_name:
        uname = platform.uname()
        cpu_name = uname.processor
    
    _CPU_NAME_CACHE = cpu_name
    return cpu_name

def get_system_info_str():
    lines = []
    lines.append("="*40 + " Información del Sistema " + "="*40)
    uname = platform.uname()
    lines.append(f"Sistema: {uname.system}")
    lines.append(f"Nombre del nodo: {uname.node}")
    lines.append(f"Release: {uname.release}")
    lines.append(f"Versión: {uname.version}")
    lines.append(f"Máquina: {uname.machine}")
    
    lines.append(f"Procesador: {get_cpu_name()}")
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
    # Esta línea es crucial para evitar bucles infinitos en Windows con PyInstaller/multiprocessing
    multiprocessing.freeze_support()

    print("Iniciando monitorización... Por favor espere, obteniendo datos del sistema...")
    
    while True:
        # Generamos primero (puede tardar la primera vez)
        full_report = generate_snapshot()
        
        clear_screen()
        print(full_report)
        
        print("\nInformación guardada en 'reporte_sistema.txt'")
        print("Presiona Ctrl+C para salir.")
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
    except Exception as e:
        print(f"\nERROR CRÍTICO: {e}")
        traceback.print_exc()
        input("Presiona ENTER para cerrar...")
