import json
from math import ceil
from encryptors.simple import Simple
from encryptors.vertical import Vertical
from encryptors.rail_fence import RailFence


ENCRYPTORS = {'Simple': Simple,
              'Vertical': Vertical,
              'RailFence': RailFence
              }


def print_config(filename: str) -> None:
    with open('configs/' + filename + '.json', 'r') as f:
        config_list = json.load(f)
    for config in config_list:
        print(f'Название: {config["name"]}\n'
              f'Ключ: {config["key"]}\n'
              f'Тип данных: {config["dtype"] if config["dtype"] else "Single"}\n'
              f'Нули на последнем блоке: {config["with_null"]}\n')


def save_to(data, dtype):
    if dtype == 'byte':
        filename = input('Введите название файла для записи\n')
        with open(filename, 'wb') as f:
            if isinstance(data[0], str):
                f.write(bytes([ord(x) for x in data]))
            else:
                f.write(bytes(data))
        return
    save_choice = input('Куда вывести сообщение?\n'
                        '1 - В консоль\n'
                        '2 - В файл\n')
    if save_choice == '1':
        print(data)
    else:
        filename = input('Введите название файла для записи\n')
        with open(filename, 'w') as f:
            f.write(data)


def save_config(config_list: list):
    user_choice = input('Не хотите ли записать этот конфиг?\n'
                        '1 - Да\n'
                        '2 - Нет\n') == '1'
    if not user_choice:
        return
    filename = input('Введите название файла для записи\n')
    with open('configs/' + filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(config_list, f, indent=4, ensure_ascii=False)


def get_config(filename: str):
    with open('configs/' + filename + '.json', 'r', encoding='utf-8') as f:
        config_list = json.load(f)
        for config in config_list:
            config['name'] = ENCRYPTORS[config['name']]
    return config_list


def choose_dtype():
    dtype = input('Тип данных:\n'
                '1 - Односимвольный\n'
                '2 - Группа символов\n'
                '3 - Байт\n')
    if dtype == '1':
        return None
    elif dtype == '2':
        group_amount = int(input('Количество символов в группе\n'))
        return ('group', group_amount)
    elif dtype == '3':
        return 'byte'


def choose_input(dtype):
    if dtype == 'byte':
        filename = input('Введите название файла\n')
        with open(filename, 'rb') as f:
            return f.read()
    choose = input('Выберите источник\n'
                '1 - Консоль\n'
                '2 - Файл\n') == '1'
    if choose:
        return input('Введите сообщение\n')
    filename = input('Введите название файла\n')
    with open(filename, 'r') as f:
            return f.read()


def null_ending():
    return input('Что делать с последним блоком?\n'
        '1 - Добавить нули\n'
        '2 - Не добавлять нули\n') == '1'


def crypt_algorithm_choice(choice: str):
    if choice in '1235':
        if choice != '5':
            if choice in '12':
                key_choice = input('Сгенерировать случайный ключ?\n'
                                   '1 - Да\n'
                                   '2 - Нет\n') == '1'
                if key_choice:
                    size = int(input('Введите размер блока\n'))
                    key = Simple.generate_key(size)
                    print(f'Ключ: {key}\n')
                else:
                    key = input('Введите ключ ("_" как разделитель)\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype)
                if choice == '2':
                    dimension = ceil(len(data) / len(key.split('_')))
                    key = str(dimension) + 'x' + str(len(key.split('_'))) + ' ' + key
                if choice == '1':
                    s = Simple(data, key, with_null=with_null, dtype=dtype)
                else:
                    s = Vertical(data, key, with_null=with_null, dtype=dtype)
            elif choice == '3':
                key = input('Введите размерность матрицы (MxN):\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype)
                s = RailFence(data, key, with_null=with_null, dtype=dtype)
            config = {'name': str(s),
                    'key': key,
                    'dtype': dtype,
                    'with_null': with_null
                    }
            save_config([config])
            crypt_data = s.encryption()
            save_to(crypt_data, dtype)
        else:
            filename = input('Введите название конфига\n')
            config_list = get_config(filename)
            first = True
            for config in config_list:
                data = choose_input(config['dtype']) if first else data
                first = False
                s = config['name'](data, **config)
                data = s.encryption()
            save_to(data, config['dtype'])
    else:
        event = input('Выберите следующий алгоритм:\n'
                    '1 - Простая перестановка\n'
                    '2 - Вертикальная перестановка\n'
                    '3 - Rail Fence\n'
                    '0 - Закончить\n')
        config_list = []
        while event != '0':
            if event in '12':
                key_choice = input('Сгенерировать случайный ключ?\n'
                                   '1 - Да\n'
                                   '2 - Нет\n') == '1'
                if key_choice:
                    size = int(input('Введите размер блока\n'))
                    key = Simple.generate_key(size)
                    print(f'Ключ: {key}\n')
                else:
                    key = input('Введите ключ ("_" как разделитель)\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype) if not config_list else data
                if event == '2':
                    dimension = ceil(len(data) / len(key.split('_')))
                    key = str(dimension) + 'x' + str(len(key.split('_'))) + ' ' + key
                if event == '1':
                    s = Simple(data, key, with_null=with_null, dtype=dtype)
                else:
                    s = Vertical(data, key, with_null=with_null, dtype=dtype)
            elif event == '3':
                key = input('Введите размерность матрицы (MxN):\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype) if not config_list else data
                s = RailFence(data, key, with_null=with_null, dtype=dtype)
            config = {'name': str(s),
                    'key': key,
                    'dtype': dtype,
                    'with_null': with_null
                    }
            config_list.append(config)
            data = s.encryption()
            event = input('Выберите следующий алгоритм:\n'
                        '1 - Простая перестановка\n'
                        '2 - Вертикальная перестановка\n'
                        '3 - Rail Fence\n'
                        '0 - Закончить\n')
        save_config(config_list)
        save_to(data, dtype)


def decrypt_algorithm_choice(choice: str):
    if choice in '1235':
        if choice != '5':
            if choice in '12':
                key = input('Введите ключ ("_" как разделитель)\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype)
                if choice == '2':
                    dimension = ceil(len(data) / len(key.split('_')))
                    key = str(dimension) + 'x' + str(len(key.split('_'))) + ' ' + key
                if choice == '1':
                    s = Simple(data, key, with_null=with_null, dtype=dtype)
                else:
                    s = Vertical(data, key, with_null=with_null, dtype=dtype)
            elif choice == '3':
                key = input('Введите размерность матрицы (MxN):\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype)
                s = RailFence(data, key, with_null=with_null, dtype=dtype)
            config = {'name': str(s),
                    'key': key,
                    'dtype': dtype,
                    'with_null': with_null
                    }
            save_config([config])
            decrypt_data = s.decryption()
            save_to(decrypt_data, dtype)
        else:
            filename = input('Введите название конфига\n')
            config_list = get_config(filename)[::-1]
            first = True
            for config in config_list:
                data = choose_input(config['dtype']) if first else data
                first = False
                s = config['name'](data, **config)
                if config['dtype'] == 'byte':
                    data = [chr(x) for x in s.decryption()]
                else:
                    data = s.decryption()
            save_to(data, config['dtype'])
    else:
        event = input('Выберите следующий алгоритм:\n'
                    '1 - Простая перестановка\n'
                    '2 - Вертикальная перестановка\n'
                    '3 - Rail Fence\n'
                    '0 - Закончить\n')
        config_list = []
        while event != '0':
            if event in '12':
                key = input('Введите ключ ("_" как разделитель)\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype) if not config_list else data
                if event == '2':
                    dimension = ceil(len(data) / len(key.split('_')))
                    key = str(dimension) + 'x' + str(len(key.split('_'))) + ' ' + key
                if event == '1':
                    s = Simple(data, key, with_null=with_null, dtype=dtype)
                else:
                    s = Vertical(data, key, with_null=with_null, dtype=dtype)
            elif event == '3':
                key = input('Введите размерность матрицы (MxN):\n')
                dtype = choose_dtype()
                with_null = null_ending()
                data = choose_input(dtype) if not config_list else data
                s = RailFence(data, key, with_null=with_null, dtype=dtype)
            config = {'name': str(s),
                    'key': key,
                    'dtype': dtype,
                    'with_null': with_null
                    }
            config_list.append(config)
            data = s.decryption()
            event = input('Выберите следующий алгоритм:\n'
                        '1 - Простая перестановка\n'
                        '2 - Вертикальная перестановка\n'
                        '3 - Rail Fence\n'
                        '0 - Закончить\n')
        save_config(config_list)
        save_to(data, dtype)

if __name__ == '__main__':
    main_menu = input(
                    '1 - Зашифровать\n'
                    '2 - Расшифровать\n'
                    '3 - Посмотреть конфиг\n')
    if main_menu == '1' or main_menu == '2':
        algorithm = input(
                    'Выберите алгоритм\n'
                    '1 - Простая перестановка\n'
                    '2 - Вертикальная перестановка\n'
                    '3 - Rail Fence\n'
                    '4 - Множественная перестановка\n'
                    '5 - Свой конфиг\n')
        if main_menu == '1':
            crypt_algorithm_choice(algorithm)
        else:
            decrypt_algorithm_choice(algorithm)
    elif main_menu == '3':
        filename = input('Введите название файла\n')
        print_config(filename)
