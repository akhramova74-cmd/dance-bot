from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8612025075:AAF0f7DkQNeprK-6XzOeY1pyU9iHREuNtCk"
ADMIN_ID = 832430325
users = set()
feedbacks = []

welcome_text = """Всем привет! Сегодня был особенный вечер!
Вы были зрителем танцевального спектакля о любви, в котором слова заменились жестами, а музыкой стали биения сердец.
Цитата, которая стала лейтмотивом нашей постановки:
«Любовь - это начало всего. Она проявляется в каждом нашем действии, прикосновении, взгляде. Без любви невозможны творчество, дружба, искусство. Любовь начинается с нас! Только наполнив любовью себя, мы сможем отдать ее другим.»
Эта история разбита на главы. Дальше вы можете ознакомиться со смыслом, который вкладывался в каждую из них и сравнить с тем, как изначально поняли вы.
"""

titles = [
"Номер 1 — Рождение любви",
"Номер 2 — Я и мое отражение",
"Номер 3 — Первое прикосновение",
"Номер 4 — Игра теней",
"Номер 5 — Ритм",
"Номер 6 — Книга жизни",
"Номер 7 — Земля и небо",
"Номер 8 — Без слов",
"Номер 9 — Разбитые сердца",
"Номер 10 — Воскрешение",
"Номер 11 — Все ради любви"
]

descriptions = [
"""[Пробуждение любви внутри нас.]
Аллегорическая история рождения чувства – любви не как внешнего явление, а как внутреннего пробуждения и осознания. Путь от пустоты и одиночества к обретению внутренней гармонии и силы, которые исходят из самого сердца. Любовь, как фундаментальная энергия, которая есть в нас и которую нужно лишь раскрыть внутри нас. Зритель проходит путь вместе с артистом от отчаяния до надежды.""",

"""[Любовь к себе. Принятие себя и своего внутреннего Я.]
Визуализация внутреннего диалога человека с самим собой. История о борьбе и примирении со своим отражением, принятие своих сильных и слабых сторон.""",

"""[Проявление доверия и любви к окружающему миру и людям.]
В номере исследуется момент преодоления внутренних барьеров, страхов и недоверия к людям. Установление первой искренней связи с человеком и миром.""",

"""[Тема конфликтов и отношений между людьми.]
В номере исследуется динамика взаимоотношений через метафору света и тени.""",

"""[Любовь к определенной деятельности. Найти любовь в хаосе.]""",

"""[Поиск любви в прошлом опыте, знаниях и учениях.]""",

"""[Гармония и любовь в природе.]""",

"""[Проявление любви через бытовые вещи.]""",

"""[Любовь через боль, потерю и надежду.]""",

"""[Исцеление через любовь. Возрождение.]""",

"""[Все начинается с любви. Символ — дерево жизни.]"""
]

def menu_keyboard():
    keyboard = []
    for i in range(len(titles)):
        keyboard.append([InlineKeyboardButton(titles[i], callback_data=f"num_{i}")])
    return InlineKeyboardMarkup(keyboard)

def number_keyboard(index):
    keyboard = []

    if index < 10:
        keyboard.append([InlineKeyboardButton("➡️ Дальше", callback_data=f"num_{index+1}")])

    keyboard.append([InlineKeyboardButton("⬅️ Вернуться к списку", callback_data="menu")])
    keyboard.append([InlineKeyboardButton("💬 Оставить отзыв", callback_data="feedback")])

    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)

    await update.message.reply_text(welcome_text)
    await update.message.reply_text("Выберите номер:", reply_markup=menu_keyboard())

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.message.reply_text("Выберите номер:", reply_markup=menu_keyboard())

    elif query.data == "feedback":
        context.user_data["waiting_feedback"] = True
        await query.message.reply_text("Напишите ваш отзыв ❤️")

    elif query.data.startswith("num_"):
        index = int(query.data.split("_")[1])
        text = f"{titles[index]}\n\n{descriptions[index]}"
        await query.message.reply_text(text, reply_markup=number_keyboard(index))

async def receive_feedback(update: Update, context: ContextTypes.

DEFAULT_TYPE):

    if context.user_data.get("waiting_feedback"):

        user = update.message.from_user
        text = update.message.text

        feedbacks.append(text)

        message = f"""Новый отзыв

Имя: {user.first_name}
Username: @{user.username}

{text}
"""

        await context.bot.send_message(ADMIN_ID, message)

        await update.message.reply_text("Спасибо за отзыв ❤️")

        context.user_data["waiting_feedback"] = False

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("💬 Последние отзывы", callback_data="reviews")],
        [InlineKeyboardButton("📢 Рассылка", callback_data="broadcast")]
    ]

    await update.message.reply_text(
        "Админ панель",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    if query.data == "stats":

        await query.message.reply_text(
            f"Пользователей: {len(users)}\n"
            f"Отзывов: {len(feedbacks)}"
        )

    elif query.data == "reviews":

        if not feedbacks:
            await query.message.reply_text("Отзывов пока нет")
            return

        text = "\n\n".join(feedbacks[-5:])
        await query.message.reply_text(text)

    elif query.data == "broadcast":

        context.user_data["broadcast"] = True
        await query.message.reply_text("Напишите сообщение для рассылки")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if context.user_data.get("broadcast"):

        text = update.message.text

        for user_id in users:
            try:
                await context.bot.send_message(user_id, text)
            except:
                pass

        await update.message.reply_text("Рассылка отправлена")

        context.user_data["broadcast"] = False

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))

app.add_handler(CallbackQueryHandler(buttons, pattern="^(num_|menu|feedback)"))
app.add_handler(CallbackQueryHandler(admin_buttons))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_feedback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message))

app.run_polling()
