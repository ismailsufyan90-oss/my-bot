# كود بوت تليجرام بسيط
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="أهلاً بك! البوت يعمل بنجاح.")

if __name__ == '__main__':
    application = ApplicationBuilder().token('ضع_التوكن_هنا').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
