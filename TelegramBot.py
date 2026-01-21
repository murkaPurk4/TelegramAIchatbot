import os
import asyncio
import random
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ================== ENVIRONMENT VARIABLES ==================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN environment variable not set")

if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY environment variable not set")

# ================== TELEGRAM BOT SETUP ==================

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ================== OPENROUTER SETUP ==================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Default model
current_model = "openai/gpt-3.5-turbo"

# ================== COMMANDS ==================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🤖 Привет! Я ИИ чат-бот через OpenRouter.\n"
        "Напиши мне сообщение 👇\n"
        "Используй /help для списка команд."
    )


@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📖 Доступные команды:\n"
        "/start – начать диалог\n"
        "/help – список команд\n"
        "/about – информация о боте\n"
        "/model <название> – сменить модель\n"
        "/dice – бросить кубик 🎲\n"
        "/joke – случайная шутка 😂\n"
        "/fact – интересный факт 🌍\n"
        "/quote – вдохновляющая цитата ✨\n"
        "/quiz – мини-викторина 🧠"
    )


@dp.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer(
        "ℹ️ Я Telegram-бот, использующий OpenRouter.ai.\n"
        "Поддерживаю GPT, Claude, Mistral и другие модели."
    )


@dp.message(Command("model"))
async def change_model(message: types.Message):
    global current_model
    args = message.text.split(maxsplit=1)

    if len(args) == 2:
        current_model = args[1]
        await message.answer(f"✅ Модель изменена на:\n{current_model}")
    else:
        await message.answer("⚠️ Использование:\n/model <название модели>")


@dp.message(Command("dice"))
async def roll_dice(message: types.Message):
    await message.answer(f"🎲 Ты выбросил: {random.randint(1, 6)}")


@dp.message(Command("joke"))
async def joke(message: types.Message):
    jokes = [
        "Почему программисты любят кофе? Потому что без него код не компилируется ☕",
        "Бот зашёл в бар… и сразу начал отвечать на все вопросы 🤖",
        "Ученые доказали: смех продлевает жизнь 😄"
    ]
    await message.answer(random.choice(jokes))


@dp.message(Command("fact"))
async def fact(message: types.Message):
    facts = [
        "🌍 В мире больше кур, чем людей.",
        "🧠 Мозг человека потребляет около 20% энергии тела.",
        "🚀 Первый человек в космосе — Юрий Гагарин."
    ]
    await message.answer(random.choice(facts))


@dp.message(Command("quote"))
async def quote(message: types.Message):
    quotes = [
        "✨ «Будь собой; все остальные роли уже заняты.» — Оскар Уайльд",
        "💡 «Успех — это движение от неудачи к неудаче без потери энтузиазма.» — Черчилль",
        "🔥 «Делай сегодня то, что другие не хотят.»"
    ]
    await message.answer(random.choice(quotes))


@dp.message(Command("quiz"))
async def quiz(message: types.Message):
    question = "🧩 Какая планета ближе всего к Солнцу?"
    options = ["Земля", "Меркурий", "Венера", "Марс"]
    text = question + "\n\n" + "\n".join(
        f"{i+1}. {opt}" for i, opt in enumerate(options)
    )
    await message.answer(text + "\n\nОтветь номером.")


# ================== MAIN CHAT ==================

@dp.message()
async def chat_with_ai(message: types.Message):
    try:
        payload = {
            "model": current_model,
            "messages": [
                {"role": "system", "content": "Ты дружелюбный Telegram чат-бот."},
                {"role": "user", "content": message.text}
            ],
            "max_tokens": 500
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        ai_text = data["choices"][0]["message"]["content"]
        await message.answer(ai_text)

    except Exception as e:
        print(e)
        await message.answer("❌ Ошибка при обращении к ИИ.")


# ================== START BOT ==================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
