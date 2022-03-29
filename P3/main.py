"""
    Prototipo main para posteriormente importar a Google Colab
"""

import random
import re
import time
import functools
import enum


def counts_frequency_of_occurrences(patient_list: [], event: str, epoch: int) -> float:
    """
    Function that traverses the array of patients calculating the frequency of occurrence of an event X at time Y.

    :param patient_list: List of patients with apnea
    :param event: Event that occurs
    :param epoch: Moment when the event occurs
    :return: Frequency of occurrence of event X at time Y
    """

    frequency = float(0)

    for patient in patient_list:
        if event in patient.keys():
            if epoch in patient[event]:
                frequency += 1

    return float(frequency / patient_list.__len__())


def main():
    path = "dataset_100_500.txt"
    list_patients = []

    with open(path, "r") as file:
        lines = file.readlines()
        patient_index = 0

        # Procesamos línea por línea el fichero
        for line in lines:
            regex = '[A-Z] [0-9]+'

            # Por cada paciente almacenaremos un diccionario donde k = behaviour y v = lista de épocas
            dictionary_patient = {}
            for item in re.findall(regex, line):
                behaviour, epoch = item.split(' ')

                if behaviour in dictionary_patient.keys():
                    pass
                else:
                    dictionary_patient[str(behaviour)] = []

                dictionary_patient[str(behaviour)].append(int(epoch))

            list_patients.append(dictionary_patient)

            # Convierto las listas del diccionario en frozensets para poder aplicar operadores de conjuntos
            for index in range(list_patients.__len__()):
                for key in list_patients[index]:
                    list_patients[index][key] = frozenset(list_patients[index][key])

    start_time = time.time()
    occurrence = counts_frequency_of_occurrences(list_patients, 'B', 1)
    end_time = time.time()
    print(
        f"La frecuencia de aparición del suceso B en la época 1 es {occurrence} ({(end_time - start_time) * 1000} ms)")
    print(list_patients[0])

if __name__ == "__main__":
    main()
