import numpy as np
import matplotlib.pyplot as plt


# Inicializar parametros de la simulacion
media_demanda = 150
desviacion_estandar_demanda = 25
capacidad_produccion = 130
anios_simulacion = 30
dias_habiles = 250
inv_inicial = 90
umbrales_inventario = [50,60,70,80]
costo_mantenimiento = 70


def calcular_intervalo_confianza(media_muestral, mult_desvio, desvio_estandar, z, n):
    error_estandar = z * ( (mult_desvio * desvio_estandar) / np.sqrt(n))
    extremo_inferior = media_muestral - error_estandar
    extremo_superior = media_muestral + error_estandar
    
    return extremo_inferior, extremo_superior

def mostrar_resultados_graficados(resultados):
    for resultado in resultados:
        print(f"Umbral de inventario: {resultado['umbral']}")
        print(f"Promedio de turnos adicionales: {resultado['promedio_turnos_adicionales']:.2f}")
        print(f"IC 95% turnos adicionales: ({resultado['ic_turnos'][0]:.2f}, {resultado['ic_turnos'][1]:.2f})")
        print(f"Promedio de costos anuales de mantenimiento: {resultado['promedio_costos_mantenimiento']:.2f}")
        print(f"IC 95% costos anuales: ({resultado['ic_costos'][0]:.2f}, {resultado['ic_costos'][1]:.2f})")

        plt.hist(resultado["histogram_data"], bins=30, alpha=0.75, edgecolor='black')
        plt.title(f"Histograma de costos anuales (Umbral: {resultado['umbral']})")
        plt.xlabel("Costo anual de mantenimiento")
        plt.ylabel("Frecuencia")
        plt.show()


def simulacion():

    resultados = []
    total_turnos_adicionales = []
    total_costo_mantenimiento = []
    inventario = inv_inicial

    for umbral in umbrales_inventario: 
        for anio in range(anios_simulacion):
            turnos_adic_anules = 0
            costo_mant_anual = 0

            for dia in range(dias_habiles):
                inventario += 130
                demanda = np.random.normal(media_demanda, desviacion_estandar_demanda)
                inventario -= demanda
                if inventario <= umbral:
                    inventario += capacidad_produccion
                    turnos_adic_anules += 1

                if inventario > 0: 
                    costo_mant_anual += costo_mantenimiento *inventario
                
            
            total_turnos_adicionales.append(turnos_adic_anules)
            total_costo_mantenimiento.append(costo_mant_anual)

        z = 1.96
        promedio_turnos_adicionales = np.mean(total_turnos_adicionales)
        ic_turnos_inf, ic_turnos_sup = calcular_intervalo_confianza(promedio_turnos_adicionales, 1, np.std(total_turnos_adicionales), z, len(total_turnos_adicionales))
        promedio_costos_mantenimiento = np.mean(total_costo_mantenimiento)
        ic_costos_inf, ic_costos_sup = calcular_intervalo_confianza(promedio_costos_mantenimiento, 1, np.std(total_costo_mantenimiento), z, len(total_costo_mantenimiento))

        resultados.append({
            "umbral": umbral,
            "promedio_turnos_adicionales": promedio_turnos_adicionales,
            "ic_turnos": (ic_turnos_inf, ic_turnos_sup),
            "promedio_costos_mantenimiento": promedio_costos_mantenimiento,
            "ic_costos": (ic_costos_inf, ic_costos_sup),
            "histogram_data": total_costo_mantenimiento
        })

    mostrar_resultados_graficados(resultados)





