import sys
import os
import struct
import argparse


def tea_encrypt(block, key):
    """Шифрование 64-битного блока с использованием TEA"""
    v0, v1 = struct.unpack('!2I', block)
    k0, k1, k2, k3 = struct.unpack('!4I', key)

    delta = 0x9e3779b9
    sum_ = 0

    for _ in range(32):
        sum_ = (sum_ + delta) & 0xFFFFFFFF
        v0 = (v0 + ((v1 << 4) + k0 ^ v1 + sum_ ^ (v1 >> 5) + k1)) & 0xFFFFFFFF
        v1 = (v1 + ((v0 << 4) + k2 ^ v0 + sum_ ^ (v0 >> 5) + k3)) & 0xFFFFFFFF

    return struct.pack('!2I', v0, v1)


def tea_decrypt(block, key):
    """Дешифрование 64-битного блока с использованием TEA"""
    v0, v1 = struct.unpack('!2I', block)
    k0, k1, k2, k3 = struct.unpack('!4I', key)

    delta = 0x9e3779b9
    sum_ = (delta * 32) & 0xFFFFFFFF

    for _ in range(32):
        v1 = (v1 - ((v0 << 4) + k2 ^ v0 + sum_ ^ (v0 >> 5) + k3)) & 0xFFFFFFFF
        v0 = (v0 - ((v1 << 4) + k0 ^ v1 + sum_ ^ (v1 >> 5) + k1)) & 0xFFFFFFFF
        sum_ = (sum_ - delta) & 0xFFFFFFFF

    return struct.pack('!2I', v0, v1)


def pad_data(data):
    """Дополнение данных до размера, кратного 8 байтам"""
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)


def unpad_data(data):
    """Удаление дополнения из данных"""
    pad_len = data[-1]
    return data[:-pad_len]


def process_file(input_file, output_file, key, mode):
    """Обработка файла: шифрование или дешифрование"""
    block_size = 8  # 64 бита для TEA

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        if mode == 'encrypt':
            # Чтение и дополнение файла
            data = f_in.read()
            data = pad_data(data)

            # Шифрование по блокам
            for i in range(0, len(data), block_size):
                block = data[i:i + block_size]
                encrypted_block = tea_encrypt(block, key)
                f_out.write(encrypted_block)

        elif mode == 'decrypt':
            # Дешифрование по блокам
            while True:
                block = f_in.read(block_size)
                if not block:
                    break

                decrypted_block = tea_decrypt(block, key)

                # Удаление дополнения только для последнего блока
                if f_in.tell() == os.path.getsize(input_file):
                    decrypted_block = unpad_data(decrypted_block)

                f_out.write(decrypted_block)


def main():
    parser = argparse.ArgumentParser(description='Утилита для шифрования/дешифрования файлов с использованием TEA')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Режим работы: encrypt или decrypt')
    parser.add_argument('input_file', help='Входной файл')
    parser.add_argument('output_file', help='Выходной файл')
    parser.add_argument('key', help='Ключ шифрования (16 символов)')

    args = parser.parse_args()

    # Проверка ключа
    if len(args.key) != 16:
        print("Ошибка: ключ должен быть длиной 16 символов (128 бит)")
        sys.exit(1)

    # Преобразование ключа в байты
    key = args.key.encode('utf-8')

    # Проверка существования входного файла
    if not os.path.exists(args.input_file):
        print(f"Ошибка: файл {args.input_file} не существует")
        sys.exit(1)

    # Обработка файла
    try:
        process_file(args.input_file, args.output_file, key, args.mode)
        print(f"Файл успешно {'зашифрован' if args.mode == 'encrypt' else 'расшифрован'}")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()