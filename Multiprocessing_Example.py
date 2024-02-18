from multiprocessing import Process
import time

def tarea(nombre, segundos):
    print(f"{nombre}: Iniciando tarea")
    time.sleep(segundos)
    print(f"{nombre}: Tarea completada después de {segundos} segundos")

if __name__ == "__main__":
    # Definimos las tareas con diferentes tiempos de ejecución
    tareas = [
        Process(target=tarea, args=("Tarea 1", 3)),
        Process(target=tarea, args=("Tarea 2", 2)),
        Process(target=tarea, args=("Tarea 3", 4))
    ]

    # Iniciamos cada proceso
    for proceso in tareas:
        proceso.start()

    # Esperamos a que cada proceso termine
    for proceso in tareas:
        proceso.join()

    print("Todas las tareas han sido completadas")