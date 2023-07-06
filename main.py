import os
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

bot = AsyncTeleBot(TOKEN, parse_mode='HTML')

def generate_markup(buttons, row):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*buttons, row_width=row) #* рспаковка список
    return markup

# def create_keyboard_markup(button_dict):
#     markup = InlineKeyboardMarkup()
#     for button_text, callback_data in button_dict.items():
#         button = InlineKeyboardButton(button_text, callback_data=callback_data)
#         markup.add(button)
#
#     return markup

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, 'привет...')
    buttons = ['пунктуация', 'орфография', 'упражнения']
    await bot.send_message(chat_id, 'выберите', reply_markup=generate_markup(buttons, 2))

@bot.message_handler(content_types=['text'])
async def punc(message):
    if message.text == 'пунктуация':
        buttons = ['запятая', 'тире']
        await bot.send_message(message.chat.id, 'выберите', reply_markup=generate_markup(buttons, 1))

    if message.text == 'запятая':
        await bot.send_message(message.chat.id, 'правило')
        buttons = ['вернуться']
        await bot.send_message(message.chat.id, 'вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'тире':
        await bot.send_message(message.chat.id, 'правило')
        buttons = ['вернуться']
        await bot.send_message(message.chat.id, 'вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    elif message.text == 'орфография':
        buttons = ['гласные', 'согласные']
        await bot.send_message(message.chat.id, 'выберите', reply_markup=generate_markup(buttons, 1))

    if message.text=='вернуться':
        buttons = ['пунктуация', 'орфография']
        await bot.send_message(message.chat.id, 'выберите', reply_markup=generate_markup(buttons, 2))


    # if message.text=='упражнения':
    #     chat_id = message.from_user.id
    #     button_dict={'запятая': 'first',
    #                  'тире': 'second',
    #                  'орфография': 'third'
    #                  }
    #     await bot.send_message(chat_id, 'выберите тему упражнений', reply_markup=create_keyboard_markup(button_dict))

        # markup = InlineKeyboardMarkup(row_width=1)
        # b1 = InlineKeyboardButton('запятая', callback_data='first')
        # b2 = InlineKeyboardButton('тире', callback_data='second')
        # b3 = InlineKeyboardButton('орфография', callback_data='third')
        # markup.add(b1, b2, b3)
        # await bot.send_message(chat_id, 'выберите тему упражнений', reply_markup=markup)

# @bot.callback_query_handler(func=lambda call:True)
# async def handle_callback(call):
#     call_id=call.message.chat.id
#     button_call=call.data
#     if button_call=='first':
#         await bot.send_message(call_id, 'упражнение 1')
#         # buttons = ['следующее упр']
#         # await bot.send_message(message.chat.id, 'выберите цифры правильных ответов', reply_markup=generate_markup(buttons, 1))


def get_word_definition(word):
    url = f"https://ru.wiktionary.org/wiki/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

        # Ищем определение слова
    definition = ""
    definition_element = soup.find("span", {"class": "mw-headline", "id": "Значение"})
    if definition_element:
        definition = definition_element.find_next("ol").text.strip()

        # Ищем правила орфографии
    spelling_rules = ""
    rules_element = soup.find("span", {"class": "mw-headline", "id": "Орфографические_правила"})
    if rules_element:
        spelling_rules = rules_element.find_next("ul").text.strip()

    return definition, spelling_rules

word = input("Введите слово: ")
definition, rules = get_word_definition(word)
if definition:
    print(f"Определение слова '{word}':")
    print(definition)
else:
    print(f"Определение слова '{word}' не найдено.")

if rules:
    print(f"Правила орфографии для слова '{word}':")
    print(rules)
else:
    print(f"Правила орфографии для слова '{word}' не найдены.")


import asyncio
asyncio.run(bot.polling())