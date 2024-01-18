import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import datetime
bot = telebot.TeleBot(config.API_TOKEN)

@bot.message_handler(commands=['delete'])
def message(message):
    user_id = message.from_user.id
    con = sqlite3.connect("history_of_text.db")
    with con:
        cur = con.cursor()
        con.execute("DELETE FROM history WHERE user_id = ? ", (user_id,))
        cur.close()

@bot.message_handler(commands=['show_all'])
def message(message):
    user_id = message.from_user.id
    con = sqlite3.connect("history_of_text.db")
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history WHERE user_id = ?",(user_id,))
        resal = cur.fetchall()
        for r in resal:
            if r: # не забудь про проверку на случай, если история пуста
                bot.send_message(message.chat.id, f'user name :@{r[4]}, time: {r[2]}, text: {r[3]}.')
            else:
                bot.send_message(message.chat.id, "История пуста")
        cur.close()

@bot.message_handler(commands=['show'])
def message(message):
    user_id = message.from_user.id
    n = int(telebot.util.extract_arguments(message.text))
    con = sqlite3.connect("history_of_text.db")
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history WHERE user_id = ?",(user_id,))
        if n :
            resal = cur.fetchmany(n)
        else :
            resal = cur.fetchone()
        for r in resal:
            if r: # не забудь про проверку на случай, если история пуста
                bot.send_message(message.chat.id, f'user name :@{r[4]}, time: {r[2]}, text: {r[3]}.')
            else:
                bot.send_message(message.chat.id, "История пуста")
        cur.close()

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.from_user.id
    text = message.text
    date = datetime.datetime.fromtimestamp(message.date)
    user_name = message.from_user.username
    con = sqlite3.connect("history_of_text.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO history(user_id,text,datime,user_name) VALUES (?,?,?,?)",(user_id,text,date,user_name))
        cur.close()

bot.infinity_polling()