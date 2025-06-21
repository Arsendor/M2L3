# Задание 2 - Импортируй нужные классы
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Question:

    def __init__(self, text, answer_id, *options, image_url=None):
        self.__text = text
        self.__answer_id = answer_id
        self.options = options
        self.image_url = image_url
    # Задание 1 - Создай геттер для получения текста вопроса
    @property
    def text(self):
        return self.__text
    
    def gen_markup(self):
        # Задание 3 - Создай метод для генерации Inline клавиатуры
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)

        for i, option in enumerate(self.options):
            if i == self.__answer_id:
                markup.add(InlineKeyboardButton(option, callback_data='correct'))
            else:
                markup.add(InlineKeyboardButton(option, callback_data='wrong'))
        return markup


class MultiAnswerQuestion(Question):
    def __init__(self, text, correct_ids, *options, image_url=None):
        super().__init__(text, None, *options, image_url=image_url)
        self.correct_ids = set(correct_ids)

    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        for i, option in enumerate(self.options):
            markup.add(InlineKeyboardButton(option, callback_data=f'multi_{i}'))
        markup.add(InlineKeyboardButton("Готово", callback_data="multi_done"))
        return markup

    def check_answer(self, selected_ids):
        return set(selected_ids) == self.correct_ids


    def check_answer(self, callback_data):
        # callback_data вида 'multi_0', 'multi_2' и т.п.
        if not callback_data.startswith('multi_'):
            return False
        idx = int(callback_data.split('_')[1])
        return idx in self.correct_ids
    
# Задание 4 - заполни список своими вопросами
quiz_questions = [
    Question("Какой цвет у котиков?", 0, "Черный", "Белый", "Розовый", image_url="https://i.imgur.com/4AiXzf8.jpg"),
    Question("Что котики делают, когда никто их не видит?", 1, "Спят", "Пишут мемы", image_url="https://i.imgur.com/4AiXzf8.jpg"),
    MultiAnswerQuestion("Выберите все правильные варианты:", [0, 2], "Правильно 1", "Неправильно", "Правильно 2"),
    Question("Как котики выражают свою любовь?", 0, "Громким мурлыканием", "Отправляют фото на Instagram", "Гавкают"),
    Question("Какие книги котики любят читать?", 3, "Обретение вашего внутреннего урр-мирения", "Тайм-менеджмент или как выделить 18 часов в день для сна", "101 способ уснуть на 5 минут раньше, чем хозяин", "Пособие по управлению людьми"),
    Question("Какое из этих животных НЕ является кошачьим?", 2, "Лев", "Тигр", "Волк", "Ягуар"),
    MultiAnswerQuestion("Какие цвета присутствуют на флаге Латвии?", [0, 1], "Красный", "Белый", "Синий", "Зеленый"),
    Question("Что изображено на картинке?", 0, "Котёнок", "Собака", "Птица", image_url="https://i.imgur.com/w3duR07.png"),
    MultiAnswerQuestion("Выберите фрукты из списка:", [1, 3], "Картофель", "Яблоко", "Морковь", "Банан"),
    Question("Какой язык программирования используется для создания ботов в Telegram?", 0, "Python", "JavaScript", "C++", "Java"),
    Question("Какой символ используется для обозначения комментариев в Python?", 0, "#", "//", "/*", "--"),
    Question("Какой метод используется для добавления элемента в список в Python?", 0, "append()", "add()", "insert()", "push()"),
    Question("Какой метод используется для удаления элемента из списка в Python?", 0, "remove()", "delete()", "pop()", "discard()"),
]
