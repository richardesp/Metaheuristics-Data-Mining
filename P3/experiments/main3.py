import random
import re
import time
from functools import lru_cache
import enum
import numpy as np
import string


@lru_cache(maxsize=65536)
def get_event_from_patient(patient: list, index_patient: int) -> str:
    return patient[index_patient]


def exist_pattern(pattern: str, patient: tuple) -> bool:
    index_pattern = len(pattern) - 1  # Vamos recorriendo de delante hacia atrás

    for index_patient in range(len(patient) - 1, -1, -1):

        # En el momento que encuentre la letra del patrón este ya existirá, por tanto seguimos viendo
        # si hay coincidencia en el paciente i-ésimo
        # Esto se debe a que no deben ir seguidos, sino que los eventos existan en cualquier momento del patrón
        # aunque AB, y A aparezca en la época 1 y B en la época 767 (por eso es un problema tan complejo)
        if get_event_from_patient(patient, index_patient) == pattern[index_pattern]:
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

    print("COMPROBAMDO TIEMPOS DE EJECUCIÓN ------->")

    mean = 0
    ejecuciones = 1000

    total_start = time.time()
    for index in range(ejecuciones):
        letters = string.ascii_lowercase
        pattern = ''.join(random.choice(letters) for i in range(10))
        start = time.time()
        evaluate_pattern(pattern, data)
        end = time.time()
        mean += (end - start)
    total_end = time.time()

    print(f"{(mean / ejecuciones) * 1000} ms con implementación default")
    print(f"Tiempo total en ejecutarse {ejecuciones} iteraciones: {total_end - total_start} s")
    default_ram = mean / ejecuciones

    # Procesamos previamente los datos para cachearlos
    for patient in data:
        for index in range(len(patient)):
            _ = get_event_from_patient(patient, index)

    mean = 0

    total_start = time.time()
    for index in range(ejecuciones):
        letters = string.ascii_lowercase
        pattern = ''.join(random.choice(letters) for i in range(10))
        start = time.time()
        evaluate_pattern(pattern, data)
        end = time.time()
        mean += (end - start)
    total_end = time.time()

    print(f"{(mean / ejecuciones) * 1000} ms con implementación cacheada")
    print(f"Tiempo total en ejecutarse {ejecuciones} iteraciones: {total_end - total_start} s")
    print("==================================")
    print(f"La mejora es de {default_ram / (mean / ejecuciones)} veces más rápido")


if __name__ == "__main__":
    main()
