# dz4_config
# Описание проекта: Ассемблер и Интерпретатор
## Данный проект включает два основных компонента: `Ассемблер` и `Интерпретатор`, предназначенные для обработки и выполнения команд в бинарном формате. Ассемблер преобразует текстовые команды в бинарный формат, а интерпретатор выполняет эти команды, манипулируя памятью и стеком. Проект также предоставляет возможность логирования операций для анализа.

### Ассемблер (`assembler.py`)
Ассемблер считывает команды из текстового файла, преобразует их в бинарный формат и сохраняет в файл. Дополнительно создаётся лог-файл с информацией о каждой обработанной команде.

#### Поддерживаемые команды
- `LOAD_CONST` — Загрузка константы в стек.
- `READ_MEM` — Чтение значения из памяти.
- `WRITE_MEM` — Запись значения в память.
- `MIN` — Вычисление минимума между вершиной стека и значением в памяти.
#### Основные функции
- `assemble(input_file, output_bin_file, log_file)`
Функция преобразует текстовые команды в бинарный формат.

#### Аргументы:

- `input_file` — путь к текстовому файлу с командами.
- `output_bin_file` — путь для сохранения бинарного файла.
- `log_file` — путь для сохранения логов в формате CSV.
#### Пример использования:
```python
assemble('commands.txt', 'output.bin', 'log.csv')
```
#### Пример текстового файла команд (commands.txt):
```LOAD_CONST 25
READ_MEM 1
WRITE_MEM
MIN 100
```
#### Пример содержимого лог-файла (log.csv):
```csv
command,operand,binary
LOAD_CONST,25,0x03,0x00,0x19
READ_MEM,1,0x04,0x01
WRITE_MEM,,0x06
MIN,100,0x00,0x00,0x64
```
### Интерпретатор (`interpreter.py`)
Интерпретатор выполняет бинарные команды, манипулируя памятью и стеком. Он считывает команды из бинарного файла, выполняет их, записывает состояние памяти в CSV и логирует операции со стеком.

#### Основные команды
- `LOAD_CONST` — Помещает константу на стек.
- `READ_MEM` — Считывает значение из памяти в стек.
- `WRITE_MEM` — Записывает значение из стека в память.
- `MIN` — Вычисляет минимум между значением из памяти и вершиной стека.
#### Основные функции
- `interpret(input_bin_file, output_csv_file, memory_range, log_file)`
Функция интерпретирует бинарные команды и сохраняет результаты.

#### Аргументы:

- `input_bin_file` — путь к бинарному файлу с командами.
- `output_csv_file` — путь для сохранения состояния памяти.
- `memory_range` — диапазон адресов памяти (например, (0, 3)).
- `log_file` — путь для сохранения логов операций со стеком.
#### Пример использования:
```python
interpret('output.bin', 'result.csv', (0, 3), 'stack_operations_log.txt')
```
#### Пример содержимого бинарного файла (output.bin):
```bash
0x03 0x00 0x19  # LOAD_CONST 25
0x04 0x01       # READ_MEM 1
0x06            # WRITE_MEM
0x00 0x00 0x64  # MIN 100
```
#### Пример содержимого CSV-файла (result.csv):
```csv
address,value
0,25
1,10
2,15
3,30
```
#### Пример содержимого лог-файла (stack_operations_log.txt):
```makefile
LOAD_CONST: добавили 25 в стек. Стек: [25]
READ_MEM: считали 10 с адреса 1. Стек: [25, 10]
WRITE_MEM: записали 15 в память по адресу 2. Стек: [25]
MIN: сравнили 15 из памяти по адресу 2 со значением 25 из стека. Результат: 15.
```

## Как запустить
### Установка
- Убедитесь, что у вас установлен `Python 3.x`.
- Склонируйте или загрузите проект в вашу рабочую директорию.
### Запуск Ассемблера
- Подготовьте текстовый файл с командами, например `commands.txt`.
- Выполните команду:
```bash
python assembler.py
```
### Результат:
- Бинарный файл (`output.bin`).
- Лог-файл (`log.csv`).
## Запуск Интерпретатора
- Убедитесь, что у вас есть бинарный файл с командами (например, `output.bin`).
### Выполните команду:
```bash
python interpreter.py
```
### Результат:
- Состояние памяти в CSV (`result.csv`).
- Лог операций со стеком (`stack_operations_log.txt`).
#### Структура проекта
- `assembler.py` — Ассемблер.
- `interpreter.py` — Интерпретатор.
#### Пример файлов:
- `commands.txt` — текстовый файл с командами для Ассемблера.
- `output.bin` — бинарный файл команд, созданный Ассемблером.
- `result.csv` — состояние памяти, сохранённое Интерпретатором.
- `stack_operations_log.txt` — логи операций Интерпретатора.
