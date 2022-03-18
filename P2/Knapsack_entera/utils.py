import random


def seleccionar_individuo(poblacion: list, k: int) -> list:
    candidatos_torneo = []

    # Seleccionamos k candidatos para el posterior torneo

    poblacion_aux = poblacion.copy()

    for i in range(k):
        individuo = poblacion_aux[random.randint(0, len(poblacion_aux) - 1)]
        #poblacion_aux.remove(individuo)
        candidatos_torneo.append(individuo)

    # Seleccionamos el ganador de los k individuos seleccionados

    max = candidatos_torneo[0][1]
    mejor_individuo = candidatos_torneo[0]

    for individuo in candidatos_torneo:
        if individuo[1] > max:
            max = individuo[1]
            mejor_individuo = individuo

    return mejor_individuo


def get_laplace_probability(frequencies: list, min_value: int) -> float:
    count = 0
    for frequency in frequencies:

        if min_value == frequency:
            count += 1

    return float(count / len(frequencies))
