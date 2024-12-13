import re

# Кэш для хранения результатов гороскопов
horoscope_cache = {}

def parse_date_message(message):
    pattern = r'^(\d{2})\s+(\d{2})\s+(\d{4})$|^(\d{2})\.(\d{2})\.(\d{4})$'
    match = re.match(pattern, message)
    if not match:
        raise ValueError("Неправильный формат сообщения. Пожалуйста, используйте формат: ДД ММ ГГГГ или ДД.ММ.ГГГГ.")

    if match.group(1):
        date_str = f"{match.group(1)} {match.group(2)} {match.group(3)}"
    else:
        date_str = f"{match.group(4)}.{match.group(5)}.{match.group(6)}"
    return date_str

def parse_time_message(message):
    pattern = r'^(\d{2}:\d{2})$'
    match = re.match(pattern, message)
    if not match:
        raise ValueError("Неправильный формат сообщения. Пожалуйста, используйте формат: ЧЧ:ММ.")

    time_str = match.group(1)
    return time_str
