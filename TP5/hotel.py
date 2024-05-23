import numpy as np
import matplotlib.pyplot as plt


num_experimentos = 1
num_corridas = 1

tiempos_experimentos = []
criticidad_accesos_experimentos = []


"""
Referencia  Tarea                                   Demora
A           Romper huevos                           U(2, 4)
B           Revolver huevos                         U(3, 6)
C           Cocinar huevos                          U(2, 5)
D           Cortar panes                            U(3, 6)
E           Preparar tostadas                       U(2, 5)
F           Preparar bebidas calientes (té, café)   U(4, 8)
G           Preparar bebidas frías (jugos, yogur)   U(3, 7)

El orden de las tareas va a estar dado por 3 accesos:
Superior:
INICIO -> A -> B -> C -> FIN
Medio:
INICIO -> D -> E -> FIN
Inferior:
INICIO -> F -> G -> FIN

Cada acceso se realiza en paralelo y el tiempo de finalizacion va a estar 
dado por la ultima tarea en finalizar. En este caso se pretende simular
los tiempos en los que las tareas van a ejcutarse 
"""

tareas = {
    'A' : {'nombre' : "Romper huevos", 'demora_min': 2, 'demora_max': 4},
    'B' : {'nombre' : "Revolver huevos", 'demora_min': 3, 'demora_max': 6},
    'C' : {'nombre' : "Cocinar huevos", 'demora_min': 2, 'demora_max': 5},
    'D' : {'nombre' : "Cortar panes", 'demora_min': 3, 'demora_max': 6},
    'E' : {'nombre' : "Preparar tostadas", 'demora_min': 2, 'demora_max': 5},
    'F' : {'nombre' : "Preparar bebidas calientes", 'demora_min': 4, 'demora_max': 8},
    'G' : {'nombre' : "Preparar bebidas frías", 'demora_min': 3, 'demora_max': 7}
}

def generar_tiempo(min, max, size):
    return np.random.uniform(min, max, size)

def realizar_tarea(ref):
    tarea = tarea[ref]
    tiempo = generar_tiempo(tarea['demora_min'][0], tarea['demora_max'][1], 1)
    return tiempo

def simular_tareas():

    #Tiempos de tareas acceso superior
    tarea_a = realizar_tarea('A')
    tarea_b = realizar_tarea('B')
    tarea_c = realizar_tarea('C')
    acceso_superior = max(tarea_a + tarea_b + tarea_c)
    
    #Tiempos de tareas acceso medio
    tarea_d = realizar_tarea('D')
    tarea_e = realizar_tarea('E')
    acceso_medio = max(tarea_d + tarea_e)
    
    #Tiempos de tareas acceso inferior
    tarea_f = realizar_tarea('F')
    tarea_g = realizar_tarea('G')
    acceso_inferior = max(tarea_f + tarea_g)

    tiempo_total = max(acceso_superior, acceso_medio, acceso_inferior) #El tiempo maximo de los 3 accesos
    print(tiempo_total)
    return tiempo_total, acceso_superior, acceso_medio, acceso_inferior

"""
Simular el experimento segun la cantidad de corridas de la simulacion de tareas.

"""
def simular_experimento(num_corridas):
    tiempos_experimento = []
    criticidad_accesos = {'superior': 0, 'medio': 0, 'inferior': 0}

    for _ in range(num_corridas):
        tiempo_total, acceso_superior, acceso_medio, acceso_inferior = simular_tareas()
        tiempos_experimento.append(tiempo_total)

        if tiempo_total == acceso_superior:
            criticidad_accesos['superior'] += 1
        if tiempo_total == acceso_medio:
            criticidad_accesos['medio'] += 1
        if tiempo_total == acceso_inferior:
            criticidad_accesos['inferior'] += 1

    return tiempos_experimento, criticidad_accesos

def calcular_intervalo_confianza(media_muestral, mult_desvio, desvio_estandar, z, n):
    error_estandar = z * ( (mult_desvio * desvio_estandar) / np.sqrt(n))
    extremo_inferior = media_muestral - error_estandar
    extremo_superior = media_muestral + error_estandar
    
    return extremo_inferior, extremo_superior


for _ in range(num_experimentos):
    tiempos_experimento, criticidad_accesos = simular_experimento(num_corridas)
    tiempos_experimentos.append(tiempos_experimento)
    criticidad_accesos_experimentos.append(criticidad_accesos)

# 1. Calcular tiempo promedio de finalización del proyecto e IC
tiempos_experimentos = np.array(tiempos_experimentos)
tiempo_promedio_experimentos = np.mean(tiempos_experimentos, axis=1)
tiempo_promedio = np.mean(tiempo_promedio_experimentos)
ic_99 = np.percentile(tiempo_promedio_experimentos, [0.5, 99.5])

print("Tiempo promedio de finalización del proyecto:", tiempo_promedio)
print("Intervalo de confianza al 99%:", ic_99)

# 2. Calcular porcentaje de criticidad de los accesos
total_corridas = num_experimentos * num_corridas
criticidad_accesos_totales = {'superior': 0, 'medio': 0, 'inferior': 0}

for criticidad_accesos in criticidad_accesos_experimentos:
    for key, value in criticidad_accesos.items():
        criticidad_accesos_totales[key] += value

for key, value in criticidad_accesos_totales.items():
    print("Porcentaje de criticidad para acceso", key, ":", value / total_corridas * 100)

# 3. Graficar histograma de distribución del tiempo de realización del proyecto
plt.figure(figsize=(10, 6))
plt.hist(tiempos_experimentos.flatten(), bins=30, alpha=0.7, color='blue', edgecolor='black')
plt.title('Distribución del tiempo de realización del proyecto')
plt.xlabel('Tiempo de finalización del proyecto')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()

# Graficar histograma de promedios de los 30 experimentos
plt.figure(figsize=(10, 6))
plt.hist(tiempo_promedio_experimentos, bins=15, alpha=0.7, color='green', edgecolor='black')
plt.title('Distribución de promedios de los 30 experimentos')
plt.xlabel('Promedio de tiempo de finalización del proyecto')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()