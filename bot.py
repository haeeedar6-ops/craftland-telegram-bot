import telebot
import requests

TOKEN = '8770815242:AAHZ5-06ck0ktdx_Yw-sTlda5Bz8Dz6izEM'
bot = telebot.TeleBot(TOKEN)

API_URL = "https://flowise-production-a361.up.railway.app/api/v1/prediction/79bce751-b39e-48bd-a213-370bd01b966d"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    
    try:
        response = requests.post(API_URL, json={"question": user_message})
        result = response.json()
        reply_text = result.get("text", "عذراً، لم أتمكن من إيجاد إجابة في الملفات.")
    except Exception as e:
        reply_text = "حدث خطأ في الاتصال بنظام الذكاء الاصطناعي."
        
    bot.reply_to(message, reply_text)

print("البوت يعمل الآن...")
bot.infinity_polling()