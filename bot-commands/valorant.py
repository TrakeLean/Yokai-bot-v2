import hikari
import lightbulb
import os
import random
from lists import Lists


valorant_plugin = lightbulb.Plugin("Valorant")


@valorant_plugin.command
@lightbulb.command("valorant", "All the valorant commands")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def valorant_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here


# Picks a random agent for you
@valorant_group.child
@lightbulb.command("randomagent", "Yokai-Random-Agent: Let me pick your agent")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def randomagent_subcommand(ctx: lightbulb.Context) -> None:
    await ctx.respond(random.choice(Lists.valorant_agents))

# Picks agents for the people you specify
@valorant_group.child
@lightbulb.option("who", "Who's in the lobby?")
@lightbulb.command("team-picker", "Yokai-Team-Picker: Let me pick out your agents")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def teampicker_subcommand(ctx: lightbulb.Context) -> None:
    boys = ctx.options.who.split(" ")
    amount = len(boys)
    agents = random.sample(Lists.valorant_agents, amount)
    i = 0
    
    for boy in boys:
        await ctx.respond(boy.capitalize() + ", you're playing: " + agents[i] )
        i = i+1
        
# Pick who gets the play the chosen agent   
@valorant_group.child
@lightbulb.option("who", "Who want's to play the agent?")
@lightbulb.option("agent", "Which agent do you want to play?", choices = Lists.valorant_agents)
@lightbulb.command("agent-picker", "Yokai-Agent-Picker: Choose who gets to play the agent")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def agentpicker_subcommand(ctx: lightbulb.Context) -> None:
    winner = ctx.options.who.split(" ")
    winner = random.choice(winner)
    await ctx.respond(winner.capitalize() + " gets to play " + ctx.options.agent)
    




@valorant_group.child
@lightbulb.option("tag", "The tag of who you want to check eg. Lean")
@lightbulb.option("username", "The username of who you want to check eg. Trake")
@lightbulb.command("rank", "get valorant rank")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def rank_subcommand(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        f"https://api.henrikdev.xyz/valorant/v2/mmr/eu/{ctx.options.username}/{ctx.options.tag}"
    ) as response:
        res = await response.json()
        # {'currenttier': 18, 'currenttierpatched': 'Diamond 1', 'ranking_in_tier': 40, 'mmr_change_to_last_game': -19, 'elo': 1540, 'name': 'Trake', 'tag': 'Lean'}
        status = res["status"]

        # If we dont find a user
        if (status != 200):
            await ctx.respond(f"Couldn't find: {ctx.options.username}#{ctx.options.tag}")
        # If a user is found
        if (status == 200):
            # First stage
            info = res["data"]
            name = info["name"]
            tag = info["tag"]
            # Second stage
            current_info = info["current_data"]
            rank = current_info["currenttierpatched"]
            mmr_change_last_game = current_info["mmr_change_to_last_game"]
            mmr = current_info["elo"]
            random_image = random.choice(os.listdir("pictures/valorant_heads/"))

            if (mmr_change_last_game > 0):
                last_game = "Gained: "
            if (mmr_change_last_game == 0):
                last_game = "Draw: "
            if (mmr_change_last_game < 0):
                last_game = "Lost: "

            embed = hikari.Embed(title=name + "#" + tag,
                                description="Rank: " + rank +
                                " \n Elo: " + str(mmr) + "\n" +
                                last_game + str(abs(mmr_change_last_game)) + " rr last game",
                                colour="%06x" % random.randint(0, 0xFFFFFF))
            embed.set_thumbnail("pictures/valorant_heads/"+ random_image)
        
            if response.ok:
                await ctx.respond(embed)


    
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(valorant_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(valorant_plugin)