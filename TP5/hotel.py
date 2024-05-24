import numpy as np
import matplotlib.pyplot as plt

tiempos_experimentos = []
tiempo_proyecto = []
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

def generar_tiempo(min, max):
    return np.random.uniform(min, max)

def realizar_tarea(ref):
    tarea = tareas[ref]
    tiempo = generar_tiempo(tarea['demora_min'], tarea['demora_max'])
    return tiempo

def simular_tareas():

    #Tiempos de tareas acceso superior
    tarea_a = realizar_tarea('A')
    tarea_b = realizar_tarea('B')
    tarea_c = realizar_tarea('C')
    acceso_superior = tarea_a + tarea_b + tarea_c
    
    #Tiempos de tareas acceso medio
    tarea_d = realizar_tarea('D')
    tarea_e = realizar_tarea('E')
    acceso_medio = tarea_d + tarea_e
    
    #Tiempos de tareas acceso inferior
    tarea_f = realizar_tarea('F')
    tarea_g = realizar_tarea('G')
    acceso_inferior = tarea_f + tarea_g

    tiempo_total = max(acceso_superior, acceso_medio, acceso_inferior) #El tiempo maximo de los 3 accesos
    return tiempo_total, acceso_superior, acceso_medio, acceso_inferior

"""
Simular el experimento segun la cantidad de corridas de la simulacion de tareas.

"""
def simular_experimento(num_corridas):
    tiempos_experimento = []
    criticidad_accesos = {'superior': 0, 'medio': 0, 'inferior': 0}

    for i in range(num_corridas):
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

def simular_proyecto(num_experimentos, num_corridas):

    for _ in range(num_experimentos):

        tiempos_experimento, criticidad_accesos = simular_experimento(num_corridas)
        tiempos_experimentos.append(tiempos_experimento)
        criticidad_accesos_experimentos.append(criticidad_accesos)
        tiempo_proyecto.append(np.mean(tiempos_experimentos))
 
    return tiempos_experimentos, tiempo_proyecto, criticidad_accesos_experimentos


# 1. Calcular tiempo promedio de finalización del proyecto
def calcular_tiempo_promedio(tiempos):
    tiempo_promedio = np.mean(tiempos)
    
    print("Tiempo promedio de finalización del proyecto:", tiempo_promedio)
    return tiempo_promedio

# 1. Calcular el intervalo de confianza de la finalizacion del proyecto
def calcular_ic99_exp(tiempos_experimentos):
    tiempo_promedio = calcular_tiempo_promedio(tiempos_experimentos)
    desvio_estandar = np.std(tiempos_experimentos)

    ic_99_inf, ic_99_sup = calcular_intervalo_confianza(tiempo_promedio, 1, desvio_estandar, 2.57, len(tiempos_experimentos))
    return ic_99_inf, ic_99_sup

# 2. Calcular porcentaje de criticidad de los accesos
def calcular_criticidad_accesos(total_corridas, criticidad_accesos_experimentos):
    
    criticidad_accesos_totales = {'superior': 0, 'medio': 0, 'inferior': 0}

    for criticidad_accesos in criticidad_accesos_experimentos:
        for key, value in criticidad_accesos.items():
            criticidad_accesos_totales[key] += value

    for key, value in criticidad_accesos_totales.items():
        print("Porcentaje de criticidad para acceso", key, ":", value / total_corridas * 100)

# 3. Histograma de distribución del tiempo de realización del proyecto
def graficar_histogramas(tiempo_proyecto, tiempos_experimentos):
    fig, axs = plt.subplots(1, 2, figsize=(20, 6))

    # Primer histograma
    axs[0].hist(tiempo_proyecto, bins=30, alpha=0.7, color='blue', edgecolor='black')
    axs[0].set_title('Distribucion del tiempo de realizacion del proyecto')
    axs[0].set_xlabel('Tiempo de finalización del proyecto')
    axs[0].set_ylabel('Frecuencia')
    axs[0].grid(True)

    # Segundo histograma
    axs[1].hist(np.array(tiempos_experimentos).flatten(), bins=30, alpha=0.7, color='red', edgecolor='black')
    axs[1].set_title('Distribucion de promedios de los 30 experimentos')
    axs[1].set_xlabel('Promedio de tiempo de finalizacion del proyecto')
    axs[1].set_ylabel('Frecuencia')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()