import random

def generador(nCiudades):
    tsp = []
    for i in range(nCiudades):
        distancias = []
        for j in range(nCiudades):
            if j == i:
                distancias.append(0)
            elif j < i:
                distancias.append(tsp[j][i])
            else:
                distancias.append(random.randint(10, 1000))
        tsp.append(distancias)
    return tsp

def main():
    tsp = generador(10)
    for i in tsp:
        print(f"{i},")

if __name__ == "__main__":
    main()
