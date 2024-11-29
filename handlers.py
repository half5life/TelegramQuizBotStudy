from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from db import reset_quiz_state, set_quiz_index, get_quiz_index, increment_correct_answers, save_quiz_result, get_quiz_result, get_correct_answers
from quiz_data import quiz_data, generate_options_keyboard

async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    await reset_quiz_state(user_id)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def handle_answer(callback: types.CallbackQuery):
    # Извлекаем статус и выбранный вариант из callback_data
    try:
        status, selected_option = callback.data.split(':', 1)
    except ValueError:
        await callback.answer("Некорректные данные ответа.", show_alert=True)
        return

    # Убираем кнопки из сообщения
    await callback.message.edit_reply_markup(reply_markup=None)

    # Получение текущего вопроса для данного пользователя
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)

    if status == "right_answer":
        response_text = f"Вы выбрали: {selected_option}\nВерно!"
        # Увеличиваем количество правильных ответов
        await increment_correct_answers(user_id)
    else:
        # Получаем правильный ответ для отображения
        correct_option_index = quiz_data[current_question_index]['correct_option']
        correct_option = quiz_data[current_question_index]['options'][correct_option_index]
        response_text = f"Вы выбрали: {selected_option}\nНеправильно. Правильный ответ: {correct_option}"

    # Отправляем сообщение с результатом
    await callback.message.answer(response_text)

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await set_quiz_index(user_id, current_question_index)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Квиз завершен
        # Получение количества правильных ответов
        correct_answers = await get_correct_answers(user_id)
         # Сохранение результата квиза
        await save_quiz_result(user_id, correct_answers)
        # Уведомление об окончании квиза
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат: {correct_answers} из {len(quiz_data)}")
        # Сброс состояния квиза
        await reset_quiz_state(user_id)

async def cmd_stats(message: types.Message):
    # Получаем id пользователя
    user_id = message.from_user.id
    # Получаем последний результат квиза
    last_score = await get_quiz_result(user_id)
    if last_score is not None:
        await message.answer(f"Ваш последний результат: {last_score} из {len(quiz_data)}")
    else:
        await message.answer("Вы еще не проходили квиз. Нажмите 'Начать игру', чтобы начать.")

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_stats, Command("stats"))
    dp.message.register(cmd_stats, F.text == "Статистика")
    dp.callback_query.register(handle_answer, F.data.contains("right_answer"))
    dp.callback_query.register(handle_answer, F.data.contains("wrong_answer"))