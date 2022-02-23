import random
import math
from TSPGenerator import generador
from cooldown_functions import default_cooldown_func, non_monotonic_adaptive_cooldown_func, quadratic_multiplicative_cooling

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
        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]

        it+=1

        # Función para descender la temperatura
        #t=0.99*t

        t = quadratic_multiplicative_cooling(t, it)

        print("Longitud de la ruta: ", longitud)
        print("Temperatura: ", t)
    return solucion, longitud

def main():
    datos = [
        [0, 400, 500, 300],
        [400, 0, 300, 500],
        [500, 300, 0, 400],
        [300, 500, 400, 0]
    ]
    t0=10 # Temperatura inicial para comenzar el descenso del valor

#, fichero_temperaturas


    n_cities = 20

    datos = generador(n_cities)

    s=simAnnealing(datos,t0)
    print("--------------")
    print("Solucion final: ",s[0])
    print("Longitud de la ruta final: ",s[1])

if __name__ == "__main__":
    main()
