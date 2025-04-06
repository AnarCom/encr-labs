import sys

class LCG:
    def __init__(self, seed):
        self.seed = seed
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32

    def next_byte(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed & 0xFF  # Младший байт

def generate_key(output_file, size, seed):
    lcg = LCG(seed)
    key = bytearray()
    for _ in range(size):
        key.append(lcg.next_byte())
    with open(output_file, 'wb') as f:
        f.write(key)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python random_file_generator.py <выходной_файл> <размер> <seed>")
        sys.exit(1)
    output_file, size, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    generate_key(output_file, size, seed)
    print(f"Сгенерирован ключ {size} байт в {output_file}")