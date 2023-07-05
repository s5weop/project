import os
from telebot.async_telebot import AsyncTeleBot
#from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

bot = AsyncTeleBot(TOKEN, parse_mode='HTML')