import random
import re
import time
from functools import lru_cache
import enum
import numpy as np

@lru_cache(maxsize=65536)
def exist_pattern_cached(pattern: str, patient: tuple) -> bool:
    index_pattern = len(pattern) - 1  # Vamos recorriendo de delante hacia atrás

    for index_patient in range(len(patient) - 1, -1, -1):
        if patient[index_patient] == pattern[index_pattern]:
            index_pattern = index_pattern - 1

        # Habremos acabo de recorrer el patrón
        if index_pattern < 0:
            break

    return index_pattern == -1

@lru_cache(maxsize=65536)
def evaluate_pattern_cached(pattern: str, data: tuple) -> float:
    frequency = 0

    # Realizamos un recorrido inverso para ver si el patrón ha aparecido previamente
    for patient in data:
        if exist_pattern_cached(pattern, patient):
            frequency += 1

    return float(frequency / data.__len__())

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
    frequency = 0

    # Realizamos un recorrido inverso para ver si el patrón ha aparecido previamente
    for patient in data:
        if exist_pattern(pattern, patient):
            frequency += 1

    return float(frequency / data.__len__())


@lru_cache(maxsize=65536)
def process_data(data: tuple) -> None:
    """
    Esta función nos permite almacenar en caché la matriz lo cual lo hace muy eficiente

    :param data:
    :return:
    """
    count = 0
    for patient in data:
        for event in patient:
            ++count


@lru_cache(maxsize=65536)
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
    data = read_dataset('dataset_100_500.txt')

    for index in range(len(data)):
        print(f"Paciente {index}: {data[index]}")

    start = time.time()
    process_data(data)
    end = time.time()
    print(f"{(end - start) * 1000} ms")
    default_ram = end - start

    mean = 0

    for _ in range(100000):
        start = time.time()
        process_data(data)
        end = time.time()
        mean += (end - start)

    print(f"{(mean / 100000) * 1000} ms")
    print(f"La mejora es de {default_ram / (mean / 100000)} veces más rápido")

    print(evaluate_pattern('ABC', data))

    pattern = 'C'
    print(f"El patrón {pattern} tiene una probabilidad de aparición de {evaluate_pattern(pattern, data)}")

    # COMPROBAMDO TIEMPOS DE EJECUCIÓN
    print("COMPROBAMDO TIEMPOS DE EJECUCIÓN ------->")
    pattern = 'ABB'

    mean = 0
    ejecuciones = 100

    for _ in range(ejecuciones):
        start = time.time()
        evaluate_pattern(pattern, data)
        end = time.time()
        mean += (end - start)

    print(f"{(mean / ejecuciones) * 1000} ms con implementación default")
    default_ram = mean / ejecuciones

    mean = 0

    for index in range(ejecuciones):
        start = time.time()
        evaluate_pattern_cached(pattern, data)
        end = time.time()
        mean += (end - start)

    print(f"{(mean / ejecuciones) * 1000} ms con implementación cacheada")
    print(f"La mejora es de {default_ram / (mean / ejecuciones)} veces más rápido")

    #################################

if __name__ == "__main__":
    main()
