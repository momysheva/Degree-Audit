import telebot
from telebot import types
import major_audit


# Create a bot object
API_KEY = "6901367940:AAHt49OPRKl_OaqEQ3nmV0gJGD_j7U_MZqM"
bot = telebot.TeleBot(API_KEY)

majors= ['PLS', 'SOC', 'HST', 'ECON', 'WLL', 'BIOL', 'CHEM', 'MATH', 'PHYS']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to SSH Audit Bot! Please select the major you would like to audit.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for major in majors:
        markup.add(types.KeyboardButton(major))

    bot.send_message(message.chat.id, "Please select major:", reply_markup=markup)
    bot.register_next_step_handler(message, process_major,majors)

def process_major(message,majors):
    if message.text in majors:
        major_audit.major_check(message.text)
        bot.send_message(message.chat.id, f"Audit completed. Please check the folder {message.text} anf file {message.text}_Final. \nIf you want to check another major, please type /start.")

    else:
        bot.reply_to(message, "Please select a valid major.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for major in majors:
            markup.add(types.KeyboardButton(major))

        bot.send_message(message.chat.id, "Please select major:", reply_markup=markup)
        bot.register_next_step_handler(message, process_major,majors)

        

bot.polling(none_stop=True)

