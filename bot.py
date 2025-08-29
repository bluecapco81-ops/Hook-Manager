import disnake
from disnake.ext import commands
from flask import Flask, request, jsonify
import threading
import os
from dotenv import load_dotenv

# ------------------- Загружаем токен -------------------
load_dotenv("token.env")
TOKEN = os.getenv("DISCORD_TOKEN")

# ------------------- Настройки по умолчанию -------------------
DEFAULT_WEBHOOK_NAME = "NewWebhook"
BOT_EMOJI = "🤖"  # Эмодзи для embed

# ------------------- Бот -------------------
intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="h!", intents=intents)

# ------------------- Flask сервер -------------------
app = Flask(__name__)

@app.route("/new_webhook", methods=["POST"])
def new_webhook():
    data = request.json or {}
    user_id = int(data.get("user_id"))  # ID пользователя, который делает запрос

    # -------------- Проверка ключа ----------------------
    key = data.get("api_key")
     if key != API_KEY:
         return jsonify({"error": "Неверный ключ авторизации"}), 401

    # -------- Проверка прав администратора --------
    member = bot.get_guild(GUILD_ID).get_member(user_id)
    if not member or not member.guild_permissions.administrator:
        return jsonify({"error": "Только админы могут использовать эту команду"}), 403

    # -------- Дальше идёт твой существующий код --------
    channel_id = int(data.get("channel_id", 0))
    webhook_name = data.get("name", "NewWebhook")
    webhook_avatar = data.get("avatar")
    
    async def create_webhook():
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = bot.get_channel(DEFAULT_CHANNEL_RULES) or bot.get_channel(DEFAULT_CHANNEL_SYSTEM)
        if not channel:
            return {"error": "Канал не найден"}

        webhook = await channel.create_webhook(name=webhook_name, avatar=None)
        
        embed = disnake.Embed(
            title=f"{BOT_EMOJI} Новый вебхук создан!",
            color=EMBED_COLOR
        )
        embed.add_field(name="Название", value=webhook.name, inline=False)
        embed.add_field(name="URL", value=webhook.url, inline=False)
        embed.set_thumbnail(url=webhook.avatar.url if webhook.avatar else "")

        await channel.send(embed=embed)
        return {"name": webhook.name, "url": webhook.url}

    future = bot.loop.create_task(create_webhook())
    result = bot.loop.run_until_complete(future)
    return jsonify(result), 200

# ------------------- Поток Flask -------------------
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# ------------------- Запуск -------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)


