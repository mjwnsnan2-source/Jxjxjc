import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ====== إعداد التسجيل ======
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== توكن البوت (ضعه هنا مباشرة) ======
BOT_TOKEN = "8982682297:AAHd2zidqLceTPJQjNXBNSEUuVMeipZWqrw"  # 🔑 ضع التوكن الخاص بك بين علامتي التنصيص

# ====== بيانات العقيدة السلفية ======
AQAID = {
    "توحيد_الألوهية": "إفراد الله بالعبادة، فلا يُصرف أي نوع من العبادة لغير الله.",
    "توحيد_الربوبية": "إفراد الله بأفعاله من خلق ورزق وتدبير.",
    "توحيد_الأسماء_والصفات": "إثبات ما أثبته الله لنفسه في كتابه وسنة رسوله من الأسماء والصفات، بلا تحريف ولا تعطيل ولا تكييف ولا تمثيل.",
    "الإيمان_بالملائكة": "الإيمان بوجود الملائكة وبكل ما ورد في الكتاب والسنة من أسمائهم وأعمالهم.",
    "الإيمان_بالكتب": "الإيمان بجميع الكتب المنزلة، خاصة القرآن الكريم.",
    "الإيمان_بالرسل": "الإيمان بجميع الأنبياء والرسل، وخاتمهم محمد ﷺ.",
    "الإيمان_باليوم_الآخر": "الإيمان بكل ما ورد من أشراط الساعة والبعث والجنة والنار.",
    "الإيمان_بالقدر": "الإيمان بالقدر خيره وشره من الله تعالى.",
    "منهج_السلف": "فهم النصوص الشرعية كما فهمها الصحابة والتابعون، والبعد عن التأويلات العقلية المبتدعة.",
    "الوسطية": "التمسك بالوسطية في الاعتقاد والعبادة والسلوك، كما قال تعالى: {وَكَذَٰلِكَ جَعَلْنَاكُمْ أُمَّةً وَسَطًا}."
}

# ====== إعدادات القناة الإجبارية ======
FORCED_CHANNEL_USERNAME = "@xa_3g"
FORCED_CHANNEL_ID = -1001234567890  # ⚠️ استبدل بـ Chat ID الحقيقي

# ====== دالة التحقق من الاشتراك ======
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        user_id = update.effective_user.id
        chat_member = await context.bot.get_chat_member(chat_id=FORCED_CHANNEL_ID, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"خطأ في التحقق: {e}")
        return False

# ====== أزرار القائمة الرئيسية (مرتبة) ======
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📚 أبواب التوحيد", callback_data="توحيد")],
        [InlineKeyboardButton("🕊️ أركان الإيمان", callback_data="إيمان")],
        [InlineKeyboardButton("📖 منهج السلف", callback_data="سلف")],
        [InlineKeyboardButton("❓ سؤال عقدي", callback_data="سؤال")],
        [InlineKeyboardButton("📞 تواصل مع الشيخ", url="https://t.me/xa_3g")],
        [InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== أزرار الاشتراك الإجباري (مرتبة) ======
def get_subscription_buttons():
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة الآن", url="https://t.me/xa_3g")],
        [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")],
        [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data="retry_sub")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== أمر /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not await check_subscription(update, context):
        await update.message.reply_text(
            f"🌸 السلام عليكم {user.first_name}!\n\n"
            "🔴 **للوصول إلى محتوى البوت، يجب عليك الاشتراك في القناة الإجبارية أولاً.**\n\n"
            "📌 **خطوات الاشتراك:**\n"
            "1️⃣ اضغط على زر 'اشترك في القناة الآن'\n"
            "2️⃣ اشترك في القناة\n"
            "3️⃣ عد واضغط 'تحقق من الاشتراك'\n\n"
            "✨ **القناة:** @xa_3g",
            reply_markup=get_subscription_buttons(),
            parse_mode="Markdown"
        )
        return

    await update.message.reply_text(
        f"🌸 السلام عليكم ورحمة الله وبركاته {user.first_name}!\n\n"
        "📖 **بوت العقيدة السلفية**\n"
        "يهدف لنشر العلم الشرعي بمنهج السلف الصالح.\n\n"
        "🔹 **اختر أحد الأقسام أدناه:**",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# ====== معالج الأزرار ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ====== معالج الاشتراك ======
    if data == "check_sub":
        if await check_subscription(update, context):
            await query.edit_message_text(
                "✅ **تم التحقق من اشتراكك بنجاح!**\n\n"
                "📖 مرحبًا بك في بوت العقيدة السلفية.\n"
                "🔹 اختر أحد الأقسام أدناه:",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ **لم يتم العثور على اشتراكك.**\n\n"
                "📌 يرجى اتباع الخطوات التالية:\n"
                "1️⃣ اضغط على 'اشترك في القناة الآن'\n"
                "2️⃣ اشترك في القناة\n"
                "3️⃣ عد واضغط 'تحقق من الاشتراك'",
                reply_markup=get_subscription_buttons(),
                parse_mode="Markdown"
            )
        return

    if data == "retry_sub":
        await query.edit_message_text(
            "🔄 **إعادة المحاولة...**\n\n"
            "📌 يرجى الاشتراك في القناة أولاً ثم التحقق:",
            reply_markup=get_subscription_buttons(),
            parse_mode="Markdown"
        )
        return

    # ====== معالج "عن البوت" ======
    if data == "about":
        about_text = (
            "🌟 **عن البوت:**\n\n"
            "📖 هذا بوت تعليمي لنشر العقيدة السلفية الصحيحة.\n"
            "📚 المصادر: الكتاب والسنة بفهم سلف الأمة.\n\n"
            "👤 **المطور:** @xa_3g\n"
            "📢 **القناة الرسمية:** @xa_3g\n\n"
            "🛡️ **تنبيه:**\n"
            "هذا البوت للتعلم فقط، وليس بديلاً عن العلماء.\n"
            "للاستفسارات الجادة، راجع المشايخ الموثوقين."
        )
        await query.edit_message_text(
            about_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data == "back_to_menu":
        await query.edit_message_text(
            "📖 **القائمة الرئيسية:**\n\n"
            "🔹 اختر أحد الأقسام أدناه:",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
        return

    # ====== معالج محتوى العقيدة ======
    if data == "توحيد":
        text = "**📚 أبواب التوحيد:**\n\n"
        text += f"• **توحيد الألوهية:**\n{ AQAID['توحيد_الألوهية'] }\n\n"
        text += f"• **توحيد الربوبية:**\n{ AQAID['توحيد_الربوبية'] }\n\n"
        text += f"• **توحيد الأسماء والصفات:**\n{ AQAID['توحيد_الأسماء_والصفات'] }"
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "إيمان":
        text = "**🕊️ أركان الإيمان:**\n\n"
        text += f"• **الإيمان بالملائكة:**\n{ AQAID['الإيمان_بالملائكة'] }\n\n"
        text += f"• **الإيمان بالكتب:**\n{ AQAID['الإيمان_بالكتب'] }\n\n"
        text += f"• **الإيمان بالرسل:**\n{ AQAID['الإيمان_بالرسل'] }\n\n"
        text += f"• **الإيمان باليوم الآخر:**\n{ AQAID['الإيمان_باليوم_الآخر'] }\n\n"
        text += f"• **الإيمان بالقدر:**\n{ AQAID['الإيمان_بالقدر'] }"
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "سلف":
        text = "**📖 منهج السلف:**\n\n"
        text += f"• **منهج السلف:**\n{ AQAID['منهج_السلف'] }\n\n"
        text += f"• **الوسطية:**\n{ AQAID['الوسطية'] }"
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "سؤال":
        text = (
            "❓ **اسأل عن أي مسألة عقدية**\n\n"
            "📝 أرسل سؤالك وسأجيبك إن شاء الله بناءً على الكتاب والسنة بفهم سلف الأمة.\n\n"
            "📌 **أمثلة:**\n"
            "• ما حكم التوسل؟\n"
            "• ما معنى الإيمان؟\n"
            "• ما هي عقيدة أهل السنة؟"
        )
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
            ]),
            parse_mode="Markdown"
        )

# ====== معالج الأسئلة النصية ======
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        await update.message.reply_text(
            "🔴 **للوصول إلى هذه الخاصية، يجب الاشتراك في القناة الإجبارية.**\n\n"
            "📌 اشترك في @xa_3g ثم عد للبوت.",
            reply_markup=get_subscription_buttons(),
            parse_mode="Markdown"
        )
        return

    user_question = update.message.text
    response = (
        f"📩 **سؤالك:** {user_question}\n\n"
        "📝 **رد مبدئي:**\n"
        "هذا سؤال مهم، يُنصح بالرجوع إلى كبار العلماء الموثوقين مثل:\n"
        "• الشيخ ابن باز\n"
        "• الشيخ ابن عثيمين\n"
        "• الشيخ الألباني\n"
        "• الشيخ صالح الفوزان\n\n"
        "🔍 يمكنك البحث في **الموسوعة العقدية** أو **موقع الإسلام سؤال وجواب**.\n\n"
        "💡 هل تريد رابطًا لفتوى محددة؟ أرسل 'نعم'."
    )
    await update.message.reply_text(
        response,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_to_menu")]
        ]),
        parse_mode="Markdown"
    )

# ====== أوامر إضافية ======
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 **تعليمات البوت:**\n\n"
        "/start - عرض القائمة الرئيسية\n"
        "/about - عن البوت\n"
        "/help - هذه التعليمات\n\n"
        "📌 يمكنك أيضًا كتابة أي سؤال عقدي وسأجيبك."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🌟 **عن البوت:**\n\n"
        "📖 بوت تعليمي لنشر العقيدة السلفية.\n"
        "📚 المصادر: الكتاب والسنة بفهم السلف.\n\n"
        "📢 **قناتنا:** @xa_3g\n"
        "🛡️ للتعلم فقط، ليس بديلاً عن العلماء."
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# ====== التشغيل الرئيسي ======
def main():
    # 🔑 التوكن موجود في المتغير BOT_TOKEN أعلاه
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))

    # تشغيل البوت
    print("🤖 البوت يعمل مع خاصية الاشتراك الإجباري في @xa_3g...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()