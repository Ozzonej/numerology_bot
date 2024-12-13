from datetime import datetime, timedelta
import ephem

# Определение новолуния
def get_next_new_moon(date):
    moon = ephem.Moon()
    moon.compute(date)
    next_new_moon = ephem.next_new_moon(date)
    return next_new_moon.datetime()

# Расчет фаз Луны
def get_moon_phase(date):
    moon = ephem.Moon()
    moon.compute(date)
    phase = moon.phase
    if phase < 7.4:
        return "Новолуние"
    elif phase < 14.8:
        return "Первая четверть"
    elif phase < 22.2:
        return "Полнолуние"
    else:
        return "Последняя четверть"

# Расчет лунных дней
def get_lunar_day(date):
    next_new_moon = get_next_new_moon(date)
    previous_new_moon = ephem.previous_new_moon(date).datetime()
    days_since_new_moon = (date - previous_new_moon).days
    return (days_since_new_moon % 29) + 1

# Определение лунного знака
def get_lunar_sign(lunar_day):
    signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    if lunar_day < 1 or lunar_day > 29:
        raise ValueError("Лунный день должен быть в диапазоне от 1 до 29.")
    index = (lunar_day - 1) // 2
    if index < 0 or index >= len(signs):
        raise ValueError(f"Индекс {index} выходит за пределы диапазона списка знаков.")
    return signs[index]

# Создание лунного календаря
def generate_lunar_calendar(start_date, days):
    calendar = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        phase = get_moon_phase(current_date)
        lunar_day = get_lunar_day(current_date)
        try:
            sign = get_lunar_sign(lunar_day)
        except ValueError as e:
            sign = str(e)
        calendar.append({
            "date": current_date.strftime('%Y-%m-%d'),
            "phase": phase,
            "lunar_day": lunar_day,
            "sign": sign
        })
    return calendar
