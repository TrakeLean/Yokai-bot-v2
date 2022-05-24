from dis import Instruction
import enum
import os
from posixpath import split
import hikari
import lightbulb
import asyncio
import random
import requests
from constants import CONSTANTS as C

fun_plugin = lightbulb.Plugin("Fun")


@fun_plugin.command
@lightbulb.command("fun", "All the entertainment commands you'll ever need")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def fun_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here


ANIMALS = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Red Panda": "🐼",
    "Koala": "🐨",
    "Bird": "🐦",
    "Racoon": "🦝",
    "Kangaroo": "🦘",
}


@fun_group.child
@lightbulb.command("animal", "Get a fact + picture of a cute animal")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def animal_subcommand(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in ANIMALS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=60,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        print("Command: Fun-Animal used by:", ctx.author)
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(description=res["fact"], colour=0x3B9DFF)
                embed.set_image(res["image"])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a {animal} for you!", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a {res.status} status :c", components=[]
                )


@fun_group.child
@lightbulb.command("meme", "Get a meme")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def meme_subcommand(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://meme-api.herokuapp.com/gimme"
    ) as response:
        res = await response.json()

        if response.ok and res["nsfw"] != True:
            link = res["postLink"]
            title = res["title"]
            img_url = res["url"]

            embed = hikari.Embed(colour=0x3B9DFF)
            embed.set_author(name=title, url=link)
            embed.set_image(img_url)
            print("Command: Fun-Meme used by:", ctx.author)
            await ctx.respond(embed)

        else:
            await ctx.respond(
                "Could not fetch a meme :c", flags=hikari.MessageFlag.EPHEMERAL
            )
            
@fun_group.child
@lightbulb.command("monkey", "Picture of a random monkey")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def monkey_subcommand(ctx: lightbulb.Context) -> None:
    spooky = random.randrange(0,1000)
    if (spooky <= 10):
        url = ("https://www.placemonkeys.com/1920/1080?random&spooky")
        
        embed = hikari.Embed(colour=0x3B9DFF)
        embed.set_image(url)

        await ctx.respond(embed)
    else:
        url = ("https://www.placemonkeys.com/1920/1080?random")
        
        embed = hikari.Embed(colour=0x3B9DFF)
        embed.set_image(url)
        print("Command: Fun-Monkey used by:", ctx.author)
        await ctx.respond(embed)
        
@fun_group.child
@lightbulb.option("website", "website link eg. google.com")
@lightbulb.command("logo", "Picture the fav-icon of a website")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def favicon_subcommand(ctx: lightbulb.Context) -> None:
    url = (f"https://icon.horse/icon/{ctx.options.website}")    
    embed = (hikari.Embed(
        #title =f"{ctx.options.website.capitalize()}'s favi-con",
        colour=0x3B9DFF)
        .set_image(url)
        .set_footer(f"{ctx.options.website.capitalize()}'s favi-con"))
    print("Command: fun-logo used by:", ctx.author)
    await ctx.respond(embed)

@fun_group.child
@lightbulb.option("name", "Write a name")
@lightbulb.command("name-predictor", "Let me predict a name")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def nameprediction_subcommand(ctx: lightbulb.Context) -> None:

    age = requests.get(f"https://api.agify.io?name={ctx.options.name}")
    age_info = age.json()
    genderize = requests.get(f"https://api.genderize.io?name={ctx.options.name}")
    genderize_info = genderize.json()
    nationality = requests.get(f"https://api.nationalize.io/?name={ctx.options.name}")
    nationality_info = nationality.json()
    
    person_name = age_info["name"]
    person_age = age_info["age"]
    person_gender = genderize_info["gender"]
    person_gender_probability = genderize_info["probability"]
    person_from = nationality_info["country"]
    
    embed = (hikari.Embed(
        title = f"Guessed info for {person_name}",
        colour=0x3B9DFF)
    .add_field(f"{person_name.capitalize()}",
        f"Age: {person_age}",
        inline=True)
    
    .add_field(f"{person_gender.capitalize()}",
        f"{person_gender_probability*100}%",
        inline=True)
    
    .add_field(f"{C.INVISIBLE_LETTER}",
        f"{C.INVISIBLE_LETTER}",
        inline=True)
    
    .add_field(f"{person_from[0]['country_id']}",
        f"{round(person_from[0]['probability']*100,2)}%",
        inline=True)
    .add_field(f"{person_from[1]['country_id']}",
        f"{round(person_from[1]['probability']*100,2)}%",
        inline=True)
    .add_field(f"{person_from[2]['country_id']}",
        f"{round(person_from[2]['probability']*100,2)}%",
        inline=True)
        )
    
    
    print("Command: fun-name-predictor used by:", ctx.author)
    await ctx.respond(embed)
            















@fun_group.child
@lightbulb.option("recipe", "Write the dish you want or \"random\"")
@lightbulb.command("recipe", "Let me suggest a dish")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def recipe_subcommand(ctx: lightbulb.Context) -> None:

    if ctx.options.recipe.lower() == "random":
        recipe  = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    else:
        custom_recipe = ctx.options.recipe
        custom_recipe.replace(" ","%20")
        recipe  = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={custom_recipe}")
    recipe_info = recipe.json()
    
    if recipe_info["meals"] == 0:
        await ctx.respond(f"Sorry {ctx.author},\n I could not find a recipe for {ctx.options.recipe} ")
    name = recipe_info["meals"][0]["strMeal"]
    picture = recipe_info["meals"][0]["strMealThumb"]
    video = recipe_info["meals"][0]["strYoutube"]
    is_from = recipe_info["meals"][0]["strArea"]
    catergory = recipe_info["meals"][0]["strCategory"]
    # Get ingredients and measurements
    ingredients = []
    measurements = []
    for x in range(1,21):
        current_ingredient = recipe_info["meals"][0][f"strIngredient{x}"]
        current_measure = recipe_info["meals"][0][f"strMeasure{x}"]
        if current_ingredient != "" or 0:
            ingredients.append(current_ingredient)
            measurements.append(current_measure)
        else:
            break
        
    # Get and split up instructions
    instructions = recipe_info["meals"][0]["strInstructions"]
    split_instructions = instructions.rsplit("\r\n")
    print(split_instructions)

    # Add index to instructions
    for count, instruction in enumerate(split_instructions):
        hit = 0 
        if count < 1:
            formated_instructions = f"{count+1} - {instruction}"
        else:
            if instruction == "":
                formated_instructions = f"{formated_instructions}\n"
                hit += 1
            else:
                formated_instructions = f"{formated_instructions}\n{count+1-hit} - {instruction}"

    embed = (hikari.Embed(
        title = f"Recipe ⇨ {name}",
        url = video,
        colour=0x3B9DFF)
             .set_image(picture)
             .set_footer(f"{is_from} {catergory.lower()}")
             )
    embed.add_field("Instructions",
        f"{formated_instructions}",
        inline=False)
    embed.add_field("Sorry",
        f"the instructions were to long",
        inline=False)
        
        
    for x in range(len(ingredients)):
        embed.add_field(f"{ingredients[x]}",
            f"{measurements[x]}",
            inline=True)
    
    
    
    print("Command: fun-recipe used by:", ctx.author, name)
    try:
        await ctx.respond(embed)
    except hikari.BadRequestError as error:
        await ctx.respond(error)
        












def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fun_plugin)