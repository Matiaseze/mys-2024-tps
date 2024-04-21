import numpy as np
import matplotlib.pyplot as plt

"""

1) Investigue y documente al menos 2 lenguajes de programación que ofrezcan la posibilidad de generar números aleatorios que sigan una distribución probabilística ya sea de modo nativo o bien a través del uso de librerías externas. 
Genere un conjunto de 100 datos numéricos para una variable imaginaria y con ayuda de los lenguajes:
a. Calcule la media.
b. Calcule el desvío estándar.
c. Calcule la varianza. 
¿Cómo se crean gráficos para interpretar los valores generados? Describa qué método/función se ha invocado junto con sus parámetros.


"""

muestra = np.random.normal(loc=0, scale=0.1, size=100) # Generar datos con distribuicion normal

media = np.mean(muestra) # Calcular la media

desvio = np.std(muestra) # Calcular el desvio estandar

varianza = np.var(muestra) # Calcular la varianza

print("Valor de la media: ",media)
print("Valor del desvio estandar: ", desvio)
print("Valor de la varianza: ", varianza)

plt.hist(muestra, bins=10, edgecolor='black')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.title('Histograma de datos generados con python')
plt.show()

"""

2) Teniendo en cuenta el material teórico y los lenguajes investigados en el punto 1, elija uno de ellos y genere 1000 valores de números aleatorios:
a. Uniforme, con parámetros: Min: 0, Max: 1. 
b. Normal, con parámetros: Media: 0, Desvío: 1.
c. Poisson, con parámetro: λ = 6. 
d. Exponencial, con parámetro: β = 3/4. 
Luego realice un histograma para observar gráficamente cómo es la distribución en cada ítem.

"""
distr_uniforme = np.random.uniform(0, 1, 1000) # Uniforme, con parámetros: Min: 0, Max: 1.

distr_normal = np.random.normal(0, 1, 1000) # Normal, con parámetros: Media: 0, Desvío: 1.

distr_poisson = np.random.poisson(6, 1000) # Poisson, con parámetro: λ = 6. 

distr_exponencial = np.random.exponential(3/4, 1000) # Exponencial, con parámetro: β = 3/4.

plt.figure(figsize=(12, 10)) # Grafico en una sola ventana

plt.subplot(2, 2, 1)
plt.hist(distr_uniforme, bins=50, color='blue', alpha=0.4, edgecolor='black')
plt.title('Histograma de muestra generada con distribucion Uniforme')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')

plt.subplot(2, 2, 2)
plt.hist(distr_normal, bins=50, color='red', alpha=0.7, edgecolor='black')
plt.title('Histograma de muestra generada con distribucion Normal (0,1)')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')

plt.subplot(2, 2, 3)
plt.hist(distr_poisson, bins=50, color='green', alpha=0.7,  edgecolor='black')
plt.title('Histograma de muestra generada con distribucion de Poisson')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')

plt.subplot(2, 2, 4)
plt.hist(distr_exponencial, bins=30, color='gold', edgecolor='black')
plt.title('Histograma de muestra generada con distribucion Exponencial')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')

plt.tight_layout()
plt.show()

"""

3) A partir de la muestra obtenida de 1000 valores en el punto 2.a, realice:
a. Una función de transformación para que la variable aleatoria tenga una distribución de probabilidad Exponencial con parámetro β = 12.
b. Un gráfico adecuado para la variable aleatoria del inciso anterior.
c. Genere otros 100 valores aleatorios siguiendo una distribución Exponencial con parámetro β = 3.
d. Genere 1000 valores aleatorios con las mismas características que en el inciso c.
e. Grafique los incisos c y d.
f. Compare resultados para 100, 1000 y 10000 valores. ¿Qué diferencia visual encuentra entre los gráficos?

"""

"""
a. 
Formula de la transformacion: X = - (1/λ) ln(U) 
donde:
U es la muestra con distribucion uniforme (0,1) y 1/λ es beta. 

"""
def transformacion_exponencial(muestra, beta):
    return -beta * np.log(1 - muestra)

exponencial_con_beta12 = transformacion_exponencial(distr_uniforme, 12)

"""
b. Graficar

"""
plt.hist(exponencial_con_beta12, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma con valores con distribución exponencial β = 12')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.show()

"""
c. 100 numeros aleatorios con distribucion exponencial

"""
exponencial_100_beta3 = np.random.exponential(3, 100)

"""
d. 1000 numeros aleatorios con distribucion exponencial

"""

exponencial_1000_beta3 = np.random.exponential(3, 1000)

"""
e. Graficar c y d

"""
plt.subplot(2,2,1)
plt.hist(exponencial_100_beta3, bins=40, color='salmon', edgecolor='black', alpha=0.7, label='n=100')
plt.title('100 numeros aleatorios')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()

plt.subplot(2,2,2)
plt.hist(exponencial_1000_beta3, bins=40, color='green', edgecolor='black', alpha=0.7, label='n=1000')
plt.title('1000 numeros aleatorios')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()

"""
f. 10000 numeros aleatorios con distribucion exponencial, graficar y comparar con 100 y 1000

"""
exponencial_10000_beta3 = np.random.exponential(3, 10000)

plt.figure(figsize=(12, 10))

plt.subplot(2,3,1)
plt.hist(exponencial_100_beta3, bins=40, color='salmon', edgecolor='black', alpha=0.7, label='n=100')
plt.title('100 numeros aleatorios')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()

plt.subplot(2,3,2)
plt.hist(exponencial_1000_beta3, bins=40, color='green', edgecolor='black', alpha=0.7, label='n=1000')
plt.title('1000 numeros aleatorios')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()

plt.subplot(2,3,3)
plt.hist(exponencial_10000_beta3, bins=40, color='cyan', edgecolor='black', alpha=0.7, label='n=10000')
plt.title('10000 numeros aleatorios')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()

plt.suptitle("Comparacion de histogramas con distribucion exponencial")
plt.tight_layout()
plt.show()


"""

4) De acuerdo a los resultados obtenidos en el ejercicio anterior (3.f). Especifique:
a. ¿Cuál fue la media muestral de los datos generados?
b. ¿Cuál fue el desvío estándar de los datos generados?
c. ¿Cuál fue la varianza muestral de los datos generados?

"""
media_100 = np.mean(exponencial_100_beta3) # Media 100 numeros aleatorios

media_1000 = np.mean(exponencial_1000_beta3) # Media 1000 numeros aleatorios

media_10000 = np.mean(exponencial_10000_beta3) # Media 10000 numeros aleatorios


desvio_100 = np.std(exponencial_100_beta3) # desvio 100 numeros aleatorios

desvio_1000 = np.std(exponencial_1000_beta3) # desvio 1000 numeros aleatorios

desvio_10000 = np.std(exponencial_10000_beta3) # desvio 10000 numeros aleatorios


varianza_100 = np.var(exponencial_100_beta3) # varianza 100 numeros aleatorios

varianza_1000 = np.var(exponencial_1000_beta3) # varianza 1000 numeros aleatorios

varianza_10000 = np.var(exponencial_10000_beta3) # varianza 10000 numeros aleatorios

print("La media es:","\n"," Con 100:", media_100,"\n"," Con 1000:", media_1000,"\n"," Con 10000:", media_10000)
print("El desvio estandar es:","\n"," Con 100:", desvio_100,"\n"," Con 1000:", desvio_1000,"\n"," Con 10000:", desvio_10000)
print("La varianza es:","\n"," Con 100:", varianza_100,"\n"," Con 1000:", varianza_1000,"\n"," Con 10000:", varianza_10000)


"""

5) Codifique una función o método que permita calcular para la muestra un intervalo de confianza para estimar el valor de la media poblacional. Deberá obtener el coeficiente z para un 99% de confiabilidad y retornar el resultado contemplando  2 desvíos estándar en la fórmula. 
Para el cálculo del coeficiente z, utilice la tabla disponible en la bibliografía.
Ejemplo: para un 95% de confiabilidad, z=1.96.
El intervalo de confianza se conforma de la siguiente manera:

Extremo inferior = X - 1.96 . σ/√n

Extremo inferior = X + 1.96 . σ/√n

Donde X, representa la media muestral, σ es el desvío estándar de dicha muestra y n, es el número de elementos de la muestra. Se dice entonces que:

X - 1.96 σ/√n  <= μ <=  X + 1.96 . σ/√n

Donde μ es la media poblacional

"""

n_de_100 = len(exponencial_100_beta3)
n_de_1000 = len(exponencial_1000_beta3)
n_de_10000 = len(exponencial_10000_beta3)
# Nota: utilice el tamaño de las muestras generadas con distribucion exponencial del punto anterior.

z = 2.58 # Valor obtenido de la tabla Z para un nivel de confianza del 99%
mult_desvio = 2
def calcular_intervalo_confianza(media_muestral, mult_desvio, desvio_estandar, z, n):
    error_estandar = z * ( (mult_desvio * desvio_estandar) / np.sqrt(n))
    extremo_inferior = media_muestral - error_estandar
    extremo_superior = media_muestral + error_estandar
    
    return extremo_inferior, extremo_superior

intervalo_100 = calcular_intervalo_confianza(media_100, mult_desvio, desvio_100, z, n_de_100)
intervalo_1000 = calcular_intervalo_confianza(media_1000, mult_desvio, desvio_1000, z, n_de_1000)
intervalo_10000 = calcular_intervalo_confianza(media_10000, mult_desvio, desvio_10000, z, n_de_10000)

print("Intervalo de confianza estimado para :", intervalo_100)
print("Intervalo de confianza estimado para :", intervalo_1000)
print("Intervalo de confianza estimado para :", intervalo_10000)
