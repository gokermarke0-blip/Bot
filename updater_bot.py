import telebot
import subprocess
import os

# اقرأ التوكن من متغير بيئة بدل أن يكون مكتوباً في الملف
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)

# معرف المسؤول. افتراضيًا تركت القيم القديمة كقيمة احتياطية لكن من الأفضل ضبطه عبر المتغيرات.
ADMIN_ID = int(os.environ.get("ADMIN_ID", "7215277191"))

# اسم عملية PM2 التي يُعاد تشغيلها بعد التحديث
MAIN_PM2_NAME = os.environ.get("MAIN_PM2_NAME", "my_main_bot")

@bot.message_handler(commands=['update'])
def update_system(message):
    # استخدم from_user.id عندما تكون الرسالة من محادثة خاصة
    user_id = message.from_user.id if getattr(message, 'from_user', None) else message.chat.id
    if user_id == ADMIN_ID:
        bot.reply_to(message, "⏳ جاري التحديث من GitHub...")
        try:
            # تنفيذ أمر التحديث
            result = subprocess.check_output(["git", "pull", "origin", "main"], stderr=subprocess.STDOUT)
            bot.reply_to(message, f"✅ تم سحب الملفات بنجاح:\n{result.decode('utf-8')}")

            # إعادة تشغيل البوت الأساسي باستخدام PM2
            subprocess.run(["pm2", "restart", MAIN_PM2_NAME], check=False)
            bot.reply_to(message, "🚀 تم إعادة تشغيل البوت بنجاح!")
        except subprocess.CalledProcessError as e:
            # عرض مخرجات الخطأ من git
            output = e.output.decode('utf-8') if getattr(e, 'output', None) else str(e)
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث:\n{output}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث: {str(e)}")
    else:
        bot.reply_to(message, "🚫 لا تملك صلاحية التحديث.")

if __name__ == '__main__':
    # تشغيل البوت
    bot.polling()
