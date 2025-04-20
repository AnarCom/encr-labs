import argparse
from PIL import Image
import numpy as np
import sys
import os


def embed_message(input_image, output_image, message):
    """Внедрение сообщения в изображение"""
    try:
        img = Image.open(input_image)
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_image} не найден", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}", file=sys.stderr)
        return False

    if img.mode not in ['RGB', 'RGBA']:
        print("Ошибка: Изображение должно быть в режиме RGB или RGBA", file=sys.stderr)
        return False

    binary_message = ''.join([format(ord(c), '08b') for c in message])
    binary_message += '00000000'  # Маркер конца сообщения

    img_array = np.array(img)
    height, width, channels = img_array.shape

    max_message_length = height * width * 3 // 8
    if len(message) > max_message_length:
        print(f"Ошибка: Сообщение слишком длинное. Максимум: {max_message_length} символов", file=sys.stderr)
        return False

    message_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                if message_index < len(binary_message):
                    img_array[row, col, channel] = (img_array[row, col, channel] & 0xFE) | int(
                        binary_message[message_index])
                    message_index += 1
                else:
                    break
            if message_index >= len(binary_message):
                break
        if message_index >= len(binary_message):
            break

    try:
        result_img = Image.fromarray(img_array)
        result_img.save(output_image)
        print(f"Сообщение успешно внедрено в {output_image}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}", file=sys.stderr)
        return False


def extract_message(input_image):
    """Извлечение сообщения из изображения"""
    try:
        img = Image.open(input_image)
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_image} не найден", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}", file=sys.stderr)
        return None

    if img.mode not in ['RGB', 'RGBA']:
        print("Ошибка: Изображение должно быть в режиме RGB или RGBA", file=sys.stderr)
        return None

    img_array = np.array(img)
    height, width, channels = img_array.shape

    binary_message = []
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                lsb = str(img_array[row, col, channel] & 1)
                binary_message.append(lsb)

    message_bytes = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) < 8:
            break
        byte_str = ''.join(byte)
        byte_value = int(byte_str, 2)
        message_bytes.append(byte_value)

        if byte_value == 0:  # Маркер конца сообщения
            break

    return ''.join([chr(b) for b in message_bytes[:-1]])


def main():
    parser = argparse.ArgumentParser(
        description='LSB Replacement Tool - внедрение и извлечение сообщений из BMP изображений',
        epilog='Примеры использования:\n'
               '  lsb_tool.py -e input.bmp -o secret.bmp -m "секретное сообщение"\n'
               '  lsb_tool.py -x secret.bmp',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--embed', metavar='INPUT_BMP', help='Внедрить сообщение в изображение')
    group.add_argument('-x', '--extract', metavar='INPUT_BMP', help='Извлечь сообщение из изображения')

    parser.add_argument('-o', '--output', metavar='OUTPUT_BMP', help='Выходное изображение (для внедрения)')
    parser.add_argument('-m', '--message', help='Сообщение для внедрения')

    args = parser.parse_args()

    if args.embed:
        if not args.output:
            print("Ошибка: Для внедрения необходимо указать выходной файл (-o)", file=sys.stderr)
            sys.exit(1)
        if not args.message:
            print("Ошибка: Для внедрения необходимо указать сообщение (-m)", file=sys.stderr)
            sys.exit(1)

        success = embed_message(args.embed, args.output, args.message)
        if not success:
            sys.exit(1)

    elif args.extract:
        message = extract_message(args.extract)
        if message is not None:
            print("Извлеченное сообщение:", message)


if __name__ == '__main__':
    main()