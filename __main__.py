import os
import hikari
import lightbulb
import aiohttp

from constants import CONSTANTS
from __init__ import GUILD_ID



# Create the main bot instance with all intents.
bot = lightbulb.BotApp(
    token=CONSTANTS.TOKEN,
    prefix=CONSTANTS.PREFIX,
    intents=hikari.Intents.ALL,
    help_slash_command = True,
    default_enabled_guilds= GUILD_ID,
)




    
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





if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.run()