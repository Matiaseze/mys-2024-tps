import numpy as np
import matplotlib.pyplot as plt

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

def generar_tiempo(min, max):
    return np.random.uniform(min, max)

def realizar_tarea(ref):
    tarea = tareas[ref]
    tiempo = generar_tiempo(tarea['demora_min'], tarea['demora_max'])
    return tiempo

def simular_tareas():

    # A->B->C->
    tarea_a = realizar_tarea('A')
    tarea_b = realizar_tarea('B')
    tarea_c = realizar_tarea('C')
    tareas_iniciales = (tarea_a + tarea_b + tarea_c)
    #Tiempos de tareas acceso superior
    # D->G->H->
    tarea_d = realizar_tarea('D')
    tarea_g = realizar_tarea('G')
    tarea_h = realizar_tarea('H')
    acceso_superior = tarea_d + tarea_g + tarea_h

    #Tiempos de tareas acceso medio
    # D->E->
    tarea_e = realizar_tarea('E')
    acceso_medio = tarea_d + tarea_e
    
    #Tiempos de tareas acceso inferior
    # D->F->I
    tarea_f = realizar_tarea('F')
    tarea_i = realizar_tarea('I')
    acceso_inferior = tarea_d + tarea_f + tarea_i

    tarea_j = realizar_tarea('J')   
    tarea_final = tarea_j

    tiempo_total = tareas_iniciales + max(acceso_superior, acceso_medio, acceso_inferior) + tarea_j
    return tiempo_total, tareas_iniciales, acceso_superior, acceso_medio, acceso_inferior, tarea_final

"""
Simular el experimento segun la cantidad de corridas de la simulacion de tareas.

"""
def simular_experimento(num_corridas):
    tiempos_corridas = []
    criticidad_accesos = {'inicial' : 0, 'superior': 0, 'medio': 0, 'inferior': 0, 'final' : 0} 

    for i in range(num_corridas):
        tiempo_total, tareas_iniciales, acceso_superior, acceso_medio, acceso_inferior, tarea_final = simular_tareas()

        tiempos_corridas.append(tiempo_total)
        
        criticidad_accesos['inicial'] += tareas_iniciales
        criticidad_accesos['superior'] += acceso_superior
        criticidad_accesos['medio'] += acceso_medio
        criticidad_accesos['inferior'] += acceso_inferior
        criticidad_accesos['final'] += tarea_final
           
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
    desvio_estandar = np.std(tiempos_experimentos)

    ic_99_inf, ic_99_sup = calcular_intervalo_confianza(tiempo_promedio, 1, desvio_estandar, 2.57, len(tiempos_experimentos))
    return ic_99_inf, ic_99_sup

# 2. Calcular porcentaje de criticidad de los accesos
def calcular_criticidad_accesos(total_corridas, criticidad_accesos_experimentos):
    
    criticidad_accesos_totales = {'inicial': 0, 'superior': 0, 'medio': 0, 'inferior': 0, 'final' : 0}

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