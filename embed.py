from disnake import Embed, Colour
from flask import Flask, request, jsonify
import threading
import os
from disnake.ext import commands
import disnake

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route("/embed", methods=["POST"])
def embed_route():
    data = request.json or {}

    # Проверка API key
    if data.get("api_key") != API_KEY:
        e = Embed(
            title="API-Ключ не совпадает.",
            description="Вы не можете управлять чужим сервером",
            colour=Colour.red()
        )
        e.set_footer(text="Error: 401")
        return jsonify({"embed": str(e)}), 401

    user_id = int(data.get("user_id"))
    color_hex = data.get("color", "#0000FF")

    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(user_id)

    if not member or not member.guild_permissions.administrator:
        e = Embed(
            title="Вы не являетесь владельцем сервера",
            description="Чтобы сохранить безопасность этого сервера, вам нужно быть администратором, а если вы администратор но команда не работает, это значит что в настройках роли у вас нету права 'Администратор', сообщите об этом владельцу сервера, может быть они исправят это.",
            colour=Colour.red()
        )
        e.set_footer(text="Error: 403")
        return jsonify({"embed": str(e)}), 403

    # Всё ок, создаём embed с выбранным цветом
    try:
        if color_hex.startswith("#"):
            color_value = Colour(int(color_hex[1:], 16))
        else:
            color_value = Colour.blue()
    except:
        color_value = Colour.blue()

    async def send_embed():
        channel = bot.get_channel(CHANNEL_ID)
        e = Embed(
            title="Цвет embed-сообщений был успешно изменён!",
            colour=color_value
        )
        await channel.send(embed=e)

    future = bot.loop.create_task(send_embed())
    bot.loop.run_until_complete(future)
    return jsonify({"success": True}), 200


def run_flask():
    app.run(host="0.0.0.0", port=5000)

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="h!", intents=intents)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
