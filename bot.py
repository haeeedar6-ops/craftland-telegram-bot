import os
import telebot
from flask import Flask, request

TOKEN = "8770815242:AAHZ5-06ck0ktdx_Yw-sTlda5Bz8Dz6izEM"
bot = telebot.TeleBot(TOKEN)
# سيرفر وهمي بسيط لتبقى خدمة Render (Web Service) سعيدة وشغالة
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")


# باقي أوامر البوت الخاصة بك هنا...

# تشغيل السيرفر الوهمي مع البوت
if __name__ == "__main__":
  import threading

  # تشغيل البوت بخاصية الـ Polling في الخلفية
  def run_bot():
    bot.infinity_polling()

  t = threading.Thread(target=run_bot)
  t.start()

  # تشغيل سيرفر Flask على المنفذ المطلوب من Render
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)