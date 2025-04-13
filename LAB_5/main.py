import hashlib


class HashPRNG:
    def __init__(self, seed):
        self.state = str(seed).encode('utf-8')

    def next_int(self, min_val=0, max_val=2 ** 32 - 1):
        hash_obj = hashlib.sha256(self.state)
        hash_hex = hash_obj.hexdigest()

        hash_int = int(hash_hex, 16)

        self.state = hash_hex.encode('utf-8')

        range_size = max_val - min_val + 1
        scaled_value = min_val + (hash_int % range_size)

        return scaled_value

    def next_float(self):
        hash_obj = hashlib.sha256(self.state)
        hash_hex = hash_obj.hexdigest()
        hash_int = int(hash_hex[:16], 16)

        self.state = hash_hex.encode('utf-8')

        return hash_int / (2 ** 64) # Нормализуем к [0,1)


if __name__ == "__main__":
    print("Генерация псевдослучайных чисел на основе хеш-функции SHA-256")
    print("-------------------------------------------------------")

    seed = input("Введите начальное значение (seed): ") or "default_seed"
    prng = HashPRNG(seed)

    print("\n10 случайных целых чисел от 0 до 100:")
    for _ in range(10):
        print(prng.next_int(0, 100), end=" ")

    print("\n\n10 случайных чисел с плавающей точкой [0, 1):")
    for _ in range(10):
        print(f"{prng.next_float():.6f}", end=" ")

    print("\n\n10 случайных больших целых чисел (от 1,000,000 до 9,999,999):")
    for _ in range(10):
        print(prng.next_int(1_000_000, 9_999_999), end=" ")

    print("\n")