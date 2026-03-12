
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك (تم دمجه)
TOKEN = 8781113777:AAHVSjos-0xL5OiWXRmHzs4Bj0RlnbfehoU

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
    from telegram import ChatPermissions

async def promote_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. التأكد من أن الذي يستخدم الأمر هو (المالك) - يجب تحديد ID الخاص بك
    # استبدل 123456789 بـ ID حسابك الشخصي
    MY_ID = 123456789 
    if update.effective_user.id != MY_ID:
        await update.message.reply_text("هذا الأمر للمالك فقط!")
        return

    # 2. التأكد من وجود رد على رسالة
    if not update.message.reply_to_message:
        await update.message.reply_text("يرجى الرد على رسالة الشخص لرفعه.")
        return

    user_to_promote = update.message.reply_to_message.from_user
    
    # 3. منح الصلاحيات في تليجرام
    try:
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_to_promote.id,
            can_manage_chat=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_promote_members=False, # المدير لا يرفع مدراء آخرين
            can_invite_users=True,
            can_pin_messages=True
        )
        await update.message.reply_text(f"تم رفع {user_to_promote.first_name} إلى رتبة 'مدير'.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")
        async def lock_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # قفل إرسال الصور والفيديوهات
    await context.bot.set_chat_permissions(
        chat_id=update.effective_chat.id,
        permissions=ChatPermissions(can_send_media_messages=False)
    )
    await update.message.reply_text("تم قفل الوسائط في المجموعة.")
    from telegram.ext import MessageHandler, filters

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "سلام" in text or "أهلاً" in text:
        await update.message.reply_text("وعليكم السلام ورحمة الله وبركاته!")
    elif "صباح الخير" in text:
        await update.message.reply_text("صباح النور والسرور ☀️")
    elif "مساء الخير" in text:
        await update.message.reply_text("مساء الورد 🌙")

# في دالة التجهيز (Main) أضف هذا:
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def help_command(update, context):
    keyboard = [
        [InlineKeyboardButton("أوامر المشرفين", callback_data='admin')],
        [InlineKeyboardButton("إعدادات المجموعة", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('أهلاً! اختر قسماً للمساعدة:', reply_markup=reply_markup)
    import logging
import sqlite3
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد قاعدة البيانات (لحفظ الإعدادات)
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS groups 
                  (chat_id INTEGER PRIMARY KEY, locked_media BOOLEAN)''')
conn.commit()

# --- أوامر الإدارة ---

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("تم طرد العضو.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.reply_to_message.from_user.id
    # كتم العضو (منع إرسال الرسائل)
    await context.bot.restrict_chat_member(
        update.effective_chat.id, user_id, 
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("تم كتم العضو.")

# --- نظام القفل والفتح ---

async def lock_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # تحديث قاعدة البيانات
    cursor.execute("INSERT OR REPLACE INTO groups (chat_id, locked_media) VALUES (?, ?)", (chat_id, True))
    conn.commit()
    await context.bot.set_chat_permissions(chat_id, ChatPermissions(can_send_media_messages=False))
    await update.message.reply_text("تم قفل الوسائط.")

# --- نظام الرد التلقائي ---

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "سلام" in text:
        await update.message.reply_text("وعليكم السلام!")
    elif "صباح الخير" in text:
        await update.message.reply_text("صباح النور!")

# --- إعداد البوت ---

if __name__ == '__main__':
    TOKEN = 'YOUR_TOKEN_HERE'
    app = ApplicationBuilder().token(TOKEN).build()

    # الأوامر
    app.add_handler(CommandHandler('ban', ban))
    app.add_handler(CommandHandler('mute', mute))
    app.add_handler(CommandHandler('lock_media', lock_media))
    
    # الردود التلقائية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("البوت يعمل...")
    app.run_polling()
    # هذا القاموس يحتوي على الكلمات وردودها (يمكنك توسيعه ليصل لـ 100 أو أكثر)
auto_replies = {
    "سلام": "وعليكم السلام ورحمة الله وبركاته، أهلاً بك!",
    "صباح الخير": "صباح النور والسرور ☀️",
    "مساء الخير": "مساء الورد والياسمين 🌙",
    "رابط": "يمنع نشر الروابط في المجموعة، يرجى الالتزام بالقوانين.",
    "قوانين": "قوانين المجموعة هي: 1. الاحترام المتبادل. 2. يمنع السبام. 3. يمنع نشر الروابط.",
    # يمكنك إضافة المئات هنا...
}
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تجاهل رسائل البوت نفسه
    if update.message.from_user.is_bot:
        return

    user_text = update.message.text.lower()
    
    # البحث في القاموس
    for key, reply in auto_replies.items():
        if key in user_text:
            await update.message.reply_text(reply)
            break # يتوقف عند إيجاد أول كلمة مطابقة
            {
    "سلام": "وعليكم السلام",
    "شكرًا": "عفواً، نحن في الخدمة",
    "كيف الحال": "بخير، شكراً لسؤالك!"
            }
            import sqlite3
from telegram import Update
from telegram.ext import ContextTypes

# تهيئة قاعدة البيانات للتحذيرات
conn = sqlite3.connect('warns.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS warnings 
                  (user_id INTEGER, chat_id INTEGER, count INTEGER, PRIMARY KEY(user_id, chat_id))''')
conn.commit()

# حد التحذيرات قبل الطرد
MAX_WARNS = 3

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("يرجى الرد على رسالة العضو المراد تحذيره.")
        return

    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    # جلب عدد التحذيرات الحالي
    cursor.execute("SELECT count FROM warnings WHERE user_id=? AND chat_id=?", (user.id, chat_id))
    row = cursor.fetchone()
    count = (row[0] + 1) if row else 1

    # تحديث قاعدة البيانات
    cursor.execute("INSERT OR REPLACE INTO warnings (user_id, chat_id, count) VALUES (?, ?, ?)", (user.id, chat_id, count))
    conn.commit()

    if count >= MAX_WARNS:
        await context.bot.ban_chat_member(chat_id, user.id)
        await update.message.reply_text(f"وصل {user.first_name} إلى {MAX_WARNS} تحذيرات، تم طرده!")
    else:
        await update.message.reply_text(f"تحذير لـ {user.first_name}! (التحذير رقم {count}/{MAX_WARNS})")

async def reset_warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return
    user_id = update.message.reply_to_message.from_user.id
    cursor.execute("DELETE FROM warnings WHERE user_id=? AND chat_id=?", (user_id, update.effective_chat.id))
    conn.commit()
    await update.message.reply_text("تم تصفير تحذيرات العضو بنجاح.")
    app.add_handler(CommandHandler('warn', warn_user))
app.add_handler(CommandHandler('resetwarns', reset_warns))
app.add_handler(CommandHandler('warn', warn_user))
app.add_handler(CommandHandler('resetwarns', reset_warns))
async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # شرط: هل المستخدم هو المالك؟
    if not await is_owner(update):
        await update.message.reply_text("هذا الأمر للمالك فقط!")
        return
    
    # كود الرفع (Promote)...
    # (كما شرحنا في الكود السابق)
    async def restrict_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إغلاق كل شيء على الأعضاء العاديين
    await context.bot.set_chat_permissions(
        chat_id=update.effective_chat.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=False, # قفل الصور والفيديو
            can_send_other_messages=False, # قفل الروابط والملصقات
            can_add_web_page_previews=False
        )
    )
    await update.message.reply_text("تم إغلاق الوسائط والروابط على الأعضاء.")
    
    # ربط الأوامر
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ban', ban))
    
    # ربط حدث دخول الأعضاء
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    
    print("البوت يعمل الآن ومستعد لإدارة المجموعات...")
    application.run_polling()

