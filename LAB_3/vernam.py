import sys


def vernam(input_file, key_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    with open(key_file, 'rb') as f:
        key = f.read()

    if len(key) < len(data):
        raise ValueError("Ключ короче данных")

    key = key[:len(data)]
    result = bytearray(a ^ b for a, b in zip(data, key))

    with open(output_file, 'wb') as f:
        f.write(result)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python vernam.py <входной_файл> <ключ> <выходной_файл>")
        sys.exit(1)
    input_file, key_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    vernam(input_file, key_file, output_file)
    print(f"Обработан {input_file} -> {output_file}")