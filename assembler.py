import struct
import csv

# Команды
COMMANDS = {
    "LOAD_CONST": 3,  # Загрузка константы
    "READ_MEM": 4,    # Чтение из памяти
    "WRITE_MEM": 6,   # Запись в память
    "MIN": 0,         # Бинарная операция MIN
}

def assemble(input_file, output_bin_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Массив для бинарных команд
    binary_commands = []

    # Лог для команд
    log_data = []

    for line in lines:
        parts = line.strip().split()
        command = parts[0]

        if command == "LOAD_CONST":
            operand = int(parts[1])
            A = COMMANDS[command]
            B = operand
            # Формируем команду: 3 байта (A, B)
            command_bytes = bytearray()
            command_bytes.append(A)
            command_bytes.extend(struct.pack(">H", B & 0xFFFF))  # 2 байта для B
            binary_commands.extend(command_bytes)

            # Логируем команду
            log_data.append({"command": command, "operand": operand, "binary": ','.join(f'0x{b:02X}' for b in command_bytes)})

        elif command == "READ_MEM":
            operand = int(parts[1])
            A = COMMANDS[command]
            B = operand
            # Формируем команду: 2 байта (A, B)
            command_bytes = bytearray()
            command_bytes.append(A)
            command_bytes.append(B & 0xFF)  # Смещение B в одном байте
            binary_commands.extend(command_bytes)

            # Логируем команду
            log_data.append({"command": command, "operand": operand, "binary": ','.join(f'0x{b:02X}' for b in command_bytes)})

        elif command == "WRITE_MEM":
            A = COMMANDS[command]
            # Формируем команду: 1 байт (A)
            command_bytes = bytearray()
            command_bytes.append(A)
            binary_commands.extend(command_bytes)

            # Логируем команду
            log_data.append({"command": command, "operand": None, "binary": ','.join(f'0x{b:02X}' for b in command_bytes)})

        elif command == "MIN":
            operand = int(parts[1])
            A = COMMANDS[command]
            B = operand
            # Формируем команду: 3 байта (A, B)
            command_bytes = bytearray()
            command_bytes.append(A)
            command_bytes.extend(struct.pack(">H", B & 0xFFFF))  # 2 байта для B
            binary_commands.extend(command_bytes)

            # Логируем команду
            log_data.append({"command": command, "operand": operand, "binary": ','.join(f'0x{b:02X}' for b in command_bytes)})

    # Записываем бинарный файл
    with open(output_bin_file, 'wb') as f:
        f.write(bytearray(binary_commands))

    # Записываем лог в CSV
    with open(log_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["command", "operand", "binary"])
        writer.writeheader()
        writer.writerows(log_data)

# Пример использования
assemble('test.txt', 'output.bin', 'log.csv')
