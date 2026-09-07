import os
import requests
import telebot
from flask import Flask, request

TOKEN = "8770815242:AAFPNZOiXBsQzyE6goZ600UUKa4VI3EhIr4"
bot = telebot.TeleBot(TOKEN)

app = Flask(name)

@app.route("/")
def home():
return "Bot is running 24/7!"

@bot.message_handler(commands=["start"])
def send_welcome(message):
bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")

@bot.message_handler(func=lambda message: True)
def handle_ai_message(message):
user_message = message.text
flowise_url = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"

try:
response = requests.post(flowise_url, json={"question": user_message})
data = response.json()

# استخراج الرد بشكل صحيح وآمن
if isinstance(data, dict):
ai_answer = data.get("text") or data.get("json", {}).get(
"text", "عذراً، لم أتمكن من صياغة الإجابة."
)
else:
ai_answer = str(data)

bot.reply_to(message, ai_answer)
except Exception as e:
bot.reply_to(message, "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي.")

def run_bot():
bot.infinity_polling()

if name == "main":
import threading

t = threading.Thread(target=run_bot)
t.start()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)