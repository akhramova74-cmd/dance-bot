import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

welcome_text = """Всем привет! Сегодня был особенный вечер!
Вы были зрителем танцевального спектакля о любви, в котором слова заменились жестами, а музыкой стали биения сердец.
Цитата, которая стала лейтмотивом нашей постановки:
«Любовь - это начало всего. Она проявляется в каждом нашем действии, прикосновении, взгляде. Без любви невозможны творчество, дружба, искусство. Любовь начинается с нас! Только наполнив любовью себя, мы сможем отдать ее другим.»
Эта история разбита на главы. Дальше вы можете ознакомиться со смыслом, который вкладывался в каждую из них и сравнить с тем, как изначально поняли вы.
"""

numbers = {
    1: """«Рождение любви»

[Пробуждение любви внутри нас.]
Аллегорическая история рождения чувства – любви не как внешнего явление, а как внутреннего пробуждения и осознания.""",

    2: """«Я и мое отражение»

[Любовь к себе. Принятие себя и своего внутреннего Я.]
История о борьбе и примирении со своим отражением.""",

    3: """«Первое прикосновение»

[Проявление доверия и любви к окружающему миру и людям.]
История о рождении доверия через прикосновение.""",

    4: """«Игра теней»

[Тема конфликтов и отношений между людьми.]
Любовь и борьба неразделимы.""",

    5: """«Ритм»

[Любовь к деятельности.]
Поиск призвания и внутреннего стержня.""",

    6: """«Книга жизни»

[Поиск любви в прошлом.]
Любовь — это процесс познания.""",

    7: """«Земля и небо»

[Гармония в природе.]
Любовь рождается в равновесии.""",

    8: """«Без слов»

[Любовь в бытовых жестах.]
Самый глубокий язык любви не требует слов.""",

    9: """«Разбитые сердца»

[Любовь через боль.]
Боль — доказательство любви.""",

    10: """«Воскрешение»

[Исцеление через любовь.]
Любовь возвращает к жизни.""",

    11: """«Все ради любви»

[Все начинается с любви.]
Любовь связывает прошлое, настоящее и будущее."""
}

def main_menu():
    keyboard = []
    for i in range(1, 12):
        keyboard.append(
            [InlineKeyboardButton(f"Номер {i}", callback_data=f"num_{i}")]
        )
    return InlineKeyboardMarkup(keyboard)

def number_menu(current):
    keyboard = [
        [InlineKeyboardButton("⬅ Вернуться к списку", callback_data="back")]
    ]

    if current < 11:
        keyboard.append(
            [InlineKeyboardButton("➡ Дальше", callback_data=f"num_{current+1}")]
        )

    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(welcome_text)
    await update.message.reply_text("Выберите номер:", reply_markup=main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "back":
        await query.message.reply_text("Выберите номер:", reply_markup=main_menu())

    elif data.startswith("num_"):
        number = int(data.split("_")[1])
        await query.message.reply_text(
            numbers[number],
            reply_markup=number_menu(number)
        )

if name == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    app.run_polling()
