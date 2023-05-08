from telebot import TeleBot
from  parsing import result
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from slugify import slugify


token = "6024401349:AAGqUrlUnYbBtdwG-ochXgqvf7rC4z059EA"
bot = TeleBot(token)

data = result
keyboard = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton(
    card["title"],callback_data=str(card["id"])

    )for card in data
]
keyboard.add(*buttons)

@bot.message_handler(commands= ["start"])
def start_message(message):
    bot.send_message(message.chat.id,"Hello,how may i help you?",reply_markup=keyboard)

@bot.callback_query_handler(lambda callback:callback.data.isdigit())
def sent_details(callback):
    for card in data:
        if callback.data == str(card["id"]):
            bot.send_message(callback.message.chat.id,f"Title: {card['title']}, Price:  {card['price']}")
    else:
        bot.send_message(callback.message.chat.id, "What else", reply_markup=keyboard)


bot.polling()    



