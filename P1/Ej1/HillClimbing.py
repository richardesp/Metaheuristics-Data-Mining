import random
from TSPGenerator import generador
from utils import get_laplace_probability


def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud


def obtenerMejorVecino(solucion, datos):
    ##Obtención de los vecinos
    vecinos = []
    l = len(solucion)
    for i in range(l):
        for j in range(i + 1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtención del mejor vecino
    mejorVecino = vecinos[0]
    mejorLongitud = evaluarSolucion(datos, mejorVecino)
    for vecino in vecinos:
        longitud = evaluarSolucion(datos, vecino)
        if longitud < mejorLongitud:
            mejorLongitud = longitud
            mejorVecino = vecino
    return mejorVecino, mejorLongitud


"""
    Debo cambiar el estado inicial para poder encontrar soluciones
    perturbar puede ser generar de manera aleatoria una nueva instancia
    de hillclimbing
    
    Ejecuto N veces el programa y almaceno el menor coste de los estados solucion
    encontrados de manera aleatoria
"""


def hillClimbing(datos):
    l = len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)

    print("Longitud de la ruta: ", longitud)
    ##Obtenemos el mejor vecino hasta que no haya vecinos mejores
    vecino = obtenerMejorVecino(solucion, datos)
    while vecino[1] < longitud:
        solucion = vecino[0]
        longitud = vecino[1]
        print("Longitud de la ruta: ", longitud)
        vecino = obtenerMejorVecino(solucion, datos)

    return solucion, longitud


def main():
    exp_len_min = 4
    exp_len_max = 20

    EXECUTE_EXPERIMENT_1 = False
    EXECUTE_EXPERIMENT_2 = True

    frequencies_array = []

    if EXECUTE_EXPERIMENT_1:

        # Experimento 1 para generar la gráfica de comportamiento del algoritmo en función del número de ciudades
        with open("ej1_frecuencia_aparicion_valorlocal.txt", "a") as descriptor_file:

            for n_cities in range(exp_len_min, exp_len_max + 1):

                # Voy agregando de manera aleatoria el vector de ciudades
                datos = generador(n_cities)

                mejor_s = None

                s = hillClimbing(datos)

                if mejor_s is None:
                    mejor_s = s

                # Realizaremos 500 iteraciones para intentar obtener la mejor solucion
                # por probabilidad

                # Limpiamos previamente frequencies para no tener valores anteriores

                frequencies_array.clear()

                for i in range(500):
                    s = hillClimbing(datos)

                    # Voy agregando las frecuencias
                    frequencies_array.append(s[1])

                    if s[1] < mejor_s[1]:
                        mejor_s = s

                    # Imprimimos el mejor valor local encontrado en cada iteracion
                    # para asi realizar el muestro de: count(minimo global/local)/n iteraciones

                    """
                    print("--------------")
                    print("Hillclimbing con " + str(len(datos)) + " ciudades")
                    print("Solucion final: ", s[0])
                    print("Longitud de la ruta final: ", s[1])
                    """

                    print(f"{s[1]}")

                print("===================")
                print("Hillclimbing con " + str(len(datos)) + " ciudades")
                print("Solucion final de la ruta optima encontrada: ", mejor_s[0])
                print("Longitud de la ruta final optima encontrada: ", mejor_s[1])

                descriptor_file.write(f"{len(datos)} {get_laplace_probability(frequencies_array, mejor_s[1])}\n")

    if EXECUTE_EXPERIMENT_2:

        # Experimento 2 para generar la gráfica de evolución del mejor coste, en función del número de iteraciones para un TSP dado
        with open("ej1_mejora_longitud_dado_niteraciones.txt", "a") as descriptor_file:

            n_ciudades = 30  # Número considerable para ver la mejora existente dado el número de iteraciones
            datos = generador(n_ciudades)

            # Búsqueda de la variación de la longitud, incrementando de 10 en 10 el número de iteraciones
            # Partiendo de 10 iteraciones hasta 500 iteraciones

            max_iteraciones = 100
            incremento = 1

            for i in range(1, max_iteraciones + 1, incremento):

                # Limpiamos el mejor valor de longitud encontrado previamente
                mejor_s = None
                for j in range(i):
                    s = hillClimbing(datos)

                    if mejor_s is None:
                        mejor_s = s

                    # Almacenamos el mejor valor de longitud encontrado
                    if s[1] < mejor_s[1]:
                        mejor_s = s

                descriptor_file.write(f"{i} {mejor_s[1]}\n")


if __name__ == "__main__":
    main()
