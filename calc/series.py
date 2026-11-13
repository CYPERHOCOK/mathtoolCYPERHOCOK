"""Знакочередующиеся ряды и общие алгоритмы суммирования."""

import math

MAX_TERMS = 10_000
MAX_EPS = 0.0001
MAX_ITERATIONS = 100_000
DIGITS = math.ceil(-math.log10(MAX_EPS))


def sign(number):
    """Вернуть плюс для нечётного номера и минус для чётного."""
    if number % 2 == 0:
        return -1
    return 1


def third(number):
    """Вернуть слагаемое (-1)^(n+1)/(3n), n начинается с единицы."""
    return sign(number) / (3 * number)


def sqplus(number):
    """Вернуть слагаемое (-1)^(n+1)/(n²+1)."""
    return sign(number) / (number * number + 1)


FORMULAS = {
    "third": (third, "S = 1/3 - 1/6 + 1/9 - 1/12 + ..."),
    "sqplus": (sqplus, "S = 1/(1^2+1) - 1/(2^2+1) + 1/(3^2+1) - ..."),
}


def sum_by_terms(term, count):
    """Сложить count слагаемых переданной функции."""
    if not 1 <= count <= MAX_TERMS:
        raise ValueError("количество слагаемых вне диапазона")
    result = 0.0
    for number in range(1, count + 1):
        result += term(number)
    return result


def sum_by_eps(term, eps):
    """Суммировать до первого |слагаемое| < eps, включая его в сумму."""
    if not math.isfinite(eps) or not 0 < eps <= MAX_EPS:
        raise ValueError("точность вне диапазона")
    result = 0.0
    for number in range(1, MAX_ITERATIONS + 1):
        value = term(number)
        # Сначала добавляем слагаемое, затем проверяем условие остановки.
        result += value
        if abs(value) < eps:
            return result, number
    raise ValueError("точность не достигнута")
