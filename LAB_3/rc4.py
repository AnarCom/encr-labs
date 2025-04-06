import sys


class RC4:
    def __init__(self, key):
        self.S = list(range(256))
        self.i = self.j = 0

        # Инициализация KSA
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def generate_keystream(self, length):
        i, j = self.i, self.j
        keystream = []
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            keystream.append(self.S[(self.S[i] + self.S[j]) % 256])
        self.i, self.j = i, j
        return keystream


def rc4_cipher(input_file, key_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    with open(key_file, 'rb') as f:
        key = f.read()

    rc4 = RC4(key)
    keystream = rc4.generate_keystream(len(data))
    result = bytearray(a ^ b for a, b in zip(data, keystream))

    with open(output_file, 'wb') as f:
        f.write(result)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python rc4.py <входной_файл> <ключ> <выходной_файл>")
        sys.exit(1)
    input_file, key_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    rc4_cipher(input_file, key_file, output_file)
    print(f"Обработан {input_file} через RC4 -> {output_file}")