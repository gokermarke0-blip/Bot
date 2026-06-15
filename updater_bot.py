import telebot
import subprocess
import os

# ضع توكن البوت المدير هنا
BOT_TOKEN = "8678206908:AAGkjlS2Q7SHGmAESVbrbmp_GmS4Y_1CE3Q"
bot = telebot.TeleBot(BOT_TOKEN)

# معرفك الشخصي (عشان مفيش حد غيرك يقدر يحدث البوت)
ADMIN_ID = 7215277191 

@bot.message_handler(commands=['update'])
def update_system(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "⏳ جاري التحديث من GitHub...")
        try:
            # تنفيذ أمر التحديث
            result = subprocess.check_output(["git", "pull", "origin", "main"], stderr=subprocess.STDOUT)
            bot.reply_to(message, f"✅ تم سحب الملفات بنجاح:\n{result.decode('utf-8')}")
            
            # إعادة تشغيل البوت الأساسي باستخدام PM2
            subprocess.run(["pm2", "restart", "my_main_bot"])
            bot.reply_to(message, "🚀 تم إعادة تشغيل البوت بنجاح!")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث: {str(e)}")
    else:
        bot.reply_to(message, "🚫 لا تملك صلاحية التحديث.")

bot.polling()
