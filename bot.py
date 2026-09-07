import os
import requests
import telebot
from flask import Flask

TOKEN = "8853749299:AAGtqxZtasFK7pp6EIjTEQPQ7SICKkg-nfs"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")


@bot.message_handler(func=lambda m: True)
def handle_ai_message(message):
  url = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"
  try:
    res = requests.post(url, json={"question": message.text})
    data = res.json()
    ans = (
        data.get("text")
        if isinstance(data, dict)
        else "عذراً، لم أتمكن من الإجابة."
    )
    bot.reply_to(message, ans if ans else "تم الاستلام!")
  except Exception:
    bot.reply_to(message, "حدث خطأ في الاتصال بالذكاء الاصطناعي.")


def run_bot():
  bot.infinity_polling()


if __name__ == "__main__":
  import threading

  t = threading.Thread(target=run_bot)
  t.start()
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
