import os
os.system("pip install -r requirements.txt")
import hikari
import lightbulb
import aiohttp
from webserver import keep_alive

from constants import CONSTANTS




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
keep_alive()
bot.run()