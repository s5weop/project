import os
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

bot = AsyncTeleBot(TOKEN, parse_mode='HTML')

def get_word_definition(word):
    url = f"https://ru.wiktionary.org/wiki/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    definition = ""
    definition_element = soup.find("span", {"class": "mw-headline", "id": "Значение"})
    if definition_element:
        definition = definition_element.find_next("ol").text.strip()

    spelling_rules = ""
    rules_element = soup.find("span", {"class": "mw-headline", "id": "Этимология"})
    if rules_element:
        spelling_rules = rules_element.find_next("ul").text.strip()

    return definition, spelling_rules

def generate_markup(buttons, row):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*buttons, row_width=row) #* рспаковка список
    return markup

def create_keyboard_markup(button_dict):
    markup = InlineKeyboardMarkup()
    for button_text, callback_data in button_dict.items():
        button = InlineKeyboardButton(button_text, callback_data=callback_data)
        markup.add(button)

    return markup

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, 'Привет, данный бот поможет тебе:\n— узнать (или вспомнить) правила русского языка;\n— найти определение слова: для этого напиши в чат слово, у которого необходимо узнать значение.')
    buttons = ['Пунктуация', 'Орфография']
    await bot.send_message(chat_id, 'Выберите раздел русского языка:', reply_markup=generate_markup(buttons, 2))


@bot.message_handler(content_types=['text'])
async def pravila(message):

    if message.text == 'Пунктуация':
        buttons = ['Запятая', 'Тире', 'Двоеточие']
        await bot.send_message(message.chat.id, 'Выберите знак препинания:', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Запятая':
        await bot.send_message(message.chat.id, 'Правило 1: \nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством повторяющихся союзов и...и, ни...ни, или...или и т. п., например: \n«И всё тошнит, и голова кружится, и мальчики кровавые в глазах...» (Пушкин).')
        await bot.send_message(message.chat.id, 'Правило 2: \nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством союзов и, да (в значении «и»), да и, или, либо, а также союзов а, и, да (в значении «но»), например: \n«Море глухо роптало, и волны бились о берег бешено и гневно» (М. Горький).')
        await bot.send_message(message.chat.id, 'Правило 3: \nЗапятая ставится между главным и придаточным предложениями, а если придаточное стоит внутри главного, то оно выделяется запятыми с обеих сторон, например: \n«Дорогою свободной иди, куда влечёт тебя свободный ум» (Пушкин).')
        buttons = ['Упражнение на постановку запятой','Вернуться']
        await bot.send_message(message.chat.id, 'Выполнить упражнение или вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Упражнение на постановку запятой':
        button_dict = {'Запятая': 'first',
                       'Пробел': 'second',
                       }
        await bot.send_message(message.chat.id, 'Что стоит на месте пропуска (1)?\n«Несколько в стороне от него темнел жалкий вишнёвый садик с плетнём(1) да под окнами, склонив свои тяжёлые головы, стояли спавшие подсолнечники» (Чехов).', reply_markup=create_keyboard_markup(button_dict))

    if message.text == 'Тире':
        await bot.send_message(message.chat.id, 'Правило 1: \nТире ставится перед это, это есть, это значит, вот, если сказуемое, выраженное существительным в именительном падеже или неопределённой формой, присоединяется посредством этих слов к подлежащему, например:\n«Поэзия — это огненный взор юноши, кипящего избытком сил» (Белинский).')
        await bot.send_message(message.chat.id, 'Правило 2: \nТире ставится перед обобщающим словом, стоящим после перечисления, например:\n«Надежду и пловца — всё море поглотило» (Крылов).')
        await bot.send_message(message.chat.id, 'Правило 3: \nТире ставится между предложениями, не соединёнными посредством союзов, если второе предложение заключает в себе результат или вывод из того, о чём говорится в первом, например:\n«Хвалы приманчивы — как их не пожелать?» (Крылов).')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, 'Вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Двоеточие':
        await bot.send_message(message.chat.id, 'Правило 1: \nДвоеточие ставится перед перечислением, которым заканчивается предложение, если перечислению предшествует обобщающее слово (а нередко, кроме того, ещё слова «например», «как-то», «а именно»), например:\n«Острогою бьётся крупная рыба, как-то: щуки, сомы, жерехи, судаки» (С. Аксаков).')
        await bot.send_message(message.chat.id, 'Правило 2: \nДвоеточие ставится между двумя предложениями, не соединёнными посредством союзов, если в первом предложении такими глаголами, как видеть, смотреть, слышать, знать, чувствовать и т. п., делается предупреждение, что далее последует изложение какого-нибудь факта или какое-нибудь описание, например:\n«Павел чувствует: чьи-то пальцы дотрагиваются до его руки выше локтя» (Н. Островский).')
        await bot.send_message(message.chat.id, 'Правило 3: \nДвоеточие ставится после предложения, за которым следует одно или несколько предложений, не соединённых с первым посредством союзов и заключающих в себе разъяснение или причину того, о чём говорится в первом предложении, например:\n«Я не ошибся: старик не отказался от предлагаемого стакана» (Пушкин).')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, 'Вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Орфография':
        buttons = ['Гласные', 'Согласные']
        await bot.send_message(message.chat.id, 'Выберите группу букв:', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Гласные':
        await bot.send_message(message.chat.id, 'Правило 1: \n\n')
        await bot.send_message(message.chat.id, 'Правило 2: \n\n')
        await bot.send_message(message.chat.id, 'Правило 3: \n\n')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, 'Вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Согласные':
        await bot.send_message(message.chat.id, 'Правило 1: \n\n')
        await bot.send_message(message.chat.id, 'Правило 2: \n\n')
        await bot.send_message(message.chat.id, 'Правило 3: \n\n')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, 'Вернуться на главную?', reply_markup=generate_markup(buttons, 1))

    if message.text=='Вернуться':
        buttons = ['Пунктуация', 'Орфография']
        await bot.send_message(message.chat.id, 'Выберите раздел русского языка:', reply_markup=generate_markup(buttons, 2))

    if message.text!='Пунктуация' and message.text!='Запятая' and message.text!='Тире' and message.text!='Двоеточие' and message.text!='Гласные' and message.text!='Согласные' and message.text!='Вернуться' and message.text!='Упражнение на постановку запятой':
        word = message.text
        word = word.lower()
        definition, spelling_rules = get_word_definition(word)
        if definition:
            await bot.send_message(message.chat.id, f"Определение слова '{word}':")
            await bot.send_message(message.chat.id, definition)
        else:
            await bot.send_message(message.chat.id, f"Определение слова '{word}' не найдено.")
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, 'Вернуться на главную?', reply_markup=generate_markup(buttons, 1))

        # if spelling_rules:
        #     await bot.send_message(message.chat.id, f"Происхождение слова '{word}':")
        #     await bot.send_message(message.chat.id, spelling_rules)
        # else:
        #     await bot.send_message(message.chat.id, f"Происхождение слова '{word}' не найдено.")


@bot.callback_query_handler(func=lambda call:True)
async def handle_callback(call):
    call_id=call.message.chat.id
    button_call=call.data
    if button_call=='first':
        await bot.send_message(call_id, 'Правильный ответ✅')
        #сделать вернуться на главную?
    if button_call=='second':
        await bot.send_message(call_id, 'Неправильный ответ❌')
        await bot.send_message(call_id, 'Пояснение:\nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством союза «да» (в значении «и»).')


import asyncio
asyncio.run(bot.polling())