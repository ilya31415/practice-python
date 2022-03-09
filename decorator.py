import random
import time


def decorator(path_logs):
    def _decorator(function):
        def new_funcrion(*args):
            data_time = time.ctime()
            result = function(*args)
            arguments = args
            with open(path_logs, "a", encoding="UTF8") as f:
                f.write('\n'f'Дата и время вызова функции: {data_time}''\n')
                f.write(f'Имя функции: "{function.__name__}"''\n')
                f.write(f'Аргументы, с которыми вызвалась функция: {arguments}''\n')
                f.write(f'Возвращаемое значение: {result}''\n')
            return result

        return new_funcrion

    return _decorator


@decorator(path_logs=r'logs.txt')
def generator_password(len_passwprd: int = 8, number_items: int = 1):
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    result = []
    for items in range(number_items):
        password = [random.choice(chars) for pas in range(len_passwprd)]
        result.append("".join(password))
    return "  ".join(result)


print(generator_password(8, 4))
