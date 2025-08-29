import disnake
from disnake.ext import commands, tasks
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix="h!", intents=intents)

# ---------------- Статус при старте ----------------
@bot.event
async def on_ready():
    print(f"{bot.user} подключён!")
    # Выбираем статус: online, idle, dnd (не беспокоить)
    await bot.change_presence(status=disnake.Status.online)  # Можно сменить на idle или dnd

# ---------------- Команда для смены статуса ----------------
@bot.slash_command(description="Сменить статус бота")
@commands.is_owner()  # Только владелец бота
async def set_status(inter, status: str):
    status = status.lower()
    if status == "онлайн" or status == "online":
        await bot.change_presence(status=disnake.Status.online)
    elif status == "неактивен" or status == "idle":
        await bot.change_presence(status=disnake.Status.idle)
    elif status == "не беспокоить" or status == "dnd":
        await bot.change_presence(status=disnake.Status.dnd)
    else:
        await inter.send("Неверный статус! Используй: онлайн, неактивен, не беспокоить")
        return
    await inter.send(f"Статус бота изменён на: {status}")

bot.run(TOKEN)
