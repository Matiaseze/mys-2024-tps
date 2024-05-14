import numpy as np
import matplotlib.pyplot as plt


def generar_tiempo(min, max, size):
    return np.random.uniform(min, max, size)

def realizar_tarea(ref):
    tarea = tareas[ref]
    tiempo = generar_tiempo(tarea['demora_min'], tarea['demora_max'], 1)
    return tiempo

def simular_tareas():

    # A->B->C->
    tarea_a = realizar_tarea('A')
    tarea_b = realizar_tarea('B')
    tarea_c = realizar_tarea('C')
    tareas_iniciales = max(tarea_a + tarea_b + tarea_c)
    
    #Tiempos de tareas acceso superior
    tarea_g = realizar_tarea('G')
    tarea_h = realizar_tarea('H')
    acceso_superior = max(tarea_g + tarea_h)

    #Tiempos de tareas acceso medio
    tarea_d = realizar_tarea('D')
    tarea_e = realizar_tarea('E')
    acceso_medio = max(tarea_d + tarea_e)
    
    #Tiempos de tareas acceso inferior
    tarea_f = realizar_tarea('F')
    tarea_i = realizar_tarea('I')
    acceso_inferior = max(tarea_f + tarea_i)

    tiempo_total = max(tareas_iniciales, acceso_superior, acceso_medio, acceso_inferior) #El tiempo maximo de los 3 accesos
    return tiempo_total, tareas_iniciales, acceso_superior, acceso_medio, acceso_inferior

"""
Simular el experimento segun la cantidad de corridas de la simulacion de tareas.

"""
def simular_experimento(num_corridas):
    tiempos_corridas = []
    criticidad_accesos = {'inicial': 0, 'superior': 0, 'medio': 0, 'inferior': 0}

    for i in range(num_corridas):
        tiempo_total, tareas_iniciales, acceso_superior, acceso_medio, acceso_inferior = simular_tareas()
        tiempos_corridas.append(tiempo_total)
        if tiempo_total == tareas_iniciales:
            criticidad_accesos['inicial'] += 1
        if tiempo_total == acceso_superior:
            criticidad_accesos['superior'] += 1
        if tiempo_total == acceso_medio:
            criticidad_accesos['medio'] += 1
        if tiempo_total == acceso_inferior:
            criticidad_accesos['inferior'] += 1

    return tiempos_corridas, criticidad_accesos

def calcular_intervalo_confianza(media_muestral, mult_desvio, desvio_estandar, z, n):
    error_estandar = z * ( (mult_desvio * desvio_estandar) / np.sqrt(n))
    extremo_inferior = media_muestral - error_estandar
    extremo_superior = media_muestral + error_estandar
    
    return extremo_inferior, extremo_superior


def simular_proyecto(num_experimentos, num_corridas):

    for i in range(num_experimentos):

        tiempos_corridas, criticidad_accesos = simular_experimento(num_corridas)
        
        tiempos_experimentos.append(tiempos_corridas)        
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
    desvio_estandar = np.std(tiempo_promedio)
    ic_99_inf, ic_99_sup = calcular_intervalo_confianza(tiempo_promedio, 1, desvio_estandar, 2.57, tiempos_experimentos)
    return ic_99_inf, ic_99_sup

# 2. Calcular porcentaje de criticidad de los accesos
def calcular_criticidad_accesos(total_corridas, criticidad_accesos_experimentos):
    
    criticidad_accesos_totales = {'inicial': 0, 'superior': 0, 'medio': 0, 'inferior': 0}

    for criticidad_accesos in criticidad_accesos_experimentos:
        for key, value in criticidad_accesos.items():
            criticidad_accesos_totales[key] += value

    for key, value in criticidad_accesos_totales.items():
        print("Porcentaje de criticidad para acceso", key, ":", value / total_corridas * 100)

# 3. Histograma de distribución del tiempo de realización del proyecto
def graficar_histogramas(tiempo_proyecto, tiempos_experimentos):
    plt.figure(figsize=(10, 6))
    plt.hist(tiempo_proyecto, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribución del tiempo de realización del proyecto')
    plt.xlabel('Tiempo de finalización del proyecto')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

    # Histograma de promedios de los 3000 corridas
    plt.figure(figsize=(10, 6))
    plt.hist(tiempos_experimentos, bins=30, alpha=0.7, color='red', edgecolor='black')
    plt.title('Distribución de promedios de los 30 experimentos')
    plt.xlabel('Promedio de tiempo de finalización del proyecto')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()



if __name__ == '__main__':

    num_experimentos = 2
    num_corridas = 100

    tiempos_experimentos = []
    tiempo_proyecto = []
    criticidad_accesos_experimentos = []


    """
    Referencia  Tarea                                   Demora
    A           Preparar terreno (rellenar/nivelar)     U(2, 4)
    B           Construir bases                         U(3, 5)
    C           Preparar cañería de cloacas             U(1, 2)
    D           Levantar paredes                        U(4, 8)
    E           Construir techo (madera + chapas)       U(3, 6)
    F           Realizar la instalación eléctrica       U(2, 5)
    G           Realizar la instalación de gas          U(2, 4)
    H           Colocar aberturas                       U(1, 3)
    I           Colocar pisos                           U(2, 4) 
    J           Pintar la casa (interior/exterior)      U(2, 3)

    """

    tareas = {
        'A' : {'nombre' : "Preparar terreno", 'demora_min': 2, 'demora_max': 4},
        'B' : {'nombre' : "Construir bases", 'demora_min': 3, 'demora_max': 5},
        'C' : {'nombre' : "Preparar cañería de cloacas", 'demora_min': 1, 'demora_max': 2},
        'D' : {'nombre' : "Levantar paredes", 'demora_min': 4, 'demora_max': 8},
        'E' : {'nombre' : "Construir techo", 'demora_min': 3, 'demora_max': 6},
        'F' : {'nombre' : "Realizar la instalación eléctrica", 'demora_min': 2, 'demora_max': 5},
        'G' : {'nombre' : "Realizar la instalación de gas", 'demora_min': 2, 'demora_max': 4},
        'H' : {'nombre' : "Colocar aberturas", 'demora_min': 1, 'demora_max': 3},
        'I' : {'nombre' : "Colocar pisos", 'demora_min': 2, 'demora_max': 4},
        'J' : {'nombre' : "Pintar la casa", 'demora_min': 2, 'demora_max': 3}
    }

    # 1.
    tiempos_experimentos, tiempo_proyecto, criticidad_accesos_experimentos = simular_proyecto(num_experimentos, num_corridas)
    ic_99_inf, ic_99_sup = calcular_ic99_exp(tiempos_experimentos)
    # 2.
    total_corridas = num_experimentos * num_corridas
    calcular_criticidad_accesos(total_corridas, criticidad_accesos_experimentos)
    # 3.
    print(tiempos_experimentos)
    graficar_histogramas(tiempo_proyecto, tiempos_experimentos)

