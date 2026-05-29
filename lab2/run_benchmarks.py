import subprocess
import re
import sys
import os

# Размеры матриц и количество потоков для тестирования
sizes = [400, 800, 1200, 1600, 2000]
# 6 ядер / 12 потоков процессора Ryzen 5 6600H
threads_list = [1, 2, 4, 6, 12]

results = {size: {} for size in sizes}

print("=== Начинаем автоматическое тестирование OpenMP ===")
print("Это может занять несколько минут. Пожалуйста, не закрывайте терминал.\n")

for size in sizes:
    print(f"\n--- Генерация матриц размера {size}x{size} ---")
    subprocess.run([sys.executable, "gen.py", str(size)], check=True)
    
    for threads in threads_list:
        print(f"Запуск N={size} на {threads} потоках...", end="", flush=True)
        
        # Запуск C++ программы
        exec_path = "./main.exe" if os.path.exists("./main.exe") else "main.exe"
        process = subprocess.Popen([exec_path, str(threads)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        # Поиск строки с временем выполнения
        match = re.search(r"Execution time:\s*([\d\.]+)\s*seconds", stdout)
        if match:
            time_val = float(match.group(1))
            results[size][threads] = time_val
            print(f" Успешно! Время: {time_val:.6f}s")
        else:
            print(" Ошибка чтения результатов!")
            print(stdout, stderr)

print("\n=== Тестирование завершено! ===")
print("Готовая таблица для вашего отчета:\n")

# Формируем заголовок таблицы
header = "| Размер N | " + " | ".join(f"{t} Пот." for t in threads_list) + " |"
separator = "| :--- | " + " | ".join(":---:" for _ in threads_list) + " |"
print(header)
print(separator)

for size in sizes:
    row = f"| **{size}** | " + " | ".join(f"{results[size][t]:.6f}" for t in threads_list) + " |"
    print(row)

# Сохраняем результаты в файл для удобства
with open("benchmark_results.txt", "w", encoding="utf-8") as f:
    f.write(header + "\n")
    f.write(separator + "\n")
    for size in sizes:
        row = f"| **{size}** | " + " | ".join(f"{results[size][t]:.6f}" for t in threads_list) + " |"
        f.write(row + "\n")