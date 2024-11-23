import struct
import csv

def interpret(input_bin_file, output_csv_file, memory_range, log_file):
    with open(input_bin_file, 'rb') as f:
        binary_commands = f.read()

    # Инициализация памяти (например, 30 ячеек)
    memory = [0] * 256
    stack = []  # Стек для значений
    memory[0] = 25  # Примерная запись в память
    memory[1] = 10
    memory[2] = 15
    memory[3] = 30
    i = 0
    log_data = []  # Лог выполнения

    # Логирование операций стека
    log_stack_operations = []  # Здесь будем хранить логи операций стека

    # Получаем диапазон памяти
    memory_start, memory_end = memory_range

    # Убедимся, что диапазон не выходит за пределы
    if memory_end >= len(memory):
        print(f"Ошибка: диапазон памяти выходит за пределы. Размер памяти: {len(memory)}")
        return

    # Считываем данные из памяти в пределах заданного диапазона
    memory_data = [{"address": addr, "value": memory[addr]} for addr in range(memory_start, memory_end + 1)]

    while i < len(binary_commands):
        command_byte = binary_commands[i]
        A = command_byte  # 1 байт для команды
        i += 1

        if A == 3:  # LOAD_CONST
            B = struct.unpack(">H", binary_commands[i:i+2])[0]  # Следующие 2 байта для B
            i += 2
            stack.append(B)  # Помещаем константу на стек
            log_stack_operations.append(f"LOAD_CONST: добавили {B} в стек. Стек: {stack}")

        elif A == 4:  # READ_MEM
            B = binary_commands[i]  # Смещение (1 байт)
            i += 1
            address = stack.pop()  # Адрес из стека
            new_address = (address + B) % 256  # Адрес с учетом смещения
            value = memory[new_address]  # Чтение из памяти
            stack.append(value)  # Результат на стек
            log_stack_operations.append(f"READ_MEM: считали {value} с адреса {new_address}. Стек: {stack}")

        elif A == 6:  # WRITE_MEM
            value = stack.pop()  # Снимаем значение для записи
            address = stack.pop()  # Снимаем адрес
            new_address = address % 256  # Учитываем размер памяти
            memory[new_address] = value  # Записываем значение в память
            log_stack_operations.append(f"WRITE_MEM: записали {value} в память по адресу {new_address}. Стек: {stack}")
        elif A == 0:  # MIN
            B = struct.unpack(">H", binary_commands[i:i + 2])[0]  # Следующие 2 байта для адреса
            i += 2
            address = B % 256  # Адрес в памяти
            memory_value = memory[address]  # Значение из памяти
            if stack:  # Проверяем, что стек не пуст
                stack_value = stack.pop()  # Снимаем вершину стека
                result = min(stack_value, memory_value)  # Берем минимум
                stack.append(result)  # Результат на стек
                log_stack_operations.append(f"MIN: сравнили {memory_value} из памяти по адресу {address} со значением из стека {stack_value}.Результат записанный на вершину стека {result}. Стек: {stack}")
        # Логируем состояние
        log_data.append({
            "stack_top": stack[-1] if stack else None,  # Верхний элемент стека или None
            "command": f"{A}"
        })
    memory_start, memory_end = memory_range
    memory_data = [{"address": addr, "value": memory[addr]} for addr in range(memory_start, memory_end + 1)]
    # Записываем в CSV
    with open(output_csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["address", "value"])
        writer.writeheader()
        writer.writerows(memory_data)

    # Записываем логи операций стека в файл
    with open(log_file, 'w') as f:
        for log_entry in log_stack_operations:
            f.write(log_entry + "\n")


# Пример использования
interpret('output.bin', 'result.csv', (0, 3), 'stack_operations_log.txt')  # Логируем операции над стеком
