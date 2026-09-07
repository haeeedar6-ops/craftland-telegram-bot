import os
import threading
import telebot
from flask import Flask, request

TOKEN = "8853749299:AAGtqxZtasFK7pp6EIjTEQPQ7SICkkg-nfs"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! ")


def run_bot():
  bot.infinity_polling()


if __name__ == "__main__":
  t = threading.Thread(target=run_bot)
  t.start()

  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)