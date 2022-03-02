import random

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
        precio += precios[i]*solucion[i]
        peso += pesos[i]*solucion[i]

    if peso > pesoMax: # Debemos maximizar la solucion
        return 0
    else:
        return precio

def aplicarOperadoresGeneticos(poblacion, k, cProb, mProb):

    #Seleccionar padres mediante torneo tamaño k

    #Cruzar padres con probabilidad cProb
    #if random.randint(1,100) <= cProb:

    #Mutar padres con probabilidad mProb
    #if random.randint(1,100) <= mProb:


    return poblacion #Devolver la nueva poblacion (sin evaluar)

def main():
    pesos = [ 34, 45, 14, 76, 32 ]
    precios = [ 340, 210, 87, 533, 112 ]
    pesoMax = 100 #Peso máximo que se puede poner en la mochila
    nSoluciones = 25 #Tamaño de la poblacion
    maxGeneraciones = 1 #Numero de generaciones
    k = 3 #Tamaño torneo selector de padres
    cProb = 0.7 #Probabilidad de cruce
    mProb = 0.1 #Probabilidad de mutacion

    """
    Debemos ver trucos para saber como seleccionar el nSoluciones, dado el problema. 
    
    l = longitud del cromosoma
    
    
    """

    l=len(pesos)
    ##Creamos n soluciones aleatorias que sean válidas
    poblacion = []
    for i in range(nSoluciones):
        objetos = list(range(l))
        solucion = []
        peso = 0
        while peso < pesoMax:
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
        poblacion.append([s,evaluarSolucion(s,precios,pesos,pesoMax)]) # Agrego la poblacion y como de buena es

    it=1
    while it < maxGeneraciones:
        nSoluciones = aplicarOperadoresGeneticos(poblacion,k,cProb,mProb)
        #Modelo generacional
        poblacion = []
        for solucion in nSoluciones:
            poblacion.append([solucion[0],evaluarSolucion(solucion[0],precios,pesos,pesoMax)])
        it+=1

if __name__ == "__main__":
    main()
