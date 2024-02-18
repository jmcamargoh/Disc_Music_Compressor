import threading
import time

def tarea_1():
    for _ in range(5):
        print("Tarea 1 ejecutándose")
        time.sleep(1)

def tarea_2():
    for _ in range(5):
        print("Tarea 2 ejecutándose")
        time.sleep(1)

# Creamos los objetos Thread
hilo_1 = threading.Thread(target=tarea_1)
hilo_2 = threading.Thread(target=tarea_2)

# Iniciamos los hilos
tiempo_inicio = time.perf_counter()
hilo_1.start()
hilo_2.start()

# Esperamos a que ambos hilos terminen
hilo_1.join()
hilo_2.join()
tiempo_final = time.perf_counter()

tiempo_ejecucion = tiempo_final-tiempo_inicio

print("Ambos hilos han terminado")
print(f"Tiempo de ejecucion = {tiempo_ejecucion} segundos")
# Si no se usaran hilos, tendria que acabar una tarea y luego la otra