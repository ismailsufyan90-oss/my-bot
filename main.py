
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك (تم دمجه)
TOKEN = '8781113777:AAHVSjos-0xL5OiWXRmHzs4Bj0RlnbfehoU'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! أنا بوت إدارة المجموعات، جاهز للحفاظ على نظام الجروب.')

# أمر طرد (يحتاج أن يكون البوت مشرفاً)
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user.id)
        await update.message.reply_text(f'تم طرد العضو {user.first_name} بنجاح!')
    else:
        await update.message.reply_text('يرجى الرد على رسالة العضو المراد طرده.')

# ترحيب تلقائي عند دخول عضو جديد
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f'أهلاً بك يا {member.first_name} في مجموعتنا!')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ربط الأوامر
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ban', ban))
    
    # ربط حدث دخول الأعضاء
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    
    print("البوت يعمل الآن ومستعد لإدارة المجموعات...")
    application.run_polling()

