import os
import logging
import threading
import requests
import telebot
from flask import Flask

# ================== الإعدادات ==================
TOKEN = "8770815242:AAEtPJwdc79G0mwZdRQZyIxcsbSOpJVxeYg"
FLOWISE_URL = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"
REQUEST_TIMEOUT = 60  # ثانية

# ================== تسجيل الأخطاء (Logging) ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("craftland_bot")

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running 24/7!"


# ================== دالة موحّدة للاتصال بـ Flowise ==================
def ask_flowise(question: str, file_url: str | None = None) -> str:
    payload = {"question": question}
    if file_url:
        payload["overrideConfig"] = {"uploads": [{"data": file_url, "type": "url"}]}

    try:
        res = requests.post(FLOWISE_URL, json=payload, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        data = res.json()
        ans = data.get("text") if isinstance(data, dict) else None
        return ans or "تم استلام الرد، بس ما وصلني نص واضح."
    except requests.exceptions.Timeout:
        logger.error("Flowise timeout")
        return "⏳ السيرفر تأخر بالرد، جرب كمان مرة بعد شوي."
    except requests.exceptions.RequestException as e:
        logger.error(f"Flowise request error: {e}")
        return "⚠️ صار خطأ بالاتصال بالذكاء الاصطناعي، جرب مرة تانية."
    except ValueError as e:
        logger.error(f"Flowise JSON parse error: {e}")
        return "⚠️ الرد اللي رجع مش بصيغة سليمة."


# ================== أوامر البوت ==================
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت أرض الحرف الخاص بفري فاير! 🔥")


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        bot.reply_to(message, "🔍 جاري تحليل سكريبت البلوكات للصورة...")

        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        caption = (
            message.caption
            or "حلل لي هذه الصورة لسكريبت البلوكات واشرح لي كيف يعمل هذا النظام:"
        )

        ans = ask_flowise(caption, file_url=file_url)
        bot.reply_to(message, ans)

    except telebot.apihelper.ApiException as e:
        logger.error(f"Telegram API error (photo): {e}")
        bot.reply_to(message, "⚠️ صار خطأ بجلب الصورة من تيليغرام.")
    except Exception as e:
        logger.exception(f"Unexpected error in handle_photo: {e}")
        bot.reply_to(message, "حدث خطأ غير متوقع أثناء تحليل الصورة.")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_ai_message(message):
    try:
        ans = ask_flowise(message.text)
        bot.reply_to(message, ans)
    except Exception as e:
        logger.exception(f"Unexpected error in handle_ai_message: {e}")
        bot.reply_to(message, "حدث خطأ غير متوقع، جرب مرة تانية.")


# ================== تشغيل البوت مع إعادة محاولة تلقائية ==================
def run_bot():
    while True:
        try:
            bot.remove_webhook()
        except Exception as e:
            logger.warning(f"remove_webhook failed: {e}")

        try:
            logger.info("Bot polling started.")
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            logger.error(f"Polling crashed, restarting in 5s: {e}")
            import time

            time.sleep(5)


if __name__ == "__main__":
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
