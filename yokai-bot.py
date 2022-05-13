import hikari
import lightbulb
import random

bot = lightbulb.BotApp(
    token="ODk2NDA3MDY2OTkyODM2NjQ4.GrIceq.sJDuhckAWsKhQfKN8sTcK58YJX455urXa0MUWs", 
    default_enabled_guilds=(896414680266993706, 645004208973545502),
    help_slash_command = True,
    prefix = ".",
    intents=hikari.Intents.ALL
)


@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Ping: {bot.heartbeat_latency*1000:.2f}ms")

# @bot.listen(hikari.StartedEvent)
# async def on_started(event):
#     print("Yokai Yokai Yoaki BOT!")
    
# bot.command
# #@lightbulb.add_cooldown(5.0, 1, lightbulb.UserBucket)
# @lightbulb.option("Text", "The thing to say.")
# @lightbulb.command("say", "Make the bot say something")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def say(ctx: lightbulb.SlashContext):
#     await ctx.respond(ctx.options.text)


# @bot.command
# @lightbulb.command("ping", "say pong!")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def ping(ctx):
#     await ctx.respond("Pong!")
    
# @bot.command
# @lightbulb.command("group", "This is a group")
# @lightbulb.implements(lightbulb.SlashCommandGroup)
# async def my_group(ctx):
#     pass

# @my_group.child
# @lightbulb.command("subcommand", "This is a subcommand")
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def subcommand(ctx):
#     await ctx.respond("I am a subcommand!")


valorant_agents = ("Reyna", "Fade", "Sage",
                   "Brimstone", "Skye", "Phoenix",
                   "Jett", "Viper", "Astra",
                   "Omen", "Killjoy", "Breach",
                   "Raze", "Yoru", "Cypher", "Sova",
                   "Kayo")
gutta = ("Tarek", "Danan", "Robin",
         "Thomas", "Daniel", "Minh",
         "Trym", "Ramtin", "Kashvin")
    
@bot.command
@lightbulb.option("who", "Who want's to play the agent?")
@lightbulb.option("agent", "Which agent do you want to play?", choices = valorant_agents)
@lightbulb.command("yap", "Yokai-Agent-Picker: Choose who gets to play the agent")
@lightbulb.implements(lightbulb.SlashCommand)
async def yap(ctx):
    winner = ctx.options.who.split(" ")
    winner = random.choice(winner)
    await ctx.respond(winner.capitalize() + " gets to play " + ctx.options.agent)
    
@bot.command
@lightbulb.option("who", "Who's in the lobby?")
@lightbulb.command("ytp", "Yokai-Team-Picker: Let me pick out your agents")
@lightbulb.implements(lightbulb.SlashCommand)
async def ytp(ctx):
    boys = ctx.options.who.split(" ")
    amount = len(boys)
    agents = random.sample(valorant_agents, amount)
    i = 0
    
    for boy in boys:
        await ctx.respond(boy + ", you're playing: " + agents[i] )
        i = i+1
        
@bot.command
@lightbulb.command("randomagent", "Yokai-Team-Picker: Let me pick out your agents")
@lightbulb.implements(lightbulb.SlashCommand)
async def ytp(ctx):
    await ctx.respond(random.choice(valorant_agents))
    
    
    
    
@bot.command
@lightbulb.command('fmk', 'Fuck, Marry & Kill (50/50 sjanse på kjønn)')
@lightbulb.implements(lightbulb.PrefixCommand)
async def fmk(ctx):

    emoji_1 = ["🔞","👰","🔪"]

    fmk = ["Billie Eilish","Yinka","Karina Skjold","Oddveig","Jezebel", "Caitlyn Jenner", "Greta Thunberg","Alexandra","Edle","Dara","Milly Bobby Brown","Rihanna",
    "Beyonce","Selena Gomez","Kendall Jenner","Gigi Hadid","Cara Delevingne","Annelies Marie Frank",
    "Malala Yousafzai","Kylie Jenner","Emma Ellingsen","Cardi B","En liten jente","Sultan"],
    ["Lil Wayne", "Elon Musk","Jeff Bezos","Abel Berhane","Sindre Simp","Hugh Jackman","Denzel Washington","Daniel (Secamore)",
    "Pete Davidson", "Connor McGregor","A$AP Rocky","Tyler The Creator", "Kendrick Lamar","Jack Black","Tarek", "Robin", "Daniel",
    "Minh", "Trym", "Thomas", "Ramtin","Ed Sheran", "Gud", "En liten gutt", "SixNine","Lionel Messi", "Christiano Ronaldo", "Mario", "Sonic",
    "Samuel Sewall","Sultan","XQC"]
    FMK = random.choice(fmk)
    FMK2 = random.sample(FMK,3)

    #**{} - {} - {}**").format(FMK2[0],FMK2[1],FMK2[2])
    await ctx.respond("Velkommen til Yokais **Fuck**, **Marry** & **Kill** spill!!!\n")
    for x in range(3):

        msg = ("**{}**").format(FMK2[x])

        respond = await ctx.respond(msg)
        msg = await respond.message()
        await msg.add_reaction(emoji_1[0])
        await msg.add_reaction(emoji_1[1])
        await msg.add_reaction(emoji_1[2])
   
   
# @bot.command
# @lightbulb.option("who", "Who's in the lobby?")
# @lightbulb.command("fmkc", "This is a group")
# @lightbulb.implements(lightbulb.SlashCommandGroup)
# async def my_group(ctx):
#     FMK = ctx.options.who.split(" ")
#     pass  

     
@bot.command
@lightbulb.option("who", "pick 3 people")
@lightbulb.command('fmkc', 'Fuck, Marry & Kill CUSTOM (pick 3 people urself)')
@lightbulb.implements(lightbulb.SlashCommand)
async def fmkc(ctx):

    emoji_1 = ["🔞","👰","🔪"]
    FMK = ctx.options.who.split(" ")

    await ctx.respond("Velkommen til Yokais **Fuck**, **Marry** & **Kill** spill!!!\n")
    for x in range(3):

        msg = ("**{}**").format(FMK[x])

        respond = await ctx.respond(msg)
        msg = await respond.message()
        await msg.add_reaction(emoji_1[0])
        await msg.add_reaction(emoji_1[1])
        await msg.add_reaction(emoji_1[2])





 



bot.run()