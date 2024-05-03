# --------------------Library and Token--------------------#
import os
import telebot
from telebot import types
import phonenumbers
import asyncio
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = AsyncTeleBot(API_TOKEN)

markup_first = types.InlineKeyboardMarkup()
age_one = types.InlineKeyboardButton("6-8 лет", callback_data="6-8 лет")
age_two = types.InlineKeyboardButton("9-11 лет", callback_data="9-11 лет")
age_three = types.InlineKeyboardButton("12-14 лет", callback_data="12-14 лет")
markup_first.row(age_one, age_two, age_three)
markup_second = telebot.types.ReplyKeyboardMarkup(True)
btn_send_phone = types.KeyboardButton(text="отправить мой номер", request_contact=True)

markup_second.row(btn_send_phone)

mur_age_data = ["6-8 лет", "9-11 лет", "12-14 лет"]
# mur_addres_data = ["Ул. Победы 304", "Ул. Отдельская 257/9к2"]


@bot.message_handler(commands=["start"])
async def welcome(message):
    if message.text == "/start":
        await bot.send_message(
            message.chat.id,
            f"""Школа программирования для детей KIBERone в Славянске-на-Кубани приветствует вас 🤗
            
В эти выходные мы проводим бесплатный мастер-класс для детей 6-14 лет по искусственному интеллекту 
            
На мастер-классе: 
✅ Ребенок познакомиться с магией нейросетей и узнает, как применять искусственный интеллект в деле.
✅ Создаст своего персонажа из игры ROBLOX с помощью искусственного интеллекта.
✅ Узнает как применять гаджеты, с пользой и весело проведут время.
            
А родители в это время узнают об увлечениях современных детей, которые будут полезны в будущем для каждого ребёнка. 

Длительность занятия 60 минут. Текущий уровень не важен. Научим любого ребенка. Количество участников до 12 человек. 
            
Где проходят мастер-классы: 
📌 Ул. Отдельская 257/9 к2 (ЖК Озёрный)
            
Укажите возраст вашего ребенка, чтобы мы подобрали для него оптимальную группу на мастер-класс.  👇""",
            parse_mode="html",
            reply_markup=markup_first,
        )


@bot.callback_query_handler(func=lambda callback: True)
async def answer(callback):
    if callback.data in mur_age_data:
        await bot.send_message(
            callback.message.chat.id,
            """Спасибо! Остался последний шаг😊

Укажите ваш номер телефона в формате 
+7(XXX) XXX-XX-XX.
Наш администратор отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время 🤗""",
            parse_mode="html",
            reply_markup=markup_second,
        )
        await bot.send_message(
            "@testGRRrr",
            callback.data
            + f" @{callback.message.chat.username} {callback.message.chat.first_name} {callback.message.chat.last_name} ",
        )


@bot.message_handler(content_types=["text"])
async def contact(message):
    if not message.text.startswith("+") or not phonenumbers.parse(message.text, None):
        await bot.send_message(
            message.chat.id,
            "Возможно, вы неправильно написали номер телефона. Пожалуйста, введите в формате +7(XXX) XXX-XX-XX",
        )
    else:
        await bot.send_message(
            message.chat.id,
            f"""
Спасибо! В ближайшее время с Вами свяжется администратор.
С уважением, KIBERone ❤️
""",
        )
        await bot.forward_message("@testGRRrr", message.chat.id, message.id)

        # await bot.send_message(
        #     "@testGRRrr",
        #     f"{message.text} @{message.chat.username} {message.chat.first_name} ",
        # )


@bot.message_handler(content_types=["contact"])
async def check_contact(message):
    if message.contact.user_id == message.from_user.id:
        await bot.forward_message("@testGRRrr", message.chat.id, message.id)
        await bot.send_message(
            message.chat.id,
            """
Спасибо! В ближайшее время с Вами свяжется администратор.
С уважением, KIBERone ❤️
""",
        )

    else:
        await bot.send_message(
            message.chat.id,
            "Телефон не валидный. Попробуйте написать его в формате +7(XXX) XXX-XX-XX",
        )


asyncio.run(bot.polling(non_stop=True))
