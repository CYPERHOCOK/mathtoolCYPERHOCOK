"""Подынтегральные функции и метод левых прямоугольников."""

import math

MAX_STEPS = 100_000
DIGITS = 4


def ratio(value):
    """Вычислить x/(x+1)."""
    return value / (value + 1)


def root(value):
    """Вычислить sqrt(x²+1)."""
    return math.sqrt(value * value + 1)


FORMULAS = {
    "ratio": (ratio, "F(x) = x / (x + 1)", 0, 20, True),
    "root": (root, "F(x) = sqrt(x^2 + 1)", -5, 5, False),
}


def validate(start, end, steps, low, high, inclusive):
    """Проверить конечность пределов, их порядок, промежуток и шаги."""
    if not math.isfinite(start) or not math.isfinite(end):
        raise ValueError("предел должен быть конечным числом")
    if start >= end:
        raise ValueError("начальный предел не меньше конечного")
    for value in (start, end):
        inside = low <= value <= high if inclusive else low < value < high
        if not inside:
            raise ValueError("предел вне промежутка")
    if not 1 <= steps <= MAX_STEPS:
        raise ValueError("количество шагов вне диапазона")


def integrate(function, start, end, steps):
    """Вернуть сумму левых прямоугольников для проверенных параметров."""
    width = (end - start) / steps
    result = 0.0
    for index in range(steps):
        value = start + index * width
        result += function(value) * width
    return result
