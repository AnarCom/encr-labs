import sys
import math
from collections import Counter


def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freqs = Counter(text)
    text_len = len(text)
    return -sum((count / text_len) * math.log2(count / text_len) for count in freqs.values())


def count_frequencies(text: str):
    freqs = Counter(text)
    for char, count in freqs.items():
        print(f"{repr(char)}: {count}")


def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла '{filename}': {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Использование:")
        print("  python script.py freq <строка>")
        print("  python script.py freq_file <файл>")
        print("  python script.py entropy <строка>")
        print("  python script.py entropy_file <файл>")
        sys.exit(1)

    command = sys.argv[1]
    argument = sys.argv[2]

    if command == "freq":
        count_frequencies(argument)
    elif command == "freq_file":
        text = read_file(argument)
        count_frequencies(text)
    elif command == "entropy":
        print(f"Энтропия: {shannon_entropy(argument):.4f}")
    elif command == "entropy_file":
        text = read_file(argument)
        print(f"Энтропия файла: {shannon_entropy(text):.4f}")
    else:
        print("Неизвестная команда.")
        sys.exit(1)


if __name__ == "__main__":
    main()
