"""Точка входа mathtool: ввод, вызов расчётов и вывод результатов."""

import sys

from calc import equation, integration, series, stats
from cli import build_parser


def handle_solve(args):
    """Получить коэффициенты и вывести решение уравнения."""
    a = args.a
    b = args.b
    c = args.c

    # Коэффициенты задаются либо все в команде, либо все с клавиатуры.
    if a is None and b is None and c is None:
        try:
            a = int(input("Введите A: "))
            b = int(input("Введите B: "))
            c = int(input("Введите C: "))
        except ValueError:
            raise ValueError("коэффициент не является целым числом") from None
    elif a is None or b is None or c is None:
        raise ValueError("укажите все три коэффициента либо ни одного")

    kind, discriminant, roots = equation.solve(a, b, c)
    print(f"Уравнение {kind}")
    if discriminant is not None:
        print(f"D = {discriminant}")
    if not roots:
        print("Действительных корней нет")
    elif len(roots) == 1:
        print(f"x = {roots[0]:.3f}")
    else:
        print(f"x1 = {roots[0]:.3f}")
        print(f"x2 = {roots[1]:.3f}")
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
        if value is None:
            print(f"{label}: НЕ СУЩЕСТВУЕТ")
        else:
            # form взят из таблицы: "d" для целого, ".3f" для дробного.
            print(f"{label}: {value:{form}}")
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


def handle_integrate(args):
    """Проверить пределы и вывести приближённый интеграл."""
    function, formula, low, high, inclusive = integration.FORMULAS[args.func]
    integration.validate(args.start, args.end, args.steps, low, high, inclusive)
    result = integration.integrate(function, args.start, args.end, args.steps)
    print(formula)
    print(f"Значение интеграла: {result:.{integration.DIGITS}f}")
    return 0


HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
}


def main(argv):
    """Разобрать параметры и вернуть код 0, 1 либо код ошибки argparse 2."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        # Сначала выбираем функцию по имени команды, затем вызываем её.
        handler = HANDLERS[args.command]
        return handler(args)
    except (ValueError, OSError, EOFError) as error:
        print(f"ОШИБКА: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
