import random
from utils import seleccionar_individuo

"""
    Anotaciones del profesor:

        Vamos a empezar con representación binaria, donde cada bit va a representar un item que va a contener la mochila,
        y el tamaño del cromosoma va a ser el tamaño de los productos (si tenemos 10 productos, el tamaño del cromosoma va
        a ser 10). Tenemos productos, peso y precio de los productos, donde buscamos MAXIMIZAR el precio de los productos 
        sin exceder la capacidad de la mochila. 

        Tenemos una población de soluciones donde puede ser mejor o peor (cada población tiene unos individuos con una serie
        de características)

        Un algoritmo evolutivo se basa en la vida real, tenemos una poblacion la cual se reproduce y tiene nuevos hijos, estos
        hijos pueden tener mutaciones (alteraciones genomicas) donde esa nueva población sera la que usemos, pasando evolutivamente
        de una poblacion A a una poblacion B (seleccion natural) ya que supuestamente ha de ser mejor la poblacion B dada la evolucion
        y la mejora al entorno (metafora para entender los algoritmos evolutivos). 

        Vamos a tener 4 módulos que vamos a tener que implementar, el primero es generar individuos, una primera población de la cual partir 
        para empezar a trabajar. El siguiente va a saber evaluar como de buenos son los individuos (cuanta cantidad de dinero estamos llevando
        con los productos en la mochila, f. evaluar). 

        Ahora comenzamos un bucle que se ejecuta N veces, donde iremos seleccionando individuos (seleccionamos n individuos con torneo, aleatoriamente
        , etc...) Esos individuos seleccionados para reproducirse se reproducen y van a generar un CRUZE, los cuales van a generar individuos nuevos
        que pueden mutarse o no, y con esos individuos genero una nueva población. Debo saber evaluar los nuevos individuos para saber si son mejores
        o peores (selección natural).

        Vamos a tener que implementar la seleccion, el cruze y la mutacion. 
        El cruze y la mutacion ocurren con una cierta probabilidad (como en la vida real), la probabilidad de un procreamiento exitoso entre hombre 
        y mujer no es del 100% siempre. Normalmente se pone "alta" ( > 0.7, 0.8) depende del problema. Cuando se tienen hijos, se produce una cierta
        alteración cromosomica, (probabilidad muy baja, aprox 0.1). 

        Se debe evitar el incesto, no deben cruzarse individuos practicamente iguales, porque van a ser iguales que los padres y las madres, no nos
        interesa para buscar nuevas soluciones mejores. 

        La seleccion por torneo es seleccionar el mejor individuo de un grupo, donde cogere k personas de una problacion, y de esas k personas me quedo
        con la mejor. Con eso conseguimos la selección natural. Los torneos con reemplazamiento, es coger los mejores individuos, los cruzo, y los
        devuelvo a la población. Con eso conseguimos que los individuos malos tengan menos probabilidades de reproducirse que los individuos buenos.

        Si tenemos una población de 100, y tenemos k=100, los mismos que se reproducen son los mejores, ya que selecciono los mejores de la población entera,
        llegariamos a una convergencia prematura (solucion). Si el tamaño del torneo (k) lo reducimos, estamos dando mas posibilidad de que esos que no
        son muy buenos, se cruzen con muy buenos, y me den nuevas zonas mejores de espacio de búsqueda. 

        Me queda el reemplzamiento, que son el generacional y el estacionario. Generacional, la nueva poblacion reemplaza completamente a la anterior,
        el estacionario, el mejor de la nueva poblacion reemplaza al peor de la anerior poblacion, la similitud entre una poblacion y otra es mayor
        (por tanto mas complejo de converger a una mejor solucion, tarda mas). Y el generacional puede descartar soluciones buenas que habia antes
        (menos conservador).

        Los cruces dependen del tipo de codificacion (nosotros estamos en binaria). Cruze en 1 punto, cruze en 2 puntos y con eso seria sufuciente 
        para la practica IMPORTANTE. Tengo 2 individuos nuevos que tienen media parte del padre y media parte de la madre, donde existen cruzes en 
        n puntos, intercambios diversos trozos del padre y diversos trozos de la madre. COMO VAMOS A TRABAJAR: elijo un gen del cromosoma y lo cambio:
        donde hay un 0, lo cambio por 1, y viceversa. 

        Cruze el que queramos (optimo para la mochila), mutacion el que queramos, y seleccion mediante torneo de tamaño k. 

        Como saber si el algoritmo se comporta bien o mal,

        si tenemos una grafica Aug Fitness y el numero de generaciones, una buena grafica es exponencial, pero se va a estancar

        Es como la grafica del acuraccy de un modelo de machine learning dado el numero de epocas (acuraccy)

        Debo calcular si el incremento dada la grafica esta por encima de un umbral, y paro el algoritmo para asi no hacer un estudio previo
        viendo la grafica. Es decir, si consigo en la generacion 20 obtener resultados, genial. Pero si el algoritmo mejora constantemente,
        entonces el algoritmo va a tardar muchisimo. Con eso podemos establecer un criterio de parada. 


        Puedo hacer una cosa, guardar la elite (mejores individuos, n individuos) para asi no "perderme" y volver a esos individuos por si no
        mejoro, lo que se suele hacer esque el AUG Fitness sea la elite.

        El avg de la elite siempre va a subir, aunque se estanque, pero NUNCA puede bajar. Mientras que la grafica de la poblacion seguramente
        tenga bajadas y le cueste mas subir. 

        SIEMPRE VA A MEJORAR.

        Debemos cambiar para empezar por CUALQUIER solucion, no por una solucion valida deterministica (hacer random de unos y ceros, y ya estaria)
        Eso va a afectar al rendimiento, dado que estoy partiendo de una parte alta de la grafica aug. Con la codificacion entera es hacer lo mismo,
        en vez de unos y ceros, pues selecciona del producto x me llevo y elementos. 

"""


def evaluarSolucion(solucion, precios, pesos, pesoMax):
    precio = 0
    peso = 0
    for i in range(len(solucion)):
        precio += precios[i] * solucion[i]
        peso += pesos[i] * solucion[i]

    if peso > pesoMax:  # Debemos maximizar la solucion
        return 0
    else:
        return precio


def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb):
    # Seleccionar padres mediante torneo tamaño k

    CRUCE_1_CUT = True

    # Cruce de un tajo con dos progenitores

    """
    No sé si es correcto borrar la anterior población y meter individuos en función de la anterior (modelo generacional, el que nos piden)
    """
    if CRUCE_1_CUT:
        # Como es un cruce con solo dos progenitores, necesitaré solo dos mejores candidatos de torneos de k individuos

        # El tamaño de la nueva población será aleatorio, basado en el tamaño anterior
        # n_poblacion_nueva = random.randint(int(poblacion.__len__() / 2), poblacion.__len__()) Esto no sería correcta ya que estadísticamente convergería a 0 elementos la población

        n_poblacion_nueva = poblacion.__len__()
        poblacion_nueva = []

        # Esto debe ser n/2 dado que inserto de 2 en 2
        for _ in range(int(n_poblacion_nueva / 2)):
            n_progenitores = 2
            progenitores = []

            for i in range(n_progenitores):
                progenitores.append(seleccionar_individuo(poblacion, k))

            tajo = random.randint(1, len(progenitores[0][0]) - 2)

            posible_cruce = []

            # Cruzar padres con probabilidad cProb
            if random.uniform(0, 1) <= cProb:

                # Estos elementos del tajo corresponden al progenitor 0
                for i in range(tajo + 1):
                    posible_cruce.append(progenitores[0][0][i])
                # Estos elementos del tajo corresponden al progenitor 1
                for i in range(tajo + 1, len(progenitores[1][0])):
                    posible_cruce.append(progenitores[1][0][i])

                # Si se da el cruze, lo agrego a la solucion actual para retornarlo (nuevo hijo)

                # Le pongo None para que posteiormente se evalue la solucion de esta nueva la mutacion
                poblacion_nueva.append([posible_cruce, None])

                # Insertamos el segundo hijo cruzando las mitades inversas
                posible_cruce = []

                # Estos elementos del tajo corresponden al progenitor 0
                for i in range(tajo + 1):
                    posible_cruce.append(progenitores[1][0][i])
                # Estos elementos del tajo corresponden al progenitor 1

                for i in range(tajo + 1, len(progenitores[1][0])):
                    posible_cruce.append(progenitores[0][0][i])

                # Si se da el cruze, lo agrego a la solucion actual para retornarlo (nuevo hijo)

                # Le pongo None para que posteiormente se evalue la solucion de esta nueva la mutacion
                poblacion_nueva.append([posible_cruce, None])

            # Si no se insertan los hijos entonces se insertan los padres
            else:
                for i in range(len(progenitores)):
                    poblacion_nueva.append(progenitores[i])

            # Puede darse una probabilidad de que los nuevos individuos muten
            if random.uniform(0, 1) <= mProb:

                # Va a mutar un bit de los dos nuevos individuos insertados
                ultimo_individuo = len(poblacion_nueva) - 1
                penultimo_individuo = ultimo_individuo - 1

                # Muta el último individuo insertado
                bit_mutable = random.randint(0, len(poblacion_nueva[ultimo_individuo][0]) - 1)
                poblacion_nueva[ultimo_individuo][0][bit_mutable] = int(not poblacion_nueva[ultimo_individuo][0][bit_mutable])

                # Muta el penúltimo individuo insertado
                bit_mutable = random.randint(0, len(poblacion_nueva[penultimo_individuo][0]) - 1)
                poblacion_nueva[penultimo_individuo][0][bit_mutable] = int(not poblacion_nueva[penultimo_individuo][0][bit_mutable])



            """
            # Mutar padres con probabilidad mProb
            if random.uniform(0, 1) <= mProb:
                # Va a mutar un bit de los dos padres
                for i in range(n_progenitores):
                    # Los progenitores se modifican por referencia de la lista de poblacion
                    # Seleccionamos el bit que vamos a modificar del progenitor i-esimo
                    bit_mutable = random.randint(0, len(progenitores[i][0]) - 1)
                    # Complemetamos el bit previo que tenia el progenitor i-esimo
                    progenitores[i][0][bit_mutable] = int(not progenitores[i][0][bit_mutable])
            """

    # Cruzar padres con probabilidad cProb
    # if random.randint(1,100) <= cProb:

    # Mutar padres con probabilidad mProb
    # if random.randint(1,100) <= mProb:

    # Antes estaba poblacion, pero habria que retornar las soluciones sin mas porque en el main despues se evaluan
    # estas soluciones para agregarlas a las poblaciones como pares de tuplas con el profit y la distribucion de la mochila
    return poblacion_nueva  # Devolver la nueva poblacion (sin evaluar)


def main():

    """ PRIMER PROBLEMA PLANTEADO
    # Solución óptima -> 637 (5 objetos)
    pesos = [34, 45, 14, 76, 32]
    precios = [340, 210, 87, 533, 112]
    pesoMax = 100  # Peso máximo que se puede poner en la mochila
    """

    """ SEGUNDO PROBLEMA PLANTEADO    
    # Solución óptima -> 2126 (10 objetos)
    pesos = [20, 12, 67, 34, 12, 34, 22, 34, 23, 12]
    precios = [340, 510, 671, 123, 54, 312, 421, 424, 341, 431]
    pesoMax = 100  # Peso máximo que se puede poner en la mochila
    """

    """ TERCER PROBLEMA PLANTEADO
    # Solución óptima -> 2426 (20 objetos)
    pesos = [34, 23, 54, 34, 23, 76, 21, 43, 12, 43, 67, 54, 12, 42, 32, 12, 67, 22, 45, 34]
    precios = [564, 231, 233, 785, 123, 674, 465, 345, 421, 412, 789, 567, 324, 565, 125, 431, 897, 321, 676, 321]
    pesoMax = 100  # Peso máximo que se puede poner en la mochila
    """

    # Solución óptima -> 5620 (50 objetos)
    pesos = [32, 23, 12, 56, 67, 45, 12, 8, 35, 23, 12, 54, 31, 12, 23, 34, 11, 32, 5, 12, 42, 23, 12, 54, 17, 11, 43,
             12, 23, 32, 12, 32, 12, 32, 43, 22, 43, 21, 43, 67, 32, 12, 32, 32, 32, 12, 43, 21, 32, 12]
    precios = [567, 453, 884, 215, 321, 321, 433, 231, 324, 432, 432, 564, 321, 565, 432, 456, 874, 674, 154, 123, 452,
               542, 542, 321, 654, 684, 535, 832, 245, 354, 267, 652, 543, 751, 531, 542, 652, 562, 532, 786, 325, 542,
               537, 143, 322, 536, 890, 562, 456, 343]
    pesoMax = 100  # Peso máximo que se puede poner en la mochila

    nSoluciones = 12  # Tamaño de la poblacion
    maxGeneraciones = 100  # Numero de generaciones
    k = 3  # Tamaño torneo selector de padres
    cProb = 0.7  # Probabilidad de cruce 0.7
    mProb = 0.3  # Probabilidad de mutacion 0.3

    """
    Debemos ver trucos para saber como seleccionar el nSoluciones, dado el problema. 

    l = longitud del cromosoma


    """

    l = len(pesos)
    ##Creamos n soluciones aleatorias que sean válidas
    # Cada elemento de poblacion son individuos (combinaciones de soluciones, donde fitness es el profit de la mochila)
    poblacion = []

    for i in range(nSoluciones):
        objetos = list(range(l))
        solucion = []
        peso = 0
        while peso < pesoMax and objetos:
            objeto = objetos[random.randint(0, len(objetos) - 1)]
            peso += pesos[objeto]
            if peso <= pesoMax:
                solucion.append(objeto)
                objetos.remove(objeto)

        s = []
        for i in range(l):
            s.append(0)
        for i in solucion:
            s[i] = 1

        poblacion.append([s, evaluarSolucion(s, precios, pesos, pesoMax)])  # Agrego la poblacion y como de buena es

    # Vamos a comprobar la mejor solución de la población inicial

    media = 0
    count = 0
    sbest = poblacion[0]

    for individuo in poblacion:
        media = media + individuo[1]
        count = count + 1
        if individuo[1] > sbest[1]:
            sbest = individuo

    media = media / count

    fichero_medias = open(f"valores_fitness_medias_poblacionales_por_iteracion_con_{nSoluciones}_individuos_con_{pesos.__len__()}_objetos.txt", "w")
    fichero_mejores = open(f"valores_fitness_mejor_individuo_por_iteracion_con_{nSoluciones}_individuos_con_{pesos.__len__()}_objetos.txt", "w")

    # Eje x
    it = 1

    fichero_medias.write(f"Iteraciones (eje x) Media de la población i-ésima (Eje y)\n")
    fichero_mejores .write(f"Iteraciones (eje x) Mejor individuo hasta el momento (Eje y)\n")

    fichero_medias.write(f"{it}\t\t\t\t\t{media}\n")
    fichero_mejores.write(f"{it}\t\t\t\t\t{sbest[1]}\n")

    print(f"Población inicial: {poblacion}")
    while it < maxGeneraciones:
        # Cuidado! si el número de individuos de la primera población es reducido y ejecuto muchas iteraciones las
        # nuevas generaciones, la probabilidad mprob puede provocar una población vacía (preguntar al profesor si lo
        # que estamos haciendo es correcto)
        nSoluciones = aplicarOperadoresGeneticos(poblacion, k, cProb, mProb)
        # Modelo generacional

        # POBLACION ESTA VACIO, VUELVO A CREARLO DE NUEVO
        poblacion = []
        media = 0
        count = 0
        for solucion in nSoluciones:
            # Genero nuevas posibles poblaciones para intentar mejorar
            poblacion.append([solucion[0], evaluarSolucion(solucion[0], precios, pesos, pesoMax)])

            media = media + individuo[1]
            count = count + 1

        for individuo in poblacion:
            media = media + individuo[1]
            count = count + 1
            if individuo[1] > sbest[1]:
                sbest = individuo

        media = media / count
        it += 1

        fichero_medias.write(f"{it}\t\t\t\t\t{media}\n")
        fichero_mejores.write(f"{it}\t\t\t\t\t{sbest[1]}\n")

        print(f"Población generada mediante selección generacional en la iteración {it}: {poblacion}")
    print(f"Mejor solucion encontrada mediante elitismo: {sbest[0]}, con una puntuacion de: {sbest[1]}")
    fichero_medias.close()
    fichero_mejores.close()


if __name__ == "__main__":
    main()