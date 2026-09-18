"""Консольное приложение для решения уравнения A*x^2 + B*x + C = 0."""

import math
import sys


MAX_VALUE = 10_000


# 1. Разбор параметров командной строки
args = sys.argv[1:]

if len(args) == 0 or args[0] == "--help":
    print("mathtool — решение уравнений вида A*x^2 + B*x + C = 0")
    print("Использование:")
    print("  python mathtool.py                         вывод справки")
    print("  python mathtool.py --help                  вывод справки")
    print("  python mathtool.py solve                   ввод коэффициентов с клавиатуры")
    print("  python mathtool.py solve -a 1 -b -3 -c 2  решение с заданными коэффициентами")
    print("Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000.")
    sys.exit(0)

if args[0] != "solve":
    print("ОШИБКА: неизвестная команда", file=sys.stderr)
    sys.exit(1)


# 2. Получение коэффициентов и преобразование их в целые числа
try:
    if len(args) == 1:
        A = int(input("Введите A: "))
        B = int(input("Введите B: "))
        C = int(input("Введите C: "))
    elif len(args) == 7:
        if args[1] != "-a" or args[3] != "-b" or args[5] != "-c":
            print("ОШИБКА: неизвестный параметр", file=sys.stderr)
            sys.exit(1)

        A = int(args[2])
        B = int(args[4])
        C = int(args[6])
    else:
        print("ОШИБКА: неверный набор параметров", file=sys.stderr)
        sys.exit(1)
except ValueError:
    print("ОШИБКА: коэффициент не является целым числом", file=sys.stderr)
    sys.exit(1)


# 3. Проверка допустимого диапазона коэффициентов
if abs(A) > MAX_VALUE or abs(B) > MAX_VALUE or abs(C) > MAX_VALUE:
    print("ОШИБКА: значение вне допустимого диапазона", file=sys.stderr)
    sys.exit(1)


# 4. Определение вида уравнения, решение и вывод результата
if A == 0:
    if B != 0:
        print("Уравнение линейное")
        x = -C / B
        print(f"x = {x:.3f}")
    else:
        print("ОШИБКА: это не уравнение, неизвестное отсутствует", file=sys.stderr)
        sys.exit(1)
else:
    print("Уравнение квадратное")
    D = B * B - 4 * A * C
    print(f"D = {D}")

    if D > 0:
        x1 = (-B + math.sqrt(D)) / (2 * A)
        x2 = (-B - math.sqrt(D)) / (2 * A)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif D == 0:
        x = -B / (2 * A)
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")

sys.exit(0)
