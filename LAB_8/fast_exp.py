import sys


def fast_exponentiation(a, b, c):
    result = 1
    a = a % c

    while b > 0:
        if b % 2 == 1:
            result = (result * a) % c
        b = b // 2
        a = (a * a) % c

    return result


def main():
    if len(sys.argv) != 4:
        print("Использование: python fast_exp.py <a> <b> <c>")
        print("Вычисляет a^b mod c с использованием быстрого возведения в степень")
        sys.exit(1)

    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        c = int(sys.argv[3])
    except ValueError:
        print("Ошибка: все аргументы должны быть целыми числами")
        sys.exit(1)

    if c == 0:
        print("Ошибка: модуль c не может быть нулем")
        sys.exit(1)

    if b < 0:
        print("Ошибка: показатель степени b должен быть неотрицательным")
        sys.exit(1)

    result = fast_exponentiation(a, b, c)
    print(f"{a}^{b} mod {c} = {result}")


if __name__ == "__main__":
    main()