"""Точка входа mathtool: ввод, вызов расчётов и вывод результатов."""

import sys

from calc import equation, series, stats
from cli import build_parser


def handle_solve(args):
    """Получить коэффициенты и вывести решение уравнения."""
    coefficients = (args.a, args.b, args.c)
    if all(value is None for value in coefficients):
        try:
            coefficients = tuple(int(input(f"Введите {name}: ")) for name in "ABC")
        except ValueError:
            raise ValueError("коэффициент не является целым числом") from None
    elif any(value is None for value in coefficients):
        raise ValueError("укажите все три коэффициента либо ни одного")
    kind, discriminant, roots = equation.solve(*coefficients)
    print(f"Уравнение {kind}")
    if discriminant is not None:
        print(f"D = {discriminant}")
    if not roots:
        print("Действительных корней нет")
    elif len(roots) == 1:
        print(f"x = {roots[0]:.3f}")
    else:
        for number, root in enumerate(roots, 1):
            print(f"x{number} = {root:.3f}")
    return 0


def read_numbers(source):
    """Прочитать не более MAX_COUNT чисел из строк потока."""
    values = []
    for line in source:
        for word in line.split():
            try:
                value = float(word)
            except ValueError:
                raise ValueError(f"{word} не является числом") from None
            values.append(value)
            if len(values) > stats.MAX_COUNT:
                raise ValueError("количество чисел превышает 20")
    stats.validate(values)
    return values


def handle_stats(args):
    """Прочитать файл или stdin и напечатать таблицу показателей."""
    if args.input is None:
        values = read_numbers(sys.stdin)
    else:
        try:
            with open(args.input, encoding="utf-8-sig") as source:
                values = read_numbers(source)
        except OSError:
            raise OSError("файл не открывается") from None
    for label, function, form in stats.REPORT:
        value = function(values)
        formatted = "НЕ СУЩЕСТВУЕТ" if value is None else f"{value:{form}}"
        print(f"{label}: {formatted}")
    return 0


def handle_series(args):
    """Посчитать ряд и вывести формулу только после успешного расчёта."""
    term, formula = series.FORMULAS[args.func]
    if args.terms is not None:
        result = series.sum_by_terms(term, args.terms)
        count = args.terms
    else:
        result, count = series.sum_by_eps(term, args.eps)
    print(formula)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{series.DIGITS}f}")
    return 0


HANDLERS = {"solve": handle_solve, "stats": handle_stats, "series": handle_series}


def main(argv):
    """Разобрать параметры и вернуть код 0, 1 либо код ошибки argparse 2."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        if args.command not in HANDLERS:
            raise ValueError("команда пока не реализована")
        return HANDLERS[args.command](args)
    except (ValueError, OSError, EOFError) as error:
        print(f"ОШИБКА: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
