"""Проверка коэффициентов и решение линейного или квадратного уравнения."""

import math

MAX_VALUE = 10_000


def validate_coefficients(coefficients):
    """Проверить диапазон именованных целых коэффициентов."""
    for name, value in coefficients.items():
        if not isinstance(value, int) or abs(value) > MAX_VALUE:
            raise ValueError(f"коэффициент {name} вне допустимого диапазона")
    if coefficients["A"] == 0 and coefficients["B"] == 0:
        raise ValueError("это не уравнение, неизвестное отсутствует")


def solve(a, b, c):
    """Вернуть вид уравнения, дискриминант и список действительных корней."""
    validate_coefficients({"A": a, "B": b, "C": c})
    if a == 0:
        return "линейное", None, [-c / b]
    discriminant = b * b - 4 * a * c
    if discriminant > 0:
        root = math.sqrt(discriminant)
        x1 = (-b + root) / (2 * a)
        x2 = (-b - root) / (2 * a)
        return "квадратное", discriminant, [x1, x2]
    if discriminant == 0:
        return "квадратное", discriminant, [-b / (2 * a)]
    return "квадратное", discriminant, []
