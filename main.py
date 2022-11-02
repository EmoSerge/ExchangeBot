import telebot
from extensions import BotException, Convertor
from tok import TOKEN, currency

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def instructions(message: telebot.types.Message):
    text = "Это конвертер валют!\n" \
           "Для конвертации введите конвертируемые валюты в виде \n" \
           "xxx yyy zzz.zz, где \n" \
           "ххх - обозначение конвертируемой валюта \n" \
           "yyy - обозначение валюты в которую переводим \n" \
           "zzz.zz - количество конвертируемой валюты \n" \
           "Пример запроса - usd rub 100.35 \n" \
           "со списком доступных валют можно ознакомится по команде /currency"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['currency'])
def listofcur(message: telebot.types.Message):
    text = "Валюты для конвертации: \n"
    for i in currency.keys():
        row = f"{i} - {currency[i]}"
        text = '\n'.join((text, row))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise BotException('Неверное количество параметров в запросе!')

        answer = Convertor.get_price(*values)

    except BotException as e:
        bot.reply_to(message, f"Ошибка в запросе:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
