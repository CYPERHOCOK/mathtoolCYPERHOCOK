"""Консольное приложение mathtool, лабораторная работа 2."""

import sys

from calc import equation
from cli import build_parser

parser = build_parser()
args = parser.parse_args()
if args.command is None:
    parser.print_help()
    sys.exit(0)
try:
    if args.command != "solve":
        raise ValueError("команда пока не реализована")
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
except (ValueError, OSError, EOFError) as error:
    print(f"ОШИБКА: {error}", file=sys.stderr)
    sys.exit(1)
sys.exit(0)