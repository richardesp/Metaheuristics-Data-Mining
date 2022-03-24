"""
    Prototipo main para posteriormente importar a Google Colab
"""

import random
import re


def main():
    path = "dataset_100_500.txt"

    with open(path, "r") as file:
        lines = file.readlines()
        list_patients = []
        patient_index = 0

        # Procesamos línea por línea el fichero
        for line in lines:
            regex = '[0-9]+:[A-Z]'

            # Por cada paciente almacenaremos un diccionario donde k = behaviour y v = lista de épocas
            dictionary_patient = {}
            for item in re.findall(regex, line):
                epoch, behaviour = item.split(':')

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

            print(f"Paciente 0: {list_patients[0]}")


if __name__ == "__main__":
    main()
