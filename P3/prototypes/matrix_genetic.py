import random
import re
import time
from functools import lru_cache
import enum
import numpy as np
import string


def create_random_pattern_hill_climbing(events: tuple, length: int, data: list) -> str:
    pattern = ''
    count = 0

    event = random.choice(events)

    # Agregamos el evento inicial
    pattern += event

    # Buscamos los mejores vecinos posibles
    while count < length:

        best_frequency = 0.0
        best_event = events[0]
        for item in events:

            current_frequency = evaluate_pattern(pattern + item, data)
            if current_frequency > best_frequency:
                best_frequency = current_frequency
                best_event = item

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


def process_events(data: list) -> tuple:
    events = set()

    for patient in data:
        for item in patient:
            events.add(item)

    return tuple(events)


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
    pattern = create_random_pattern_hill_climbing(events, pattern_length, data)

    print(f"El patrón {pattern} aparece con una frecuencia de {evaluate_pattern(pattern, data)}")

    patterns_list = []
    nSoluciones = 100
    nGeneraciones = 1000
    start = time.time()
    for _ in range(nSoluciones):
        patterns_list.append(create_random_pattern_hill_climbing(events, pattern_length, data))

    for _ in range(nGeneraciones):
        for pattern in patterns_list:
            # print(f"Patrón {pattern} -> {evaluate_pattern(pattern, data)}")
            evaluate_pattern(pattern, data)
    end = time.time()

    print(f"Tiempo en evaluar {nSoluciones} patrones en {nGeneraciones} generaciones: {(end - start) * 1000} ms")


if __name__ == "__main__":
    main()
