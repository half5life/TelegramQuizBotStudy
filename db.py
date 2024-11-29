import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                         user_id INTEGER PRIMARY KEY, 
                         question_index INTEGER,
                         correct_answers INTEGER DEFAULT 0
                         )''')
        # Создаем таблицу для хранения результатов квиза
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                last_score INTEGER
            )
        ''')
        # Сохраняем изменения
        await db.commit()

async def reset_quiz_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers)
            VALUES (?, 0, 0)
        ''', (user_id,))
        await db.commit()

async def set_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            UPDATE quiz_state
            SET question_index = ?
            WHERE user_id = ?
        ''', (index, user_id))
        await db.commit()

async def increment_correct_answers(user_id):
    # Увеличиваем количество правильных ответов на 1
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            UPDATE quiz_state
            SET correct_answers = correct_answers + 1
            WHERE user_id = ?
        ''', (user_id,))
        await db.commit()

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            
async def get_correct_answers(user_id):
    # Получаем количество правильных ответов для пользователя
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM quiz_state WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
            
async def save_quiz_result(user_id, score):
    # Сохраняем последний результат квиза пользователя
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_results (user_id, last_score)
            VALUES (?, ?)
        ''', (user_id, score))
        await db.commit()

async def get_quiz_result(user_id):
    # Получаем последний результат квиза пользователя
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT last_score FROM quiz_results WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return None