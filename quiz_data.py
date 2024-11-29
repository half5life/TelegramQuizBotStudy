from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

# Структура квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какое ключевое слово используется для определения функции в Python?',
        'options': ['func', 'def', 'lambda', 'function'],
        'correct_option': 1
    },
    {
        'question': 'Что делает метод split() в Python?',
        'options': ['Объединяет строки', 'Удаляет символы', 'Разделяет строку', 'Заменяет символы'],
        'correct_option': 2
    },
    {
        'question': 'Какой результат выражения: len("Python")?',
        'options': ['5', '6', '7', '8'],
        'correct_option': 1
    },
    {
        'question': 'Какой символ используется для комментариев в Python?',
        'options': ['#', '//', '/* */', '--'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения логических значений?',
        'options': ['bool', 'int', 'str', 'float'],
        'correct_option': 0
    },
    {
        'question': 'Какое ключевое слово используется для создания класса в Python?',
        'options': ['class', 'def', 'object', 'new'],
        'correct_option': 0
    },
    {
        'question': 'Что такое Git?',
        'options': ['Система контроля версий', 'Редактор кода', 'База данных', 'Скриптовый язык'],
        'correct_option': 0
    },
    {
        'question': 'Что из перечисленного является структурой данных?',
        'options': ['Массив', 'Компилятор', 'Цикл', 'Функция'],
        'correct_option': 0
    }
]

def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        # Формируем callback_data в формате "статус:ответ"
        status = "right_answer" if option == right_answer else "wrong_answer"
        callback_data = f"{status}:{option}"

        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            callback_data=callback_data
        ))

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()