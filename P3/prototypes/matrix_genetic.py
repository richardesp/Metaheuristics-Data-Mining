import random
import re
import time
from functools import lru_cache
import enum
import string


def take_second(elem):
    return elem[1]


def find_worst(bests_individuals: list):
    worst = 1
    for x in range(len(bests_individuals)):
        if worst > bests_individuals[x, 1]:
            worst = bests_individuals[x, 1]
    return worst


def find_bests(poblation: list, bests_individuals: list):
    # cuando se introduce un elemento en la élite se elimina de la población
    for x in poblation:
        if find_worst(bests_individuals) < x[1]:
            bests_individuals[9] = x
            bests_individuals = sorted(bests_individuals, reverse=True, key=take_second)


def apply_tournament(poblation: list, k: int) -> str:
    candidates = []

    aux_poblation = poblation.copy()

    for _ in range(k):
        pattern = random.choice(aux_poblation)
        aux_poblation.remove(pattern)
        candidates.append(pattern)

    best_frequency = candidates[0][1]
    best_pattern = candidates[0]

    for pattern in candidates:
        if pattern[1] > best_frequency:
            best_frequency = pattern[1]
            best_pattern = pattern

    return best_pattern


def apply_genetic_operator(poblation: list, k: int, c_prob: float, m_prob: float, data: list, events: list) -> list:
    CUT_1_CROSS = True
    new_poblation = []

    if CUT_1_CROSS:
        for _ in range(int(poblation.__len__() / 2)):
            parent_1 = apply_tournament(poblation, k)

            # Seleccionamos a otro individuo que no haya sido seleccionado previamente
            poblation_2 = poblation.copy()
            poblation_2.remove(parent_1)
            parent_2 = apply_tournament(poblation_2, k)

            if random.uniform(0, 1) <= c_prob:
                child_1 = cut_1_cross(parent_1[0], parent_2[0])  # Le pasamos el patrón en cuestión
                # new_poblation.append([new_child, evaluate_pattern(new_child, data)])

                child_2 = cut_1_cross(parent_2[0], parent_1[0])
                # new_poblation.append([new_child, evaluate_pattern(new_child, data)])

                parent_1[0] = child_1
                parent_2[0] = child_2

            # Probabilidad de mutar el primer padre
            if random.uniform(0, 1) <= m_prob:
                parent_1[0] = random_mutation(events, parent_1[0])
                # parent_1[1] = evaluate_pattern(parent_1[0], data) No es necesario

            # Probabilidad de mutar el segundo padre
            if random.uniform(0, 1) <= m_prob:
                parent_2[0] = random_mutation(events, parent_2[0])
                # parent_2[1] = evaluate_pattern(parent_2[0], data) No es necesario

            # Agregamos los individuos resultantes y los evaluamos
            new_poblation.append([parent_1[0], evaluate_pattern(parent_1[0], data)])
            new_poblation.append([parent_2[0], evaluate_pattern(parent_2[0], data)])

    return new_poblation


def random_mutation(events: list, parent: str) -> str:
    index_to_mutate = random.randint(0, len(parent) - 1)
    new_event = events[random.randint(0, len(events) - 1)]

    # Solo estoy mutando uno de los eventos
    replaces_count = 1

    # Debemos evitar que al mutar se mantenga el mismo evento, para así generar cambio
    while new_event == parent[index_to_mutate]:
        new_event = events[random.randint(0, len(events) - 1)]

    new_parent = parent.replace(parent[index_to_mutate], new_event, replaces_count)

    return new_parent


def cut_1_cross(parent_1: str, parent_2: str) -> str:
    child = ''
    parents_length = len(parent_1)

    # Tajo desde el elemento 1 hasta el n-2 (para evitar réplicas totales de un padre)
    cut = random.randint(1, parents_length - 2)

    for i in range(cut + 1):
        child += parent_1[i]

    for i in range(cut + 1, parents_length):
        child += parent_2[i]

    return child


def create_random_pattern_hill_climbing_with_roulette(events: list, length: int, data: list) -> str:
    pattern = ''
    count = 1

    event = random.choice(events)

    # Agregamos el evento inicial
    pattern += event

    # Buscamos todos los mejores vecinos para aplicar una ruleta
    while count < length:
        frequencies_sum = float(0)
        current_posible_patterns = []

        for item in events:
            current_frequency = evaluate_pattern(pattern + item, data)
            current_posible_patterns.append([pattern + item, current_frequency])

            frequencies_sum += current_frequency

        # Si no he seleccionado ningun patron en la ruleta selecciono uno aleatorio
        posible_pattern_selected = False

        # Tengo ya los posibles eventos para realizar el torneo mediante ruleta
        for posible_pattern in current_posible_patterns:

            # Cogeré el elemento con una probabilidad entre la suma de las posibles
            if (frequencies_sum != 0) and (random.uniform(0, 1) <= (posible_pattern[1] / frequencies_sum)):
                posible_pattern_selected = True
                pattern = posible_pattern[0]

                # Terminamos de ejecutar puesto que ya hemos agregado el patrón al ganar la ruleta
                break

        if not posible_pattern_selected:
            pattern += random.choice(events)

        count = count + 1

    return pattern


def create_random_pattern_hill_climbing(events: list, length: int, data: list, aux_events: list) -> str:
    pattern = ''
    count = 1

    event = random.choice(events)

    # Voy borrando eventos para así comenzar con otros nuevos posibles
    events.remove(event)

    # Agregamos el evento inicial
    pattern += event

    # Buscamos los mejores vecinos posibles
    while count < length:

        best_frequency = 0.0
        best_event = ''
        for item in aux_events:

            current_frequency = evaluate_pattern(pattern + item, data)
            if current_frequency > best_frequency:
                best_frequency = current_frequency
                best_event = item

        # Si no ha encontrado nada mejor a 0.0, selecciono cualquier evento
        if best_event == '':
            best_event = random.choice(events)

        pattern += best_event
        count = count + 1

    return pattern


def create_random_valid_pattern(events: tuple, length: int, data: list) -> str:
    pattern = ''
    count = 0

    for _ in range(length):
        pattern += random.choice(events)

        if evaluate_pattern(pattern, data) == 0:

            # Eliminamos el último evento
            pattern = pattern[:-1]

            # Seleccionamos un paciente aleatorio
            for item in random.choice(data):
                pattern += item

                if evaluate_pattern(pattern, data) != 0:
                    break

                else:
                    pattern = pattern[:-1]

    return pattern


def create_random_pattern(events: tuple, length: int) -> str:
    pattern = ''

    for _ in range(length):
        pattern += random.choice(events)

    return pattern


def process_events(data: list) -> list:
    events = set()

    for patient in data:
        for item in patient:
            events.add(item)

    return list(tuple(events))


def exist_pattern(pattern: str, patient: tuple) -> bool:
    index_pattern = len(pattern) - 1  # Vamos recorriendo de delante hacia atrás

    for index_patient in range(len(patient) - 1, -1, -1):
        if patient[index_patient] == pattern[index_pattern]:
            index_pattern = index_pattern - 1

        # Habremos acabo de recorrer el patrón
        if index_pattern < 0:
            break

    return index_pattern == -1


@lru_cache(maxsize=65536)
def evaluate_pattern(pattern: str, data: tuple) -> float:
    # EJECUTAR DE PRIMERA EN EL PRIMER BLOQUE DE COLAB PARA CACHEAR RAPIDAMENTE LA INFO
    frequency = 0

    # Realizamos un recorrido inverso para ver si el patrón ha aparecido previamente
    for patient in data:
        if exist_pattern(pattern, patient):
            frequency += 1

    return float(frequency / data.__len__())


def read_dataset(path: str) -> tuple:
    list_patients = []

    with open(path, "r") as file:
        lines = file.readlines()
        patient_index = 0

        # Procesamos línea por línea el fichero
        for line in lines:
            regex = '[A-Z] [0-9]+'

            # Por cada paciente almacenaremos un diccionario donde k = behaviour y v = lista de épocas
            pattern_patient = []
            for item in re.findall(regex, line):
                behaviour, epoch = item.split(' ')

                pattern_patient.append(behaviour)

            list_patients.append(tuple(pattern_patient))

    return tuple(list_patients)


def main():
    start = time.time()
    verbose = True  # Modo verbose para imprimir

    data = read_dataset('../datasets/dataset_100_500.txt')
    events = process_events(data)  # Conjunto de eventos posibles para así poder generar patrones aleatorios
    pattern_length = 7
    n_solutions = 100
    n_generations = 1
    c_prob = .7
    m_prob = .2
    k = 3
    poblation = []

    old_events = events.copy()  # Copia previa de los eventos dado que se van a eliminar en hill Climbing
    bests_individuals = []
    # creo unicamente tres espacios y los relleno de basura que luego iremos cambiando para guardar en ellos las mejores soluciones

    n_bests = 10

    for _ in range(n_bests):
        bests_individuals.append([None, 0])

    for _ in range(n_solutions):
        random_pattern = create_random_pattern_hill_climbing_with_roulette(events, pattern_length, data)
        poblation.append([random_pattern, evaluate_pattern(random_pattern, data)])
        # bests_individuals = find_bests(poblation, bests_individuals)

    it = 1

    if verbose:
        print(f"Iteración {it}: {poblation}")

    it += 1
    while it <= n_generations:
        poblation = apply_genetic_operator(poblation, k, c_prob, m_prob, data, old_events)

        if verbose:
            print(f"Iteración {it}: {poblation}")

        it += 1

    end = time.time()
    print(f"Tiempo de ejecución: {(end - start) * 1000} ms")


if __name__ == "__main__":
    main()
