import os
import hikari
import lightbulb
import asyncio
import random

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
            


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fun_plugin)