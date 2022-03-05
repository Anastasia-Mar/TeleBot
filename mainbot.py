import telebot
from config import currency
from config import TOKEN
from Extensions import CurrencyConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", 'help'])
def help_message(message: telebot.types.Message):
    text = "To begin enter the next command to the bot in the following format: \
     <currency name>  <currency you'd like to exchange to>  \
     <the amount of initial currency> \
     To see all the available currencies use the command /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Available currencies:"
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        message_values = message.text.split(' ')

        if len(message_values) > 3:
            raise ConvertionException("Too many parameters")

        quote, base, amount = message_values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message,f"User error\n{e}")
    except Exception as e:
        bot.reply_to(message,f'Unable to process the command\n{e}')
    else:
        text = f'Value of {amount} {quote} in {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()
