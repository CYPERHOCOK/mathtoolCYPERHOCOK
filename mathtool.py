"""Точка входа mathtool: ввод, вызов расчётов и вывод результатов."""

import sys

from calc import equation
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


HANDLERS = {"solve": handle_solve}


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