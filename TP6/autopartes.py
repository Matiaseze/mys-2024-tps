import numpy as np

demanda_diaria = np.random.normal(loc=150, scale=25)
turnos_por_dia = 1
produccion_diaria = 130 * turnos_por_dia
anios = 30
dias_habiles = 250
stock_inicial = 90
mantenimiento_stock = 70 * produccion_diaria

for anio in anios:
    for dia in dias_habiles:





