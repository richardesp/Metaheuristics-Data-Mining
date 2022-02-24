import random
import math

from utils import get_laplace_probability
from TSPGenerator import generador
from cooldown_functions import *

def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerVecino(solucion, datos):
    ##Obtención de los vecinos
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtengo un vecino aleatorio
    vecino=vecinos[random.randint(0, len(vecinos) - 1)]
    longitud = evaluarSolucion(datos, vecino)

    return vecino, longitud

def simAnnealing(datos,t0):
    t=t0
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)
    print("Longitud de la ruta: ", longitud)
    print("Temperatura: ", t)

    it=0
    while t > 0.05:
        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]

        # Si la probabilidad dada la diferencia de leyes térmicas es inferior al valor entre 0 y 1 (prob)
        # entonces cogeré ese vecino pese a que sea peor o mejor, da igual, va en función de la diferencia que haya
        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]

        it+=1

        # Función para descender la temperatura

        fichero = open("temperaturas.txt", "a")
        fichero.write(f"{t:.4f}\n")
        t = quadratic_multiplicative_cooling(t, it)

        print("Longitud de la ruta: ", longitud)
        print("Temperatura: ", t)

        fichero.close()

    return solucion, longitud

def main():
    datos = [
        [0, 400, 500, 300],
        [400, 0, 300, 500],
        [500, 300, 0, 400],
        [300, 500, 400, 0]
    ]

    EXECUTE_EXPERIMENT_1 = True
    EXECUTE_EXPERIMENT_2 = False
    EXECUTE_EXPERIMENT_3 = False

    if EXECUTE_EXPERIMENT_1:

        t0=10 # Temperatura inicial para comenzar el descenso del valor
        n_cities = int()
        datos = generador(n_cities)

        exp_len_min = 4
        exp_len_max = 20
        frequencies_array = []

        # Experimento 1 para generar la gráfica de comportamiento del algoritmo en función del número de ciudades
        with open("ej2_frecuencia_aparicion_valorlocal.txt", "a") as descriptor_file:

            for n_cities in range(exp_len_min, exp_len_max + 1):

                # Voy agregando de manera aleatoria el vector de ciudades
                datos = generador(n_cities)

                mejor_s = None

                s = simAnnealing(datos, t0)

                if mejor_s is None:
                    mejor_s = s

                # Realizaremos 500 iteraciones para intentar obtener la mejor solucion
                # por probabilidad

                # Limpiamos previamente frequencies para no tener valores anteriores

                frequencies_array.clear()

                for i in range(500):
                    s = simAnnealing(datos, t0)

                    # Voy agregando las frecuencias
                    frequencies_array.append(s[1])

                    if s[1] < mejor_s[1]:
                        mejor_s = s

                    # Imprimimos el mejor valor local encontrado en cada iteracion
                    # para asi realizar el muestro de: count(minimo global/local)/n iteraciones

                    """
                    s=simAnnealing(datos,t0)
                    print("--------------")
                    print("Solucion final: ",s[0])
                    print("Longitud de la ruta final: ",s[1])
                    """

                descriptor_file.write(f"{len(datos)} {get_laplace_probability(frequencies_array, mejor_s[1])}\n")

    # Experimento 2 para comprobar y utilizar las diferentes métricas de descenso de temperatura
    if EXECUTE_EXPERIMENT_2:
        t0 = 10  # Temperatura inicial para comenzar el descenso del valor
        n_cities = 30
        datos = generador(n_cities)

        s = simAnnealing(datos, t0)
        print("--------------")
        print("Solucion final: ", s[0])
        print("Longitud de la ruta final: ", s[1])

    # Experimento 3 para comprobar como mejora el algoritmo en función de la temperatura inicial T
    if EXECUTE_EXPERIMENT_3:
        t0_min = 10
        t0_max = 500
        t0_increment = 10

        n_cities = 20
        datos = generador(n_cities)

        for current_t0 in range(t0_min, t0_max + 1, t0_increment):
            s = simAnnealing(datos, current_t0)

            print("--------------")
            print("Solucion final: ", s[0])
            print("Longitud de la ruta final: ", s[1])
            print(f"{current_t0}")

            fichero = open("ej2_variacion_t0.txt", "a")
            fichero.write(f"{current_t0} {s[1]}\n")
            fichero.close()


if __name__ == "__main__":
    main()
