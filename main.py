import telebot
from config import token
# Задание 7 - импортируй команду defaultdict
from collections import defaultdict
from logic import quiz_questions

user_responses = {} 
# Задание 8 - создай словарь points для сохранения количества очков пользователя
points = defaultdict(int)
bot = telebot.TeleBot(token)

def send_question(chat_id):
    if chat_id not in user_responses or user_responses[chat_id] >= len(quiz_questions):
        bot.send_message(chat_id, "Please start the quiz with the command /start.")
        return
    
    # Получаем текущий вопрос
    question = quiz_questions[user_responses[chat_id]]

    # Отправка изображения, если есть
    if question.image_url:
        bot.send_photo(chat_id, question.image_url)
    bot.send_message(chat_id, question.text, reply_markup=question.gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Удаляем inline-клавиатуру
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)

    # Проверка, что пользователь начал квиз
    if chat_id not in user_responses:
        bot.answer_callback_query(call.id, "Please start the quiz with the /start command.")
        return
    
    if call.data == "correct":
        bot.answer_callback_query(call.id, "Answer is correct")
        # Задание 9 - добавь очки пользователю за правильный ответ
        points[chat_id] += 1
    elif call.data == "wrong":
        bot.answer_callback_query(call.id,  "Answer is wrong")
      
    # Задание 5 - реализуй счетчик вопросов
    user_responses[chat_id] += 1
    # Задание 6 - отправь пользователю сообщение с количеством его набранных очков, если он ответил на все вопросы, а иначе отправь следующий вопрос
    if chat_id not in user_responses or user_responses[chat_id]>=len(quiz_questions):
        bot.send_message(chat_id, f"The end. You scored {points[chat_id]} points.")
        # Очистка данных для нового запуска
        del user_responses[chat_id]
        del points[chat_id]
        bot.send_message(chat_id, "To start again, type /start")
        return
    else:
        send_question(chat_id)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    # Обнуляем состояние пользователя
    user_responses[chat_id] = 0
    points[chat_id] = 0

    # Приветствие и первый вопрос
    bot.send_message(chat_id, "Привет! 🐾 Начинаем квиз!")
    send_question(chat_id)

bot.infinity_polling()
