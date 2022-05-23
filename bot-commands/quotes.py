import os
import hikari
import lightbulb
from constants import Lists
import asyncio
import random

quote_plugin = lightbulb.Plugin("Quote")


@quote_plugin.command
@lightbulb.command("quote", "Get a quote from the boys", )
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def quote_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here


        
@quote_group.child
@lightbulb.command("kanye", "Random Kanye quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def kanye_subcommand(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://api.kanye.rest/"
    ) as response:
        res = await response.json()

        if response.ok:
            print("Command: Quote-Kanye used by:", ctx.author)
            await ctx.respond(res["quote"] + " - Kanye West")

# Random tarek quote           
@quote_group.child
@lightbulb.command("tarek", "Random tarek quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def tarek_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_tarek)
    print("Command: Quote-Tarek used by:", ctx.author)
    await ctx.respond(random_quote + " - Tarek")
    
# Random danan quote           
@quote_group.child
@lightbulb.command("danan", "Random danan quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def danan_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_danan)
    print("Command: Quote-Danan used by:", ctx.author)
    await ctx.respond(random_quote + " - Danan")
    
# Random robin quote           
@quote_group.child
@lightbulb.command("robin", "Random robin quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def robin_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_robin)
    print("Command: Quote-Robin used by:", ctx.author)
    await ctx.respond(random_quote + " - Robin")
    
# Random thomas quote           
@quote_group.child
@lightbulb.command("thomas", "Random thomas quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def thomas_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_thomas)
    print("Command: Quote-Thomas used by:", ctx.author)
    await ctx.respond(random_quote + " - Thomas")
    
# Random daniel quote           
@quote_group.child
@lightbulb.command("daniel", "Random daniel quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def daniel_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_daniel)
    print("Command: Quote-Daniel used by:", ctx.author)
    await ctx.respond(random_quote + " - Daniel")
    
# Random minh quote           
@quote_group.child
@lightbulb.command("minh", "Random minh quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def minh_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_minh)
    print("Command: Quote-Minh used by:", ctx.author)
    await ctx.respond(random_quote + " - Minh")
    
# Random trym quote           
@quote_group.child
@lightbulb.command("trym", "Random trym quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def trym_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_trym)
    print("Command: Quote-Trym used by:", ctx.author)
    await ctx.respond(random_quote + " - Trym")
    
# Random ramtin quote           
@quote_group.child
@lightbulb.command("ramtin", "Random ramtin quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def ramtin_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_ramtin)
    print("Command: Quote-Ramtin used by:", ctx.author)
    await ctx.respond(random_quote + " - Ramtin")
    
# Random toan quote           
@quote_group.child
@lightbulb.command("toan", "Random toan quote")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def toan_subcommand(ctx: lightbulb.Context) -> None:
    random_quote = random.choice(Lists.quote_toan)
    print("Command: Quote-Toan used by:", ctx.author)
    await ctx.respond(random_quote + " - Toan")
    


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(quote_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(quote_plugin)