import os
import requests
import telebot
from flask import Flask

TOKEN = "8770815242:AAEtPJwdc79G0mwZdRQZyIxcsbSOpJVxeYg"
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
  try:
    bot.reply_to(message, "🔍 جاري تحليل سكريبت البلوكات للصورة يا حيدر...")

    # الحصول على أعلى دقة للصورة المرفوعة
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    # النص المرافق للصورة أو سؤال افتراضي للتحليل
    caption = (
        message.caption
        if message.caption
        else "حلل لي هذه الصورة لسكريبت البلوكات واشرح لي كيف يعمل هذا النظام:"
    )

    # إرسال الصورة والرابط إلى Flowise API
    url = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"
    payload = {
        "question": caption,
        "overrideConfig": {"uploads": [{"data": file_url, "type": "url"}]},
    }

    res = requests.post(url, json=payload)
    data = res.json()
    ans = (
        data.get("text")
        if isinstance(data, dict)
        else "عذراً، لم أتمكن من تحليل الصورة."
    )
    bot.reply_to(message, ans if ans else "تم استلام التحليل!")

  except Exception as e:
    bot.reply_to(
        message, "حدث خطأ أثناء محاولة جلب أو تحليل الصورة عبر الذكاء الاصطناعي."
    )


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
  try:
    bot.remove_webhook()
  except:
    pass
  bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
  import threading

  t = threading.Thread(target=run_bot)
  t.start()
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
