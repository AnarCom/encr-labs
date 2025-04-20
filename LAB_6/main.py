def baby_step_giant_step(g, h, p):
    print(f"Решаем уравнение {g}^x ≡ {h} mod {p}")

    m = int((p - 1) ** 0.5) + 1
    k = m

    print(f"Автоматически выбраны параметры: m = {m}, k = {m}")

    # Шаг младенца: вычисляем и сохраняем g^j mod p для j от 0 до m-1
    baby_steps = {}
    current = 1
    mul_count = 0

    print("\nШаг младенца: вычисляем g^j mod p для j от 0 до m-1")
    for j in range(m):
        baby_steps[current] = j
        print(f"j = {j}: {g}^{j} ≡ {current} mod {p}")
        if j < m - 1:
            current = (current * g) % p
            mul_count += 1

    # Вычисляем g^(-m) mod p
    g_m = pow(g, m * (p - 2), p)
    mul_count += 1

    print(f"\nВычисляем g^(-m) ≡ {g_m} mod {p}")
    print("\nШаг великана: ищем совпадение h*(g^-m)^i в таблице")
    current = h
    for i in range(m):
        print(f"i = {i}: проверяем {current}")
        if current in baby_steps:
            j = baby_steps[current]
            x = i * m + j
            print(f"\nНайдено совпадение при i = {i}, j = {j}")
            print(f"Решение: x = i*m + j = {i}*{m} + {j} = {x}")
            print(f"Проверка: {g}^{x} mod {p} = {pow(g, x, p)} (ожидалось {h})")
            print(f"Всего выполнено умножений: {mul_count}")
            return x, mul_count

        current = (current * g_m) % p
        mul_count += 1

    print("Решение не найдено")
    return None, mul_count


def brute_force_dlp(g, h, p):
    print(f"Решаем уравнение {g}^x ≡ {h} mod {p} методом полного перебора")

    current = 1
    mul_count = 0

    for x in range(p):
        if current == h:
            print(f"Найдено решение: x = {x}")
            print(f"Проверка: {g}^{x} mod {p} = {current} (ожидалось {h})")
            print(f"Всего выполнено умножений: {mul_count}")
            return x, mul_count

        if x < p - 1:
            current = (current * g) % p
            mul_count += 1

        if x % 1000 == 0 and x != 0:
            print(f"Проверено {x} значений...")

    print("Решение не найдено")
    return None, mul_count


# Пример использования
if __name__ == "__main__":
    g, h, p = 2, 9, 11
    print("=== Метод Шэнкса ===")
    x1, mul1 = baby_step_giant_step(g, h, p)
    print("\n=== Метод полного перебора ===")
    x2, mul2 = brute_force_dlp(g, h, p)

    print("\nСравнение методов:")
    print(f"Метод Шэнкса: {mul1} умножений")
    print(f"Полный перебор: {mul2} умножений")

    g, h, p = 2, 12345678, 100000007
    print("\n\n=== Тест на больших числах ===")
    print("=== Метод Шэнкса ===")
    x1, mul1 = baby_step_giant_step(g, h, p)
    print("\n=== Метод полного перебора ===")
    x2, mul2 = brute_force_dlp(g, h, p)

    print("\nСравнение методов:")
    print(f"Метод Шэнкса: {mul1} умножений")
    print(f"Полный перебор: {mul2} умножений")