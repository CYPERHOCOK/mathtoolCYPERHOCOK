"""Проверка последовательности и одиннадцать статистических показателей."""

import math

MAX_COUNT = 20
MAX_ABS = 10_000


def validate(values):
    """Проверить количество, конечность и диапазон чисел."""
    if not values:
        raise ValueError("последовательность пуста")
    if len(values) > MAX_COUNT:
        raise ValueError("количество чисел превышает 20")
    for value in values:
        if not math.isfinite(value):
            raise ValueError("число должно быть конечным")
        if abs(value) > MAX_ABS:
            raise ValueError("число вне допустимого диапазона")


def count(values):
    """Вернуть количество чисел."""
    return len(values)


def total(values):
    """Вычислить сумму последовательности."""
    result = 0.0
    for value in values:
        result += value
    return result


def mean(values):
    """Вычислить среднее арифметическое."""
    return total(values) / len(values)


def sum_squares(values):
    """Вычислить сумму квадратов чисел."""
    result = 0.0
    for value in values:
        result += value * value
    return result


def root_mean_square(values):
    """Вычислить корень из среднего квадратов чисел."""
    return math.sqrt(sum_squares(values) / len(values))


def squared_deviations(values):
    """Вычислить сумму квадратов отклонений вторым проходом."""
    average = mean(values)
    result = 0.0
    for value in values:
        result += (value - average) ** 2
    return result


def variance(values):
    """Вычислить дисперсию с делителем N."""
    return squared_deviations(values) / len(values)


def population_deviation(values):
    """Вычислить СКО с делителем N."""
    return math.sqrt(variance(values))


def sample_deviation(values):
    """Вернуть отклонение с делителем N-1 либо None при одном числе."""
    if len(values) < 2:
        return None
    return math.sqrt(squared_deviations(values) / (len(values) - 1))


def minimum(values):
    """Найти наименьшее число последовательности."""
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values):
    """Найти наибольшее число последовательности."""
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def positive_count(values):
    """Подсчитать строго положительные числа."""
    result = 0
    for value in values:
        if value > 0:
            result += 1
    return result


def negative_count(values):
    """Подсчитать строго отрицательные числа."""
    result = 0
    for value in values:
        if value < 0:
            result += 1
    return result


REPORT = (
    ("Количество", count, "d"),
    ("Сумма", total, ".3f"),
    ("Ср. арифм.", mean, ".3f"),
    ("Сумма кв.", sum_squares, ".3f"),
    ("Ср. кв.", root_mean_square, ".3f"),
    ("Дисперсия", variance, ".3f"),
    ("СКО", population_deviation, ".3f"),
    ("Станд. откл.", sample_deviation, ".3f"),
    ("Наименьшее", minimum, ".3f"),
    ("Наибольшее", maximum, ".3f"),
    ("Положительных", positive_count, "d"),
    ("Отрицательных", negative_count, "d"),
)
