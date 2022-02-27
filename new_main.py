from telebot.util import extract_arguments
import telebot

from auth_data import token
from stock import Stock

def telegram_bot(token):
    bot = telebot.TeleBot(token)
    stock = Stock()

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, f"Greetings! Type /stock + <name of your ticker> to get advice.")
    
    @bot.message_handler(commands=["stock"])
    def stock_message(message):
        try:
            stock.tic = extract_arguments(message.text)
            interval = bot.send_message(message.chat.id, text = "Choose the interval: " + ' '.join(str(inter) for inter in stock.intervals))
            bot.register_next_step_handler(interval, get_interval)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ticker cannot be found')   

    def get_interval(message):
        user_inter = message.text

        try:
            if user_inter not in stock.intervals:
                raise ValueError()
            stock.interval = message.text
            bot.register_next_step_handler(message, get_advice)
            get_advice(message)
        except Exception as e:
            bot.send_message(message.chat.id, f"Interval '{user_inter}' is not found")   

    def get_advice(message):
        try:
            stock.crossing()
            bot.send_message(message.chat.id, f"{stock.long_response}\n\n{stock.short_response}")   
        except Exception as e:
            bot.send_message(message.chat.id, "Something's wrong. Try again.")

    bot.polling()
    bot.get_my_commands


if __name__ == '__main__':
    telegram_bot(token)