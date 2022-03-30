"""
    Prototipo main para posteriormente importar a Google Colab
"""

import random
import re
import time
import functools
import enum


def counts_frequency_of_occurrences_in_a_prev_event(patient_list: [], prev_epochs: set,
                                                    event_post: str, event_prev: str) -> float:
    frequency = 0

    for patient in patient_list:
        print(f"{patient}")
        if event_prev in patient.keys() and event_post in patient.keys():

            flag = False
            for epoch in patient[event_post]:
                for prev_item in prev_epochs:
                    if epoch >= prev_item:
                        frequency += 1
                        flag = True
                        break
                        print("SUMA")

                    if flag:
                        break
                if flag:
                    break

    return float(frequency / patient_list.__len__())


def counts_frequency_of_occurrences(patient_list: [], event: str) -> float:
    """
    Function that traverses the array of patients calculating the frequency of occurrence of an event X at time Y.
    :param patient_list: List of patients with apnea
    :param event: Event that occurs
    :param epoch: Moment when the event occurs
    :return: Frequency of occurrence of event X at time Y
    """

    frequency = 0

    for patient in patient_list:
        for key in patient.keys():
            if event == key:
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
                    list_patients[index][key] = set(list_patients[index][key])

    print(f"Paciente 0: {list_patients[0]}")
    start_time = time.time()
    occurrence = counts_frequency_of_occurrences(list_patients, 'A')
    end_time = time.time()
    print(
        f"La frecuencia de aparición del suceso A es {occurrence} ({(end_time - start_time) * 1000} ms)")


    union_prev_sets = set()
    event = 'A'

    # Voy a crear el conjunto de posible épocas que puede tomar A
    for patient in list_patients:
        if event in patient.keys():
            union_prev_sets = union_prev_sets.union(patient[event])

    start_time = time.time()
    occurrence = counts_frequency_of_occurrences_in_a_prev_event(list_patients, list_patients[0]['J'], 'C', 'J')
    end_time = time.time()
    print(
        f"La frecuencia de aparición del suceso C tras B es {occurrence} ({(end_time - start_time) * 1000} ms)")
    occurrence = counts_frequency_of_occurrences(list_patients, 'J')
    print(
        f"La frecuencia de aparición del suceso B es {occurrence} ({(end_time - start_time) * 1000} ms)")


if __name__ == "__main__":
    main()
