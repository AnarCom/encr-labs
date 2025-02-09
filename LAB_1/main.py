import argparse

from texttable import Texttable


def caesar_cipher(text, shift):
    result = ""

    # Проходим по каждому символу в тексте
    for char in text:
        # Проверяем, является ли символ строчной английской буквой
        if char.islower():
            # Вычисляем новую позицию символа с учетом сдвига
            new_pos = (ord(char) - ord('a') + shift) % 26
            # Преобразуем новую позицию обратно в символ
            result += chr(ord('a') + new_pos)
        else:
            # Если символ не является строчной английской буквой, оставляем его без изменений
            result += char

    return result


def encrypt(text, key):
    return caesar_cipher(text, key)


def decrypt(text, key):
    return caesar_cipher(text, -key)


def open_text(text1, text2):
    diff = abs(ord(text1[0]) - ord(text2[0]))
    return f'key = {diff}'


def closed_text(text):
    table = Texttable()
    table.set_cols_align(["l", "l"])
    table.add_row(["key", "result"])
    for i in range(1, 26):
        table.add_row([i, decrypt(text, i)])
    return table.draw()


def closed_text_with_dict(text1, text2):
    d = text2.split(",")
    table = Texttable()
    table.set_cols_align(["l", "l"])
    table.add_row(["key", "result"])
    for i in range(1, 26):
        decoded = decrypt(text1, i)
        for dict_value in d:
            if dict_value in decoded:
                table.add_row([i, decoded])
                break

    return table.draw()

def main():
    parser = argparse.ArgumentParser(description="Обработка текстовых данных")

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда encrypt
    encrypt_parser = subparsers.add_parser('encrypt', help='Зашифровать строку')
    encrypt_parser.add_argument('text', type=str, help='Строка для шифрования')
    encrypt_parser.add_argument('--key', type=int, required=True, help='Ключ для шифрования')

    # Команда decrypt
    decrypt_parser = subparsers.add_parser('decrypt', help='Расшифровать строку')
    decrypt_parser.add_argument('text', type=str, help='Строка для расшифровки')
    decrypt_parser.add_argument('--key', type=int, required=True, help='Ключ для расшифровки')

    # Команда open_text
    open_text_parser = subparsers.add_parser('open_text', help='Обработать две строки открытого текста')
    open_text_parser.add_argument('text1', type=str, help='Первая строка открытого текста')
    open_text_parser.add_argument('text2', type=str, help='Вторая строка открытого текста')

    # Команда closed_text
    closed_text_parser = subparsers.add_parser('closed_text', help='Обработать одну строку закрытого текста')
    closed_text_parser.add_argument('text', type=str, help='Строка закрытого текста')

    # Команда closed_text_with_dict
    closed_text_dict_parser = subparsers.add_parser('closed_text_with_dict',
                                                    help='Обработать две строки закрытого текста с использованием словаря')
    closed_text_dict_parser.add_argument('text1', type=str, help='Первая строка закрытого текста')
    closed_text_dict_parser.add_argument('text2', type=str, help='Вторая строка закрытого текста')

    args = parser.parse_args()

    if args.command == 'encrypt':
        result = encrypt(args.text, args.key)
        print(f"Encrypted Text: {result}")
    elif args.command == 'decrypt':
        result = decrypt(args.text, args.key)
        print(f"Decrypted Text: {result}")
    elif args.command == 'open_text':
        result = open_text(args.text1, args.text2)
        print(result)
    elif args.command == 'closed_text':
        result = closed_text(args.text)
        print(result)
    elif args.command == 'closed_text_with_dict':
        result = closed_text_with_dict(args.text1, args.text2)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
