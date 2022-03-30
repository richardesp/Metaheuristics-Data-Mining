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
        if event_prev in patient.keys() and event_post in patient.keys():

            flag = False
            for epoch in patient[event_post]:
                for prev_item in prev_epochs:
                    if epoch >= prev_item:
                        frequency += 1
                        flag = True
                        break

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


def find_minimum_epoch(epochs: set) -> int:
    min = 0
    for epoch in epochs:
        if epoch < min:
            epoch = min

    return min

# Esta función calcula las posibles epocas posteriores dado un evento previo
def calculate_prev_epochs(prev_epochs: set, next: str, list_patients: list) -> set:

    prev_set = set()

    # Si no tiene previo porque es el primer evento del patrón
    if prev_epochs is None:
        for patient in list_patients:

            # Si el paciente iesimo ha padecido el evento
            if next in patient.keys():
                prev_set = prev_set.union(patient[next])

    # Tiene un evento previo con unas epocas de las cuales parte
    else:
        max_epoch = max(list(prev_epochs))

        # Si cualquiera de los siguientes eventos es mayor al evento mas tardio de los pacientes, se podra dar en todos
        for patient in list_patients:
            if next in patient.keys():
                for item in patient[next]:
                    if item > max_epoch:
                        # Agrego las posibles epocas mayores a la anterior (dado que deben suceder despues)
                        prev_set.add(item)

    # Retorno el conjunto de épocas de las cuales puede partir dado el último evento que sucedió en el patrón
    return prev_set

def main():
    path = "dataset_3_10.txt"
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


    ####################
    union_prev_sets = set()
    event_next = 'C' # Evento siguiente al cual ir
    prev_event = 'A' # Evento del que vengo, del cual tengo que calcular el conjunto de epocas donde tomarlo
    # este conjunto vendra dado si vengo de otra epoca necesariamente
    prev_event_epochs = list_patients[0]['A']
    min_prev_epoch = find_minimum_epoch(prev_event_epochs)

    # Voy a crear el conjunto de posible épocas que puede tomar B, sabiendo que antes va A con un conjunto de épocas dado

    #####################
    print("->")
    prev_B = calculate_prev_epochs(None, 'B', list_patients)
    print(prev_B)
    prev_C = calculate_prev_epochs(prev_B, 'C', list_patients)
    print("->")
    print(prev_C)
    start_time = time.time()
    occurrence = counts_frequency_of_occurrences_in_a_prev_event(list_patients, calculate_prev_epochs(None, 'A', list_patients), 'G', 'C')
    end_time = time.time()
    print(
        f"La frecuencia de aparición del suceso G tras C es {occurrence} ({(end_time - start_time) * 1000} ms)")
    occurrence = counts_frequency_of_occurrences(list_patients, 'M')
    print(
        f"La frecuencia de aparición del suceso F es {occurrence} ({(end_time - start_time) * 1000} ms)")


if __name__ == "__main__":
    main()
