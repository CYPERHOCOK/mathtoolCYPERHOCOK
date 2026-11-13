"""Разбор команды и её параметров средствами argparse."""

import argparse

from calc.series import FORMULAS as SERIES_FORMULAS


def build_parser():
    """Создать разборщик с отдельными параметрами четырёх команд."""
    parser = argparse.ArgumentParser(
        prog="mathtool", description="Уравнения, статистика, ряды и интегралы.",
        allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command")
    solve = commands.add_parser("solve", help="Решение уравнения", allow_abbrev=False)
    for name in ("a", "b", "c"):
        solve.add_argument(f"-{name}", type=int, help=f"Целый коэффициент {name.upper()}, |значение| <= 10000")
    stats = commands.add_parser("stats", help="Показатели последовательности", allow_abbrev=False)
    stats.add_argument("--input", help="Файл UTF-8 с числами, иначе стандартный ввод")
    series = commands.add_parser("series", help="Сумма знакочередующегося ряда", allow_abbrev=False)
    series.add_argument("--func", choices=sorted(SERIES_FORMULAS), required=True, help="Имя ряда")
    stopping = series.add_mutually_exclusive_group(required=True)
    stopping.add_argument("--terms", type=int, help="Количество слагаемых от 1 до 10000")
    stopping.add_argument("--eps", type=float, help="Точность 0 < eps <= 0.0001")
    integrate = commands.add_parser("integrate", help="Метод левых прямоугольников", allow_abbrev=False)
    integrate.add_argument("--func", required=True, help="Имя подынтегральной функции")
    integrate.add_argument("--from", dest="start", type=float, required=True, help="Нижний предел")
    integrate.add_argument("--to", dest="end", type=float, required=True, help="Верхний предел")
    integrate.add_argument("--steps", type=int, required=True, help="Количество шагов от 1 до 100000")
    return parser
