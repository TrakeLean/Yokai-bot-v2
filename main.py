import os
import threading
import time
os.system("pip install -r requirements.txt")
os.system("/opt/virtualenvs/python3/bin/python3 -m pip install --upgrade pip")
import hikari
import lightbulb
import aiohttp
import webserver
from constants import CONSTANTS



def run_lavalink():
    os.system("java -jar Lavalink.jar")
threading.Thread(target=run_lavalink).start()
time.sleep(60)


# Create the main bot instance with all intents.
bot = CONSTANTS.bot

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()   

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

@bot.listen()
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.strip() == ".ping":
        await event.message.respond(
            f"Latency: {bot.heartbeat_latency*1000:.2f}ms"
        )

# Load all extensions.
bot.load_extensions_from("./bot-commands")

if __name__ == "main":
    if os.name != "nt":
        import uvloop

        uvloop.install()
webserver.keep_alive()
try:
    bot.run()
except:
    os.system("kill 1")