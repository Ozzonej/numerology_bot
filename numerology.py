def calculate_name_value(name):
    # Преобразование имени в числовое значение
    letter_values_ru = {
        'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9,
        'И': 1, 'Й': 2, 'К': 3, 'Л': 4, 'М': 5, 'Н': 6, 'О': 7, 'П': 8, 'Р': 9,
        'С': 1, 'Т': 2, 'У': 3, 'Ф': 4, 'Х': 5, 'Ц': 6, 'Ч': 7, 'Ш': 8, 'Щ': 9,
        'Ъ': 1, 'Ы': 2, 'Ь': 3, 'Э': 4, 'Ю': 5, 'Я': 6
    }

    name_value = 0
    for char in name:
        if char.upper() in letter_values_ru:
            name_value += letter_values_ru[char.upper()]
        else:
            raise ValueError("Имя должно содержать только русские буквы.")

    return name_value

def calculate_birthdate_value(birthdate):
    # Преобразование даты рождения в числовое значение
    birthdate_value = sum(int(char) for char in birthdate if char.isdigit())
    return birthdate_value

def calculate_specific_date_value(date):
    # Преобразование конкретной даты в числовое значение
    date_value = sum(int(char) for char in date if char.isdigit())
    return date_value

def reduce_to_single_digit(value):
    # Приведение к однозначному числу
    while value > 9:
        value = sum(int(digit) for digit in str(value))
    return value

def interpret_tarot(value):
    from tarot_interpretations import TAROT_INTERPRETATIONS
    return TAROT_INTERPRETATIONS.get(value, "Неизвестное значение.")

def calculate_life_path_number(birthdate):
    """
    Calculate the life path number based on the birthdate.
    :param birthdate: Birthdate in the format 'DD MM YYYY HH:MM'
    :return: Life path number
    """
    # Remove non-digit characters and sum all digits
    total = sum(int(char) for char in birthdate if char.isdigit())

    # Reduce the number to a single digit
    while total >= 10:
        total = sum(int(digit) for digit in str(total))

    return total

def calculate_expression_number(full_name):
    """
    Calculate the expression number based on the full name.
    :param full_name: Full name as a string
    :return: Expression number
    """
    letter_values = {
        'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9,
        'И': 1, 'Й': 2, 'К': 3, 'Л': 4, 'М': 5, 'Н': 6, 'О': 7, 'П': 8, 'Р': 9,
        'С': 1, 'Т': 2, 'У': 3, 'Ф': 4, 'Х': 5, 'Ц': 6, 'Ч': 7, 'Ш': 8, 'Щ': 9,
        'Ъ': 1, 'Ы': 2, 'Ь': 3, 'Э': 4, 'Ю': 5, 'Я': 6
    }

    # Calculate the sum of the numeric values of all letters in the full name
    total = sum(letter_values[char.upper()] for char in full_name if char.upper() in letter_values)

    # Reduce the number to a single digit
    while total >= 10:
        total = sum(int(digit) for digit in str(total))

    return total

def calculate_datetime_value(datetime_str):
    """
    Calculate the numerological value based on the datetime string.
    :param datetime_str: Datetime string in the format 'DD MM YYYY HH:MM'
    :return: Numerological value
    """
    # Remove non-digit characters and sum all digits
    total = sum(int(char) for char in datetime_str if char.isdigit())

    # Reduce the number to a single digit
    while total >= 10:
        total = sum(int(digit) for digit in str(total))

    return total
