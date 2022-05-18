import hikari
import lightbulb
from constants import CONSTANTS, Lists



bot = CONSTANTS.bot
ttt_plugin = lightbulb.Plugin("ttt")


@ttt_plugin.command
@lightbulb.command("ttt", "ttt")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def ttt_group(ctx: lightbulb.Context) -> None:
    await ctx.respond("Hei")





def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ttt_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ttt_plugin)