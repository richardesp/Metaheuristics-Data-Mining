from math import log, pow


def default_cooldown_func(current_temperature: float) -> float:
    """
    Vanilla function for calculate the current temperature to decrease

    :param current_temperature:
    :return:
    """

    return 0.99 * current_temperature


def logarithmic_cooldown_func(current_temperature: float, it: int, alpha: float) -> float:
    """
    Logarithmic function for calculate the current temperature to decrease

    :param current_temperature:
    :param it:
    :param alpha:
    :return:
    """

    return alpha * current_temperature / log(1 + it)


def geometric_cooldown_func(current_temperature: float, it: int, alpha: float) -> float:
    """
    Geometric function for calculate the current temperature to decrease

    :param current_temperature:
    :param it:
    :param alpha:
    :return:
    """

    return pow(alpha, it) * current_temperature


def non_monotonic_adaptive_cooldown_func(best_length: int, current_length: int, current_temperature: float) -> float:
    """
    NOT WORKING:

    http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/

    :param best_length:
    :param current_length:
    :param current_temperature:
    :return:
    """

    return (1 + ((current_length - best_length) / current_length)) * current_temperature

#hola
def quadratic_multiplicative_cooling(current_temperature: float, cycle: int, fichero_temperaturas):
    """

    :param current_temperature:
    :param cycle:
    :return:
    """

    return current_temperature / (1 + 0.01 * pow(cycle, 2))
