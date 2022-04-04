import random
import re
import time
from functools import lru_cache
import enum
import string


def random_mutation(events: list, parent: str) -> str:
    index_to_mutate = random.randint(0, len(parent) - 1)
    new_event = events[random.randint(0, len(events) - 1)]

    # Solo estoy mutando uno de los eventos
    replaces_count = 1

    # Debemos evitar que al mutar se mantenga el mismo evento, para así generar cambio
    while new_event == parent[index_to_mutate]:
        new_event = random.randint(0, len(events) - 1)

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

    print(cut)
    return child


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
    data = read_dataset('../datasets/dataset_100_500.txt')
    events = process_events(data)  # Conjunto de eventos posibles para así poder generar patrones aleatorios
    pattern_length = 7

    for index in range(len(data)):
        print(f"Paciente {index}: {data[index]}")

    pattern = create_random_pattern(events, pattern_length)
    pattern = create_random_valid_pattern(events, pattern_length, data)
    # pattern = create_random_pattern_hill_climbing(events, pattern_length, data)

    print(f"El patrón {pattern} aparece con una frecuencia de {evaluate_pattern(pattern, data)}")

    patterns_list = []

    # No puedo poner más de 20 porque solamente tengo 20 eventos
    nSoluciones = 20
    nGeneraciones = 7000

    print(f"Posibles eventos {events}")

    aux_events = events.copy()  # Creo una copia para iterar en el bucle, dado que iré borrando para evitar réplicas de individuos

    for _ in range(nSoluciones):
        patterns_list.append(create_random_pattern_hill_climbing(events, pattern_length, data, aux_events))

    for pattern in patterns_list:
        print(f"Patrón {pattern} aparece con una frecuencia de {evaluate_pattern(pattern, data)}")

    """
    start = time.time()
    for _ in range(nGeneraciones):
        for pattern in patterns_list:
            # print(f"Patrón {pattern} -> {evaluate_pattern(pattern, data)}")
            evaluate_pattern(pattern, data)
    end = time.time()
    """

    # print(f"Tiempo en evaluar {nSoluciones} patrones en {nGeneraciones} generaciones: {(end - start) * 1000} ms")

    pattern = 'AFCCCEE'
    print(f"{pattern} {evaluate_pattern(pattern, data)}")

    # SELECCIONAR POBLACIÓN INICIAL CON HILL CLIMBING

    # EJECUTO N GENERACIONES
    # HAGO CRUCE CON UNA PROB DE X
    # HAGO MUT CON UNA PROB DE Y

    parent = create_random_pattern(aux_events, pattern_length)
    print(parent)
    print(random_mutation(aux_events, parent))

if __name__ == "__main__":
    main()
