import telebot
import subprocess
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['update'])
def update_system(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "⏳ جاري التحديث من GitHub...")
        try:
            result = subprocess.check_output(["git", "pull", "origin", "main"], stderr=subprocess.STDOUT)
            bot.reply_to(message, f"✅ تم سحب الملفات بنجاح:\n{result.decode('utf-8')}")
            subprocess.run(["pm2", "restart", "my_main_bot"])
            bot.reply_to(message, "🚀 تم إعادة تشغيل البوت بنجاح!")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث: {str(e)}")
    else:
        bot.reply_to(message, "🚫 لا تملك صلاحية التحديث.")

bot.polling()
