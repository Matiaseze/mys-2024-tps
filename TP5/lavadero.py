import numpy as np
import matplotlib.pyplot as plt

tiempos_experimentos = []
tiempo_proyecto = []
criticidad_accesos_experimentos = []


"""
Referencia  Tarea                                   Demora
A           Retirar alfombras                       U(2, 4)
B           Aplicar detergente                      U(3, 6)
C           Enjuagar alfombras                      U(2, 5)
D           Mojar vehículo                          U(3, 6)
E           Aplicar detergente                      U(2, 5)
F           Enjuagar vehículo                       U(4, 8)
G           Aspirar interiores                      U(3, 7)

El orden de las tareas va a estar dado por:
Superior:
INICIO -> A -> B -> C -> FIN
Inferior:
INICIO -> D -> E -> F -> FIN
InferiorConG:
-> D -> E -> F -> G -> FIN

"""

tareas = {
    'A' : {'nombre' : "Retirar alfombras", 'demora_min': 1, 'demora_max': 5},
    'B' : {'nombre' : "Aplicar detergente", 'demora_min': 1, 'demora_max': 3},
    'C' : {'nombre' : "Enjuagar alfombras", 'demora_min': 1, 'demora_max': 3},
    'D' : {'nombre' : "Mojar vehículo", 'demora_min': 1, 'demora_max': 6},
    'E' : {'nombre' : "Aplicar detergente", 'demora_min': 6, 'demora_max': 12},
    'F' : {'nombre' : "Enjuagar vehículo", 'demora_min': 5, 'demora_max': 10},
    'G' : {'nombre' : "Aspirar interiores", 'demora_min': 10, 'demora_max': 15}
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
    tarea_f = realizar_tarea('F')
    acceso_inferior = tarea_d + tarea_e + tarea_f
    
    #Tiempos de tareas acceso inferior
    tarea_g = realizar_tarea('G')
    acceso_inferior_con_g = tarea_d + tarea_e + tarea_f + tarea_g 

    tiempo_total = max(acceso_superior, acceso_inferior, acceso_inferior_con_g) #El tiempo maximo de los 3 accesos
    return tiempo_total, acceso_superior, acceso_inferior, acceso_inferior_con_g
"""
Simular el experimento segun la cantidad de corridas de la simulacion de tareas.

"""
def simular_experimento(num_corridas):
    tiempos_experimento = []
    criticidad_accesos = {'superior': 0, 'inferior': 0, 'infcong': 0}

    for i in range(num_corridas):
        tiempo_total, acceso_superior, acceso_inferior, acceso_inferior_con_g = simular_tareas()
        tiempos_experimento.append(tiempo_total)

        if tiempo_total == acceso_superior:
            criticidad_accesos['superior'] += 1
        if tiempo_total == acceso_inferior:
            criticidad_accesos['inferior'] += 1
        if tiempo_total == acceso_inferior_con_g:
            criticidad_accesos['infcong'] += 1

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
    
    criticidad_accesos_totales = {'superior': 0, 'inferior': 0, 'infcong': 0}

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