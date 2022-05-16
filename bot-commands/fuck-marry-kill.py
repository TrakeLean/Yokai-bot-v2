import lightbulb
import random
from constants import Lists

fmk_plugin = lightbulb.Plugin("Fuck-Marry-Kill")


@fmk_plugin.command
# @lightbulb.option("mode", "Pick a mode", choices = (Lists.valorant_agents))
@lightbulb.command("fmk", "All the fuck marry & kill commands")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def fmk_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

# Fuck marry kill game with names from a list stored in lists.py
@fmk_group.child
@lightbulb.command('random', 'Fuck, Marry & Kill (50/50 sjanse på kjønn)')
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def normal(ctx: lightbulb.Context) -> None:

    emoji_1 = ["🔞","👰","🔪"]

    FMK = random.choice(Lists.fmk)
    FMK2 = random.sample(FMK,3)

    await ctx.respond("Velkommen til Yokais **Fuck**, **Marry** & **Kill** spill!!!\n")
    for x in range(3):

        msg = ("**{}**").format(FMK2[x])

        respond = await ctx.respond(msg)
        msg = await respond.message()
        await msg.add_reaction(emoji_1[0])
        await msg.add_reaction(emoji_1[1])
        await msg.add_reaction(emoji_1[2])
        
# Fuck marry kill with 3 custom names
@fmk_group.child
@lightbulb.option("first", "pick 1. person")
@lightbulb.option("second", "pick 2. person")
@lightbulb.option("third", "pick 3. person")
@lightbulb.command('custom', 'Fuck, Marry & Kill CUSTOM (pick 3 people urself)')
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def custom(ctx: lightbulb.Context) -> None:

    emoji_1 = ["🔞","👰","🔪"]
    FMK = (ctx.options.third, ctx.options.second, ctx.options.first)
    
    await ctx.respond(f"Velkommen til **{ctx.user}**s **Fuck**, **Marry** & **Kill** spill!!!\n")
    for x in range(3):

        msg = ("**{}**").format(FMK[x])

        respond = await ctx.respond(msg)
        msg = await respond.message()
        await msg.add_reaction(emoji_1[0])
        await msg.add_reaction(emoji_1[1])
        await msg.add_reaction(emoji_1[2])


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fmk_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fmk_plugin)