import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import NetworkError
import numerology
import astrology
from datetime import datetime
import re
from utils import parse_date_message, parse_time_message, horoscope_cache

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text('Привет! Отправьте /menu, чтобы выбрать нужную функцию.')
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        await asyncio.sleep(5)  # Подождать 5 секунд перед повторной попыткой
        await start(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Расчет по имени и дате")],
        [KeyboardButton("Расчет по дате и времени")],
        [KeyboardButton("Ваш гороскоп на сегодня")],
        [KeyboardButton("Перезапуск")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Выберите нужную функцию:', reply_markup=reply_markup)

async def horoscope_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Овен"), KeyboardButton("Телец"), KeyboardButton("Близнецы")],
        [KeyboardButton("Рак"), KeyboardButton("Лев"), KeyboardButton("Дева")],
        [KeyboardButton("Весы"), KeyboardButton("Скорпион"), KeyboardButton("Стрелец")],
        [KeyboardButton("Козерог"), KeyboardButton("Водолей"), KeyboardButton("Рыбы")],
        [KeyboardButton("Назад")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Выберите ваш знак зодиака:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    if message == "Расчет по имени и дате":
        context.user_data['mode'] = 'name_date'
        context.user_data['step'] = 1
        await update.message.reply_text('Отправьте ваше имя.')
    elif message == "Расчет по дате и времени":
        context.user_data['mode'] = 'date_time'
        context.user_data['step'] = 1
        await update.message.reply_text('Отправьте дату в формате: ДД ММ ГГГГ или ДД.ММ.ГГГГ.')
    elif message == "Ваш гороскоп на сегодня":
        await horoscope_menu(update, context)
    elif message == "Перезапуск":
        context.user_data.clear()
        await menu(update, context)
    elif message in ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]:
        context.user_data['zodiac_sign'] = message
        await process_horoscope_message(update, context)
    elif message == "Назад":
        await menu(update, context)
    else:
        mode = context.user_data.get('mode')
        step = context.user_data.get('step', 1)
        if mode == 'name_date':
            await handle_name_date_message(update, context, step)
        elif mode == 'date_time':
            await handle_date_time_message(update, context, step)

async def handle_name_date_message(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int) -> None:
    message = update.message.text
    if step == 1:
        first_name = message.split()[0]
        context.user_data['name'] = first_name
        context.user_data['step'] = 2
        await update.message.reply_text('Отправьте дату рождения в формате: ДД ММ ГГГГ или ДД.ММ.ГГГГ.')
    elif step == 2:
        try:
            date = parse_date_message(message)
            context.user_data['date'] = date
            context.user_data['step'] = 3
            await update.message.reply_text('Отправьте время в формате: ЧЧ:ММ.')
        except ValueError as e:
            await update.message.reply_text(str(e))
    elif step == 3:
        try:
            time = parse_time_message(message)
            context.user_data['time'] = time
            name = context.user_data['name']
            datetime_str = f"{context.user_data['date']} {context.user_data['time']}"
            await process_name_date_message(update, context, name, datetime_str)
        except ValueError as e:
            await update.message.reply_text(str(e))

async def handle_date_time_message(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int) -> None:
    message = update.message.text
    if step == 1:
        try:
            date = parse_date_message(message)
            context.user_data['date'] = date
            context.user_data['step'] = 2
            await update.message.reply_text('Отправьте время в формате: ЧЧ:ММ.')
        except ValueError as e:
            await update.message.reply_text(str(e))
    elif step == 2:
        try:
            time = parse_time_message(message)
            context.user_data['time'] = time
            datetime_str = f"{context.user_data['date']} {context.user_data['time']}"
            await process_date_time_message(update, context, datetime_str)
        except ValueError as e:
            await update.message.reply_text(str(e))

async def process_name_date_message(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, datetime_str: str) -> None:
    name_value = numerology.calculate_name_value(name)
    datetime_value = numerology.calculate_datetime_value(datetime_str)
    life_path_number = numerology.calculate_life_path_number(datetime_str)
    expression_number = numerology.calculate_expression_number(name)

    name_value = numerology.reduce_to_single_digit(name_value)
    datetime_value = numerology.reduce_to_single_digit(datetime_value)

    name_interpretation = numerology.interpret_tarot(name_value)
    datetime_interpretation = numerology.interpret_tarot(datetime_value)
    life_path_interpretation = numerology.interpret_tarot(life_path_number)
    expression_interpretation = numerology.interpret_tarot(expression_number)

    image_path = 'loading.jpg'
    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(photo=InputFile(photo))

    response = (f"Значение {datetime_value}-го аркана:\n{datetime_interpretation}\n\n"
                f"Число жизненного пути: {life_path_number}. Интерпретация (Таро): {life_path_interpretation}\n"
                f"Число выражения: {expression_number}. Интерпретация (Таро): {expression_interpretation}")

    await update.message.reply_text("Смотрю во вселенную, чтобы узнать магию цифр вашего имени...")
    await asyncio.sleep(3)
    await update.message.reply_text("Считаю магию цифр вашей даты...")
    await asyncio.sleep(5)
    await update.message.reply_text("Теперь у меня есть все нужные цифры, начинаю расчет вашей карты...")
    await asyncio.sleep(5)
    await update.message.reply_text(response)

    context.user_data.clear()
    await menu(update, context)

async def process_date_time_message(update: Update, context: ContextTypes.DEFAULT_TYPE, datetime_str: str) -> None:
    datetime_value = numerology.calculate_datetime_value(datetime_str)
    datetime_value = numerology.reduce_to_single_digit(datetime_value)
    datetime_interpretation = numerology.interpret_tarot(datetime_value)

    image_path = 'loading.jpg'
    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(photo=InputFile(photo))

    response = f"Значение {datetime_value}-го аркана:\n{datetime_interpretation}"

    await update.message.reply_text("Смотрю во вселенную, чтобы узнать магию цифр вашего времени...")
    await asyncio.sleep(3)
    await update.message.reply_text("Считаю магию цифр вашего времени...")
    await asyncio.sleep(5)
    await update.message.reply_text("Теперь у меня есть все нужные цифры, начинаю расчет вашей карты...")
    await asyncio.sleep(5)
    await update.message.reply_text(response)

    context.user_data.clear()
    await menu(update, context)

async def process_horoscope_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    zodiac_sign = context.user_data['zodiac_sign']
    current_date = datetime.now().strftime('%d %m %Y')
    cache_key = f"{zodiac_sign}_{current_date}"

    if cache_key in horoscope_cache:
        horoscope = horoscope_cache[cache_key]
    else:
        horoscope = astrology.generate_horoscope(zodiac_sign, current_date)
        horoscope_cache[cache_key] = horoscope

    response = f"Ваш гороскоп на {current_date}:\n{horoscope}"

    await update.message.reply_text("Рассчитываю по звездам ваш гороскоп на сегодня...")
    await asyncio.sleep(5)
    await update.message.reply_text(response)

    context.user_data.clear()
    await menu(update, context)

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
