import telebot
import random
from telebot import types

TOKEN = '8065939344:AAEiASLyP8sbzfAzpj6jNzEA0Szm37f998A'
bot = telebot.TeleBot(TOKEN)
user_data = {}

moods = {
    'happy': {
        'state': '😊 Радостный!',
        'phrases': ['Отлично!', 'Ура!', 'Супер!'] 
    },
    'neutral': {
        'state': '😐 Нейтральный',
        'phrases': ['Нормально', 'Все как обычно', 'Ничего нового']
    },
    'sad': {
        'state': '😥 Грустный',
        'phrases': ['Не очень', 'Мне грусно', 'Хочется спать']
    } 
}
current_mod = 'neutral'

WEATHER = {
    'москва': '+20С, солнечно 🌤',
    'сочи': '+28С, жара 🔥',
    'спб': '+18С, дождь 🌧',
    'казань': '+22С, облачно ☁'
}

facts = [
    'Коты спять 70% своей жизни 😴'
    'Python назван в честь Монти Пайтона 👾'
    'Сердце кита бьется 9 раз в минуту 🐳'
    'В мире больше игр чем людей 👀'
]

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bin1 = types.KeyboardButton('Узнать настроение')
    bin2 = types.KeyboardButton('Изменить настроение')
    markup.add(bin1, bin2)
    bot.reply_to(message, 'Доступные команды:\n'
                          '/start - начать общение\n'
                          '/game - игра\n'
                          '/weather - погода\n'
                          '/fact - случайный факт\n')
    
    bot.send_message(
        message.chat.id,
        'Привет! Я бот с настроением.\n'
        'Можешь узнать мое настроение или изменить его!',
        reply_markup=markup
    )
@bot.message_handler(func=lambda m: m.text == 'Узнать настроение')
def change_mood(message):
    mood = moods[current_mod]
    bot.send_message(message.chat.id,f'Мое настроение: {mood['state']}\n'
                     f'Что я думаю: {random.choice(mood['phrases'])}')
    
@bot.message_handler(func=lambda m: m.text == 'Изменить настроение')
def change_mood(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_happy = types.KeyboardButton('Сделать радостным')
    btn_neutral = types.KeyboardButton('Сделать нейтральным')
    btn_sad = types.KeyboardButton('Сделать грустным')
    markup.add(btn_happy, btn_neutral, btn_sad)

    bot.send_message(
        message.chat.id,
        'Какое настроение мне устрановить?',
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in [
    'Сделать радостным', 
    'Сделать нейтральным',
    'Сделать грустным'
])
def set_mood(message):
    global current_mood
    
    if message.text == 'Сделать радостным':
        current_mood = "happy"
    elif message.text == 'Сделать нейтральным':
        current_mood = "neutral"
    else:
        current_mood = "sad"
    
    mood = moods[current_mood]
    bot.send_message(
        message.chat.id,
        f"Мое новое настроение: {mood['state']}!\n"
        f"{random.choice(mood['phrases'])}",
           reply_markup=types.ReplyKeyboardRemove())    

@bot.message_handler(commands=['fact'])
def fact(message):
    fact = f'Бот: Знаешь ли ты? {random.choice(facts)}'
    bot.reply_to(message, fact)

@bot.message_handler(commands=['weather'])
def weather(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for city in WEATHER.keys():
        markup.add(city)
    msg = bot.send_message(message.chat.id, 'Выбирете город:', reply_markup=markup)
    bot.register_next_step_handler(msg, send_weather)
def send_weather(message):
    city = message.text.lower()
    if city in WEATHER:
        bot.send_message(message.chat.id, WEATHER[city])
    else:
        bot.send_message(message.chat.id, 'Город не найден. Попробуйте /weather')

@bot.message_handler(commands=['game'])
def game(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {'score': 0, 'bot_score': 0}
    user = users[chat_id]
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    bin1 = telebot.types.KeyboardButton('камень')
    bin2 = telebot.types.KeyboardButton('ножницы')
    bin3 = telebot.types.KeyboardButton('бумага')
    markup.add(bin1, bin2, bin3)

    bot.send_message(chat_id, 'Выбирай!(камень, ножницы, бумага)', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text.lower() in ['камень', 'ножницы', 'бумага'])
def handle_game_choice(message):
    chat_id = message.chat.id
    user = users[chat_id]
    player_choice = message.text.lower()
    choices = ['камень', 'ножницы', 'бумага']
    bot_choice = random.choice(choices)

    if player_choice == bot_choice:
        result = 'Ничья!'
    elif (player_choice == "камень" and bot_choice == "ножницы") or \
         (player_choice == "ножницы" and bot_choice == "бумага") or \
         (player_choice == "бумага" and bot_choice == "камень"):
        result = "Ты победил! 🏆"
        user['score'] += 1
    else:
        result = "Я выиграл! 💻"
        user['bot_score'] += 1

    bot.send_message(chat_id,
        f'Я выбрал: {bot_choice}\n{result}\n'
        f'Счет: Ты {user['score']} : Я {user['bot_score']}',
        reply_markup=telebot.types.ReplyKeyboardRemove())

bot.polling()