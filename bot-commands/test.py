import lightbulb
import hikari
import asyncio
from hikari.api import ActionRowBuilder
import typing as t


test_plugin = lightbulb.Plugin("Test")


@test_plugin.command
@lightbulb.command("test", "test", )
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def test_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here


# Mapping of color names to hex literal and a fact about the color.
COLORS: t.Mapping[str, t.Tuple[int, str]] = {
    "1": (0xFF0000,"Due to it's long wavelength, red is the first color a baby sees!",),
    "2": (0x00FF00,"Plants green color help them use photosynthesis!",),
    "3": (0x0000FF,"Globally, blue is the most common favorite color!",),
    "4": (0xFFA500, "The color orange is named after its fruity counterpart, the orange!"),
    "5": (0xA020F0,"Purple is the hardest color for human eyes to distinguish!",),
    "6": (0xFFFF00,"Taxi's and school buses are yellow because it's so easy to see!",),
    "7": (0x000000, "Black is a color which results from the absence of visible light!"),
    "8": (0xFFFFFF, "White objects fully reflect and scatter all visible light!"),
    "9": (0xFFC0CB, "Pink :)"),
}


async def generate_rows(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    """Generate 3 action rows with 3 buttons each."""

    # This will hold our action rows of buttons. The limit
    # imposed by Discord is 5 rows with 5 buttons each. We
    # will not use that many here, however.
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    # Here we iterate len(COLORS) times.
    for i in range(len(COLORS)):
        if i % 3 == 0 and i != 0:
            # If i is evenly divided by 4, and not 0 we want to
            # append the first row to rows and build the second
            # action row. (Gives a more even button layout)
            rows.append(row)
            row = bot.rest.build_action_row()

        # Extract the current color from the mapping and assign
        # to this label var for later.
        label = list(COLORS)[i]

        # We use an enclosing scope here so that we can easily chain
        # method calls of the action row.
        (
            # Adding the buttons into the action row.
            row.add_button(
                # Gray button style, see also PRIMARY, and DANGER.
                hikari.ButtonStyle.PRIMARY,
                # Set the buttons custom ID to the label.
                label,
            )
            # Set the actual label.
            .set_label(label)
            # Finally add the button to the container.
            .add_to_container()
        )

    # Append the second action row to rows after the for loop.
    rows.append(row)

    # Return the action rows from the function.
    return rows


async def handle_responses(
    bot: lightbulb.BotApp,
    author: hikari.User,
    message: hikari.Message,
) -> None:
    """Watches for events, and handles responding to them."""

    # Now we need to check if the user who ran the command interacts
    # with our buttons, we stop watching after 120 seconds (2 mins) of
    # inactivity.
    with bot.stream(hikari.InteractionCreateEvent, 120).filter(
        # Here we filter out events we don't care about.
        lambda e: (
            # A component interaction is a button interaction.
            isinstance(e.interaction, hikari.ComponentInteraction)
            # Make sure the command author hit the button.
            and e.interaction.user == author
            # Make sure the button was attached to our message.
            and e.interaction.message == message
        )
    ) as stream:
        async for event in stream:
            # If we made it through the filter, the user has clicked
            # one of our buttons, so we grab the custom ID.
            cid = event.interaction.custom_id

            # Create new embed with info on the color they selected
            embed = hikari.Embed(
                # The color name.
                title=cid,
                # The hex literal we stored earlier.
                color=COLORS[cid][0],
                # The fact about the color.
                description=COLORS[cid][1],
            )

            # If we haven't responded to the interaction yet, we
            # need to create the initial response. Otherwise, we
            # need to edit the initial response.
            try:
                # NOTE: We don't have to add the buttons again as they
                # are already on the message. So we don't have to
                # pass components here. If we wanted to update the
                # buttons we would pass a new list of action rows.
                await event.interaction.create_initial_response(
                    # The response type is required when creating
                    # the initial response. We use MESSAGE_UPDATE
                    # because we are updating a message we previously
                    # sent. NOTE: even though the message was already
                    # sent, this is still the **INITIAL RESPONSE** to
                    # the interaction event (button click).
                    hikari.ResponseType.MESSAGE_UPDATE,
                    embed=embed,
                )
            except hikari.NotFoundError:
                # This error is raised if we have already sent the
                # initial response. Notice no response type is needed
                # here, so we just edit the initial response with the
                # new embed.
                await event.interaction.edit_initial_response(
                    embed=embed,
                )

    # Once were back outside the stream loop, it's been 2 minutes since
    # the last interaction and it's time now to remove the buttons from
    # the message to prevent further interaction.
    await message.edit(
        # Set components to an empty list to get rid of them.
        components=[]
    )

# Create the message command.
@test_group.child()
@lightbulb.command("rgb", "Get facts on different colors!")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def rgb_subcommand(ctx: lightbulb.Context) -> None:
    """Get facts on different colors!"""

    # Generate the action rows.
    rows = await generate_rows(ctx.bot)

    # Send the initial response with our action rows, and save the
    # message for handling interaction responses.
    response = await ctx.respond(
        hikari.Embed(title="Pick a color"),
        components=rows,
    )
    message = await response.message()

    # Handle interaction responses to the initial message.
    await handle_responses(ctx.bot, ctx.author, message)

    
    
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(test_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(test_plugin)