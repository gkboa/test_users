# подключение библиотек
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: 7658942562:AAG5l1DiyCQ1hL0HxUusDBQqZr-uh9t-zPc
TOKEN = '7658942562:AAG5l1DiyCQ1hL0HxUusDBQqZr-uh9t-zPc'
bot = TeleBot(TOKEN, parse_mode='html')
# библиотека для генерации тестовых ФИО
# указываем язык - русский
faker = Faker('ru_RU') 

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей. "\
        "Выбери сколько пользователей тебе нужно 👇🏻",
        reply_markup=main_menu_reply_markup
    )


# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # определяем количество тестовых пользователей
    # или отправляем ошибку
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
