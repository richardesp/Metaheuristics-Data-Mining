def get_laplace_probability(frequencies: list, min_value: int) -> float:
    count = 0
    for frequency in frequencies:

        if min_value == frequency:
            count += 1

    return float(count/len(frequencies))