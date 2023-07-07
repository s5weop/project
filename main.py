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
    rules_element = soup.find("span", {"class": "mw-headline", "id": "Библиография"})
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
    await bot.send_message(chat_id, 'Привет, данный бот поможет тебе:\n— узнать (или вспомнить) правила русского языка;\n— найти определение слова: для этого <b>напиши в чат слово</b>, у которого необходимо узнать значение.')
    buttons = ['Пунктуация', 'Орфография']
    await bot.send_message(chat_id, 'Выберите раздел русского языка:', reply_markup=generate_markup(buttons, 2))


@bot.message_handler(content_types=['text'])
async def pravila(message):

    if message.text == 'Пунктуация':
        buttons = ['Запятая', 'Тире', 'Двоеточие']
        await bot.send_message(message.chat.id, 'Выберите знак препинания:', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Запятая':
        #await bot.send_message(message.chat.id, 'Правило 1: \nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством повторяющихся союзов и...и, ни...ни, или...или и т. п., например: \nИ всё тошнит, и голова кружится, и мальчики кровавые в глазах... (Пушкин).')
        await bot.send_message(message.chat.id, '<b>Правило 1:</b>')
        await bot.send_message(message.chat.id,
                               'Запятая ставится между предложениями, объединяемыми в одно сложное предложение посредством повторяющихся союзов и...и, ни...ни, или...или и т. п., <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«И всё тошнит, и голова кружится, и мальчики кровавые в глазах...»</i> (Пушкин).')
        #await bot.send_message(message.chat.id, 'Правило 2: \nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством союзов и, да в значении и, да и, или, либо, а также союзов а, и, да в значении но, например: \nМоре глухо роптало, и волны бились о берег бешено и гневно (М. Горький).')
        await bot.send_message(message.chat.id, '<b>Правило 2:</b>')
        await bot.send_message(message.chat.id, 'Запятая ставится между предложениями, объединяемыми в одно сложное предложение посредством союзов и, да (в значении и), да и, или, либо, а также союзов а, и, да (в значении но), <b>например:</b>')
        await bot.send_message(message.chat.id, '<i>«Море глухо роптало, и волны бились о берег бешено и гневно»</i> (М. Горький).')
        #await bot.send_message(message.chat.id, 'Правило 3: \nЗапятая ставится между главным и придаточным предложениями, а если придаточное стоит внутри главного, то оно выделяется запятыми с обеих сторон, например: \nДорогою свободной иди, куда влечёт тебя свободный ум (Пушкин).')
        await bot.send_message(message.chat.id, '<b>Правило 3:</b>')
        await bot.send_message(message.chat.id,
                               'Запятая ставится между главным и придаточным предложениями, а если придаточное стоит внутри главного, то оно выделяется запятыми с обеих сторон, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Дорогою свободной иди, куда влечёт тебя свободный ум»</i> (Пушкин).')
        buttons = ['Упражнение на постановку запятой','Вернуться']
        await bot.send_message(message.chat.id, 'Выполнить упражнение или <b>вернуться на главную</b>?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Упражнение на постановку запятой':
        button_dict = {'Запятая': 'first',
                       'Пробел': 'second',
                       }
        await bot.send_message(message.chat.id, 'Что стоит на месте <b>пропуска (1)</b>?')
        await bot.send_message(message.chat.id, '«Несколько в стороне от него темнел жалкий вишнёвый садик с плетнём<b>(1)</b> да под окнами, склонив свои тяжёлые головы, стояли спавшие подсолнечники» (Чехов).', reply_markup=create_keyboard_markup(button_dict))

    if message.text == 'Тире':
        #await bot.send_message(message.chat.id, 'Правило 1: \n Тире ставится перед это, это есть, это значит, вот, если сказуемое, выраженное существительным в именительном падеже или неопределённой формой, присоединяется посредством этих слов к подлежащему, например:\n «Поэзия — это огненный взор юноши, кипящего избытком сил» (Белинский).')
        await bot.send_message(message.chat.id, '<b>Правило 1:</b>')
        await bot.send_message(message.chat.id,
                               'Тире ставится перед это, это есть, это значит, вот, если сказуемое, выраженное существительным в именительном падеже или неопределённой формой, присоединяется посредством этих слов к подлежащему, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Поэзия — это огненный взор юноши, кипящего избытком сил»</i> (Белинский).')
        #await bot.send_message(message.chat.id, 'Правило 2: \n Тире ставится перед обобщающим словом, стоящим после перечисления, например:\n «Надежду и пловца — всё море поглотило» (Крылов).')
        await bot.send_message(message.chat.id, '<b>Правило 2:</b>')
        await bot.send_message(message.chat.id,
                               'Тире ставится перед обобщающим словом, стоящим после перечисления, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Надежду и пловца — всё море поглотило»</i> (Крылов).')
        #await bot.send_message(message.chat.id, 'Правило 3: \n Тире ставится между предложениями, не соединёнными посредством союзов, если второе предложение заключает в себе результат или вывод из того, о чём говорится в первом, например:\n «Хвалы приманчивы — как их не пожелать?» (Крылов).')
        await bot.send_message(message.chat.id, '<b>Правило 3:</b>')
        await bot.send_message(message.chat.id,
                               'Тире ставится между предложениями, не соединёнными посредством союзов, если второе предложение заключает в себе результат или вывод из того, о чём говорится в первом, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Хвалы приманчивы — как их не пожелать?»</i> (Крылов).')
        buttons = ['Упражнение на постановку тире','Вернуться']
        await bot.send_message(message.chat.id, 'Выполнить упражнение или <b>вернуться на главную</b>?', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Упражнение на постановку тире':
        button_dict = {'Тире': 'third',
                       'Двоеточие': 'fourth',
                       'Пробел': 'fifth'
                       }
        await bot.send_message(message.chat.id, 'Что стоит на месте <b>пропуска (1)</b>?')
        await bot.send_message(message.chat.id, '«Ни крики петуха, ни звучный гул рогов, ни ранней ласточки на кровле щебетанье <b>(1)</b> ничто не вызовет почивших из гробов» (Жуковский).', reply_markup=create_keyboard_markup(button_dict))

    if message.text == 'Двоеточие':
        #await bot.send_message(message.chat.id, 'Правило 1: \n Двоеточие ставится перед перечислением, которым заканчивается предложение, если перечислению предшествует обобщающее слово (а нередко, кроме того, ещё слова «например», «как-то», «а именно»), например:\n «Острогою бьётся крупная рыба, как-то: щуки, сомы, жерехи, судаки» (С. Аксаков).')
        await bot.send_message(message.chat.id, '<b>Правило 1:</b>')
        await bot.send_message(message.chat.id,
                               'Двоеточие ставится перед перечислением, которым заканчивается предложение, если перечислению предшествует обобщающее слово (а нередко, кроме того, ещё слова «например», «как-то», «а именно»), <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Острогою бьётся крупная рыба, как-то: щуки, сомы, жерехи, судаки»</i> (С. Аксаков).')
        #await bot.send_message(message.chat.id, 'Правило 2: \n Двоеточие ставится между двумя предложениями, не соединёнными посредством союзов, если в первом предложении такими глаголами, как видеть, смотреть, слышать, знать, чувствовать и т. п., делается предупреждение, что далее последует изложение какого-нибудь факта или какое-нибудь описание, например:\n «Павел чувствует: чьи-то пальцы дотрагиваются до его руки выше локтя» (Н. Островский).')
        await bot.send_message(message.chat.id, '<b>Правило 2:</b>')
        await bot.send_message(message.chat.id,
                               'Двоеточие ставится между двумя предложениями, не соединёнными посредством союзов, если в первом предложении такими глаголами, как видеть, смотреть, слышать, знать, чувствовать и т. п., делается предупреждение, что далее последует изложение какого-нибудь факта или какое-нибудь описание, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Павел чувствует: чьи-то пальцы дотрагиваются до его руки выше локтя»</i> (Н. Островский).')
        #await bot.send_message(message.chat.id, 'Правило 3: \n Двоеточие ставится после предложения, за которым следует одно или несколько предложений, не соединённых с первым посредством союзов и заключающих в себе разъяснение или причину того, о чём говорится в первом предложении, например:\n «Я не ошибся: старик не отказался от предлагаемого стакана» (Пушкин).')
        await bot.send_message(message.chat.id, '<b>Правило 3:</b>')
        await bot.send_message(message.chat.id,
                               'Двоеточие ставится после предложения, за которым следует одно или несколько предложений, не соединённых с первым посредством союзов и заключающих в себе разъяснение или причину того, о чём говорится в первом предложении, <b>например:</b>')
        await bot.send_message(message.chat.id,
                               '<i>«Я не ошибся: старик не отказался от предлагаемого стакана»</i> (Пушкин).')
        buttons = ['Упражнение на постановку двоеточия', 'Вернуться']
        await bot.send_message(message.chat.id, 'Выполнить упражнение или <b>вернуться на главную</b>?',
                               reply_markup=generate_markup(buttons, 1))

    if message.text == 'Упражнение на постановку двоеточия':
        button_dict = {'Двоеточие': 'sixth',
                       'Тире': 'seventh',
                       'Пробел': 'eighth'
                       }
        await bot.send_message(message.chat.id, 'Что стоит на месте <b>пропуска (1)</b>?')
        await bot.send_message(message.chat.id, '«Не нагнать тебе бешеной тройки<b>(1)</b> кони сыты, и крепки, и бойки» (Некрасов).', reply_markup=create_keyboard_markup(button_dict))

    if message.text == 'Орфография':
        buttons = ['Гласные', 'Согласные']
        await bot.send_message(message.chat.id, 'Выберите группу букв:', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Гласные':
        await bot.send_message(message.chat.id, '<b>Правило 1:</b> \nВ неударяемых слогах пишутся гласные, одинаковые с теми, которые произносятся в той же части слова, когда эта часть стоит под ударением, <b>например:</b>\n<b>в корнях:</b> <i>жара</i> (жар), <i>шалун</i> (ша́лость)\n<b>в приставках:</b> <i>поддаваться</i> (по́дданный, по́дступ), <i>отпирать</i> (о́тпер)\n<b>в суффиксах:</b> <i>лекарь</i> (врата́рь), <i>заборишко</i> (доми́шко)\n<b>в окончаниях:</b> <i>масло</i> (весло́), <i>стулом</i> (столо́м)')
        await bot.send_message(message.chat.id, '<b>Правило 2:</b> \nПри сочетании приставки, оканчивающейся на согласный, с корнем или с другой приставкой, которые начинаются с и, пишется, согласно с произношением, по общему правилу ы, <b>например:</b>\n<i>розыск, предыдущий, возыметь, изымать</i> (но: <i>взимать</i>, где произносится и)')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, '<b>Вернуться на главную?</b>', reply_markup=generate_markup(buttons, 1))

    if message.text == 'Согласные':
        await bot.send_message(message.chat.id, '<b>Правило 1:</b> \nЧтобы правильно написать согласную в конце слова или перед другими согласными нужно взять другую форму того же слова или подобрать другое слово того же корня, где после согласной оказалась бы гласная, и писать ту согласную, которая пишется перед гласной, <b>например:</b>\n<i>дуб, дубки</i> (дубы), <i>рукав, рукавчик</i> (рукава)')
        await bot.send_message(message.chat.id, '<b>Правило 2:</b> \nПравило 1 относится также к приставкам, например:\n<i>входить</i> (влезать), <i>надколоть</i> (надрубить)')
        await bot.send_message(message.chat.id, '<b>Правило 3:</b> \nВ приставках без-, воз-, вз-, из-, низ-, раз-, роз-, чрез- (через-) перед глухими к, п, с, т, ф, х, ц, ч, ш, щ пишется с вместо з, <b>например:</b>\n<i>бесполезный, воспитать, вспахать</i>')
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, '<b>Вернуться на главную?</b>', reply_markup=generate_markup(buttons, 1))

    if message.text=='Вернуться':
        buttons = ['Пунктуация', 'Орфография']
        await bot.send_message(message.chat.id, 'Выберите раздел русского языка:', reply_markup=generate_markup(buttons, 2))

    if message.text!='Пунктуация' and message.text!='Запятая' and message.text!='Тире' and message.text!='Орфография' and message.text!='Двоеточие' and message.text!='Гласные' and message.text!='Согласные' and message.text!='Вернуться' and message.text!='Упражнение на постановку запятой' and message.text!='Упражнение на постановку тире' and message.text!='Упражнение на постановку двоеточия':
        word = message.text
        word = word.lower()
        definition, spelling_rules = get_word_definition(word)
        if definition:
            await bot.send_message(message.chat.id, f"Определение слова <b>'{word}'</b>:")
            await bot.send_message(message.chat.id, definition)
        else:
            await bot.send_message(message.chat.id, f"Определение слова <b>'{word}'</b> не найдено.")

        if spelling_rules:
            await bot.send_message(message.chat.id, f"Использованные источники для слова <b>'{word}'</b>:")
            await bot.send_message(message.chat.id, spelling_rules)
        else:
            await bot.send_message(message.chat.id, f"Использованные источники для слова <b>'{word}'</b> не найдены.")
        buttons = ['Вернуться']
        await bot.send_message(message.chat.id, '<b>Вернуться на главную?</b>', reply_markup=generate_markup(buttons, 1))


@bot.callback_query_handler(func=lambda call:True)
async def handle_callback(call):
    call_id=call.message.chat.id
    button_call=call.data
    if button_call=='first':
        await bot.send_message(call_id, 'Правильный ответ✅')
    if button_call=='second':
        await bot.send_message(call_id, 'Неправильный ответ❌')
        await bot.send_message(call_id, '<b>Пояснение:</b>\nЗапятая ставится между предложениями, объединяемыми в одно сложное предложение посредством союза «да» (в значении «и»).')

    if button_call=='third':
        await bot.send_message(call_id, 'Правильный ответ✅')
    if button_call=='fourth' or button_call=='fifth':
        await bot.send_message(call_id, 'Неправильный ответ❌')
        await bot.send_message(call_id, '<b>Пояснение:</b>\nТире ставится перед обобщающим словом, стоящим после перечисления.')

    if button_call=='sixth':
        await bot.send_message(call_id, 'Правильный ответ✅')
    if button_call=='seventh' or button_call=='eighth':
        await bot.send_message(call_id, 'Неправильный ответ❌')
        await bot.send_message(call_id, '<b>Пояснение:</b>\nДвоеточие ставится после предложения, за которым следует одно или несколько предложений, не соединённых с первым посредством союзов и заключающих в себе причину того, о чём говорится в первом предложении.')

    buttons = ['Вернуться']
    await bot.send_message(call_id, '<b>Вернуться на главную?</b>', reply_markup=generate_markup(buttons, 1))


import asyncio
asyncio.run(bot.polling())