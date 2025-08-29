import disnake
from disnake.ext import commands
from flask import Flask, request, jsonify
import threading
import os
from dotenv import load_dotenv

# ------------------- Загружаем токен -------------------
load_dotenv("token.env")
TOKEN = os.getenv("DISCORD_TOKEN")

# ------------------- Бот -------------------
intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="h!", intents=intents)

# ------------------- Flask сервер -------------------
app = Flask(__name__)

@app.route("/delete_webhook", methods=["POST"])
def delete_webhook():
    data = request.json or {}
    user_id = int(data.get("user_id"))  # ID пользователя, который делает запрос

    # ---------------- Проверка ключа ----------------
    key = data.get("api_key")
    if key != API_KEY:
        return jsonify({"error":"Неверный ключ авторизации"}), 401

    # -------- Проверка прав администратора --------
    member = bot.get_guild(GUILD_ID).get_member(user_id)
    if not member or not member.guild_permissions.administrator:
        return jsonify({"error": "Только админы могут использовать эту команду"}), 403

    # -------- Дальше идёт твой существующий код --------
    webhook_id = data.get("id")
    webhook_url = data.get("url")

    async def remove_webhook():
        try:
            if webhook_url:
                webhook = await bot.fetch_webhook(int(webhook_url.split("/")[-2]))
            elif webhook_id:
                webhook = await bot.fetch_webhook(int(webhook_id))
            else:
                return {"error": "Не указан id или url вебхука"}

            await webhook.delete()
            return {"status": "success", "message": f"Вебхук {webhook.name} удалён"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    future = bot.loop.create_task(remove_webhook())
    result = bot.loop.run_until_complete(future)
    return jsonify(result), 200

# ------------------- Поток Flask -------------------
def run_flask():
    app.run(host="0.0.0.0", port=5001)  # Можно другой порт

# ------------------- Запуск -------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)

