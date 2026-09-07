import os
import requests
import telebot
from flask import Flask, request

TOKEN = "8770815242:AAFPNZOiXBsQzyE6goZ600UUKa4VI3EhIr4"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")


# دالة استقبال الرسائل وتحويلها إلى Flowise
@bot.message_handler(func=lambda message: True)
def handle_ai_message(message):
  user_message = message.text

  # هذا هو رابط الـ API الصحيح لـ Flowise الذي أخذناه قبل قليل
  flowise_url = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"

  try:
    response = requests.post(flowise_url, json={"question": user_message})
    ai_answer = response.json().get(
        "text", "عذراً، حدث خطأ في معالجة طلبك الذكي."
    )
    bot.reply_to(message, ai_answer)
  except Exception as e:
    bot.reply_to(
        me