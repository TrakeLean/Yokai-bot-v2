import asyncio
import hikari
import lightbulb
import os
import random
from constants import CONSTANTS, Lists
from datetime import datetime
from valorant_agents import Agent as Agent
from valorant_agents import Team as Team
from hikari.api import ActionRowBuilder
import typing as t

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
    
    get_team = Team()
    curr_agent = random.sample(list(get_team.list), 1)
    curr_agent = curr_agent[0]

        
    embed = hikari.Embed(title=ctx.user.username,
                        description="You got\n" + curr_agent.name + "\n" + curr_agent.role,
                        colour="%06x" % random.randint(0, 0xFFFFFF))
    embed.set_thumbnail(curr_agent.image)
    print("Command: Valorant-Random-Agent used by:", ctx.author)
    await ctx.respond(embed)










# Picks agents for the people you specify
@valorant_group.child
@lightbulb.option("who", "Who's in the lobby?")
@lightbulb.command("team-picker", "Yokai-Team-Picker: Let me pick out your agents")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def teampicker_subcommand(ctx: lightbulb.Context) -> None:
    boys = ctx.options.who.split(" ")
    get_team = Team()
    team_list = random.sample(list(get_team.list), 5)
    i = 0
    embed = hikari.Embed(title="Valorant-Team-Picker")
    await ctx.respond(embed)
    for boy in boys:
        curr_agent = team_list[i]
        
        if (boy.lower() == "robin" and curr_agent.name.lower() == "brimstone"):
            curr_agent.image = "pictures/valorant_heads/brimdinHD.png"
            


        embed = hikari.Embed(title=boy.capitalize(),
                            description="You're playing \n" + curr_agent.name + "\n" + curr_agent.role,
                            colour="%06x" % random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(curr_agent.image)
        #await ctx.respond(boy.capitalize() + ", you're playing: " + agents[i] )
        print("Command: Valorant-Team-Picker used by:", ctx.author)
        await ctx.respond(embed)
        i+=1
 
 
 
 
 
 
        
# Pick who gets the play the chosen agent   
@valorant_group.child
@lightbulb.option("who", "Who want's to play the agent?")
@lightbulb.option("agent", "Which agent do you want to play?", choices = Lists.valorant_agents)
@lightbulb.command("agent-duel", "Yokai-Agent-Duel: Choose who gets to play the agent")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def agentduel_subcommand(ctx: lightbulb.Context) -> None:
    winner = ctx.options.who.split(" ")
    winner = random.choice(winner)
    team_list = Team()

    embed = hikari.Embed(title=winner.capitalize(),
                        description="You're playing \n" + ctx.options.agent,
                        colour="%06x" % random.randint(0, 0xFFFFFF))
    #embed.set_thumbnail(team_list.list(ctx.options.agent.image))
    print("Command: Valorant-Agent-Duel used by:", ctx.author)
    await ctx.respond(embed)
    




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
                                " \n Elo: " + str(mmr) + "  -  " +"RR: "+ str(mmr % 100) + "\n" +
                                last_game + str(abs(mmr_change_last_game)) + " rr last game",
                                colour="%06x" % random.randint(0, 0xFFFFFF))
            embed.set_thumbnail("pictures/valorant_heads/"+ random_image)
            #embed.add_field("Bot?","asd",inline=True,)

            if response.ok:
                print("Command: Valorant-Agent-Duel used by:", ctx.author)
                await ctx.respond(embed)





Arrows = ["🢀","🢃","🢂"]

async def generate_rows(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    # Here we iterate len(COLORS) times.
    for i in range(len(Arrows)):

        label = list(Arrows)[i]
        (
            # Adding the buttons into the action row.
            row.add_button(
                hikari.ButtonStyle.SUCCESS,
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


async def handle_responses(bot: CONSTANTS.bot,author: hikari.User,message: hikari.Message,res,match,name) -> None:
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
            if cid == Arrows[0]:
                match -= 1
                if match < 0:
                    match = 0
            if cid == Arrows[1]:
                match = 0
            if cid == Arrows[2]:
                match += 1
                if match > 4:
                    match = 4
            # if cid == Arrows[3]:
            #     embed = get_match_embed()
            else:                
                # Create new embed with info on the arrow they selected
                embed = get_embed(res, match, name)
            try:
                await event.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_UPDATE,
                    embed=embed,
                )
            except hikari.NotFoundError:
                await event.interaction.edit_initial_response(
                    embed=embed,
                )
    await message.edit(
        components=[]
    )



@valorant_group.child
@lightbulb.option("tag", "The tag of who you want to check eg. Lean")
@lightbulb.option("username", "The username of who you want to check eg. Trake")
@lightbulb.command("match-history", "get valorant rank")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def matchhistory_subcommand(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
    f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{ctx.options.username}/{ctx.options.tag}?filter=Competitive") as response:
        res = await response.json()
        rows = await generate_rows(ctx.bot)
        status = res["status"]
        # If we dont find a user
        if (status != 200):
            await ctx.respond(f"Couldn't find: {ctx.options.username}#{ctx.options.tag}")
        # If a user is found
        if (status == 200):
            name = ctx.options.username
            match = 0
            embed = get_embed(res, match, name)

            print("Command: Valorant-Match-History used by:", ctx.author, datetime.now())

            response = await ctx.respond(embed,components=rows,)
            message = await response.message()

            # Handle interaction responses to the initial message.
            await handle_responses(ctx.bot, ctx.author, message, res, match, name)
            await message.delete()

def get_embed(res, match, name):

            # Access data
            data = res["data"]

            # List of info in data
            data_list = data[match]
            # Access metadata
            metadata = data_list["metadata"]
            # Get game info
            player_map = metadata["map"]
            player_mode = metadata["mode"]
            player_server = metadata["cluster"]
            player_game_length = str(round(((metadata["game_length"])/60)/1000))+" min"
            player_time_played = metadata["game_start_patched"]
            # Find out if player was red or blue
            all_players = data_list["players"]["all_players"]
            all_score = []
            for player in all_players:
                all_score.append(player["stats"]["score"])
                curr_player = player["name"]
                if curr_player.lower() == name.lower():
                    player_team = player["team"].lower()
                    player_agent = player["character"]
                    player_name = player["name"]
                    player_tag = player["tag"]
                    player_rank = player["currenttier_patched"]
                    player_level = player["level"]
                    # Player KDA
                    player_kills = str(player["stats"]["kills"])
                    player_deaths = str(player["stats"]["deaths"])
                    player_assists = str(player["stats"]["assists"])
                    player_kda = f"{player_kills}/{player_deaths}/{player_assists}"
                    # Player hit stats
                    player_headshots = player["stats"]["headshots"]
                    player_bodyshots = player["stats"]["bodyshots"]
                    player_legshots = player["stats"]["legshots"]
                    player_headshot_acc =  str(round((player_headshots / (player_headshots + player_bodyshots + player_legshots)) * 100, 2))+ "%"
                    # Player abilities used
                    player_ability_c = player["ability_casts"]["c_cast"]
                    player_ability_q = player["ability_casts"]["q_cast"]
                    player_ability_e = player["ability_casts"]["e_cast"]
                    player_ability_x = player["ability_casts"]["x_cast"]
                    # Friendly fire
                    player_ff_taken = player["behavior"]["friendly_fire"]["incoming"]
                    player_ff_given = player["behavior"]["friendly_fire"]["outgoing"]
                    # Afk rounds
                    player_afk = player["behavior"]["afk_rounds"]
                    # Player score
                    player_total_score = player["stats"]["score"]
                    # Player damage
                    player_damage_given = player["damage_made"]
                    player_damage_received = player["damage_received"]
                    # Agent
                    assets_agent_bust = player["assets"]["agent"]["bust"]
                    assets_agent_killfeed = player["assets"]["agent"]["killfeed"]
                    # Card 
                    assets_card_wide = player["assets"]["card"]["wide"]
            # Get round data
            team = data_list["teams"][player_team]
            team_win_check = team["has_won"]
            if team_win_check == False:
                team_win = "Lost"
                win_color = "#FF0000"
            else:
                team_win = "Won"      
                win_color = "#00FF00"
            team_rounds_won = team["rounds_won"]
            team_rounds_lost = team["rounds_lost"]

            # Get average score
            player_average_score = round(player_total_score / (team_rounds_won + team_rounds_lost))
            for rank in os.listdir("pictures/ranks"):
                if (player_rank.replace(" ", "_") == rank.rsplit( ".", 1 )[ 0 ]):
                    player_rank_image = rank
                    
            # Get players on enemy team
            if player_team == "red":
                enemy_team = "blue"
            else:
                enemy_team = "red"
            enemy_players = data_list["players"][enemy_team]
            enemy_players_list = []
            enemy_players_score = []
            for players in enemy_players:
                enemy_players_list.append(players["name"])
                enemy_players_score.append(round((players["stats"]["score"])/ (team_rounds_won + team_rounds_lost)))
                
            # Get players on team
            team_players = data_list["players"][player_team]
            team_players_list = []
            team_players_score = []
            
            for players in team_players:
                team_players_list.append(players["name"])
                team_players_score.append(round((players["stats"]["score"])/ (team_rounds_won + team_rounds_lost)))
            
            # Team dict
            team_dict = dict(zip(team_players_list, team_players_score))
            team_dict = dict(sorted(team_dict.items(), key=lambda item: item[1], reverse=True))
            team_players_list = list(team_dict)
            # Enemy dict
            enemy_dict = dict(zip(enemy_players_list, enemy_players_score))
            enemy_dict =  dict(sorted(enemy_dict.items(), key=lambda item: item[1], reverse=True))
            enemy_players_list = list(enemy_dict)
            
            

            
            
            mvp = ""    
            # Check if team MVP (in average)
            if all(x <= player_average_score for x in team_players_score):
                mvp = "☆"
            # Check if match MVP (in total)
            if all(x <= player_total_score for x in all_score):
                mvp = "★"


            
            # Check leaderboard MVP
            if team_dict[team_players_list[0]] > enemy_dict[enemy_players_list[0]]:
                team_bonus = "★"
                enemy_bonus = "☆"
            else:
                enemy_bonus = "★"
                team_bonus = "☆"
                    
                    
            # Player damage
            player_damage_given /= (team_rounds_won + team_rounds_lost)
            player_damage_received /=  (team_rounds_won + team_rounds_lost)
            # Fix match typing
            if match >= 1:
                match_print = f"{match+1} Games ago."
            if match == 0:
                match_print = f"Last game"

            embed = (hikari.Embed(title= f"{player_name}#{player_tag} - Level: {player_level} - {match_print}",
                                #description= player_map +" - "+ team_win + "\n" + player_kda + " KDA",
                                description = f"{player_mode} - played: {player_game_length}",
                                colour=win_color)
                                #timestamp=datetime.now().astimezone(),)
                                .set_thumbnail(f"pictures/ranks/{player_rank_image}")
                                .set_image(assets_card_wide)
                                .add_field(
                                    f" {player_map} ⇨ {team_win} ⇨ {team_rounds_won}-{team_rounds_lost}",
                                    f"{player_kda} KDA - {player_agent}",
                                    inline=False)
                                .add_field(
                                    name =f"Team - {team_rounds_won}",
                                    value = f"{team_dict[team_players_list[0]]} - {team_players_list[0]}{team_bonus}\n{team_dict[team_players_list[1]]} - {team_players_list[1]}\n{team_dict[team_players_list[2]]} - {team_players_list[2]}\n{team_dict[team_players_list[3]]} - {team_players_list[3]}\n{team_dict[team_players_list[4]]} - {team_players_list[4]}",
                                    inline=True)
                                .add_field(
                                    name =f"Enemy - {team_rounds_lost}",
                                    value = f"{enemy_dict[enemy_players_list[0]]} - {enemy_players_list[0]}{enemy_bonus}\n{enemy_dict[enemy_players_list[1]]} - {enemy_players_list[1]}\n{enemy_dict[enemy_players_list[2]]} - {enemy_players_list[2]}\n{enemy_dict[enemy_players_list[3]]} - {enemy_players_list[3]}\n{enemy_dict[enemy_players_list[4]]} - {enemy_players_list[4]}",
                                    inline=True)
                                .add_field(
                                    "Score Average",
                                    "Player score: " + str(player_average_score) + mvp +"\n"+
                                    "Damage given: "+ str(round(player_damage_given)) +"\n"+
                                    "Damage taken: "+ str(round(player_damage_received)) +"\n"+
                                    "Headshot: "+ player_headshot_acc,
                                    inline=False)
                                .add_field(
                                    "Abilities used",
                                    f"C: {player_ability_c} \nQ: {player_ability_q} \nE: {player_ability_e} \nX: {player_ability_x} \n",
                                    inline=True)
                                .add_field(
                                    "Hits",
                                    f"Headshot: {player_headshots} \nBodyshot: {player_bodyshots} \nLegshot: {player_legshots}",
                                    inline=True)
                                .set_footer(f"{player_time_played} - {player_server}📡" )
                                .add_field(
                                    "Friendly fire",
                                    f"\nGiven: {player_ff_given}\n Taken: {player_ff_taken}\nAfk: {player_afk}",
                                    inline=True)
                                .set_footer(f"{player_time_played} - {player_server}📡" )
            )
            return embed







# def get_match_embed(res,match,name):

#             # Access data
#             data = res["data"]

#             # List of info in data
#             data_list = data[match]
#             # Access metadata
#             metadata = data_list["metadata"]
#             # Get game info
#             player_map = metadata["map"]
#             player_mode = metadata["mode"]
#             # Find out if player was red or blue
#             all_players = data_list["players"]["all_players"]
#             all_score = []
#             for player in all_players:
#                 all_score.append(player["stats"]["score"])
#                 curr_player = player["name"]
#                 if curr_player.lower() == name.lower():
#                     player_team = player["team"].lower()
#                     player_name = player["name"]
#                     player_tag = player["tag"]
#                 # player_agent
#                 player_agent = player["character"]
#                 # Player KDA
#                 player_kills = str(player["stats"]["kills"])
#                 player_deaths = str(player["stats"]["deaths"])
#                 player_assists = str(player["stats"]["assists"])
#                 player_kda = f"{player_kills}/{player_deaths}/{player_assists}"
#                 # Player hit stats
#                 player_headshots = player["stats"]["headshots"]
#                 player_bodyshots = player["stats"]["bodyshots"]
#                 player_legshots = player["stats"]["legshots"]
#                 player_headshot_acc =  str(round((player_headshots / (player_headshots + player_bodyshots + player_legshots)) * 100, 2))+ "%"
#                 # Player abilities used
#                 player_ability_x = player["ability_casts"]["x_cast"]
#                 # Friendly fire
#                 player_ff_taken = player["behavior"]["friendly_fire"]["incoming"]
#                 player_ff_given = player["behavior"]["friendly_fire"]["outgoing"]
#                 # Afk rounds
#                 player_afk = player["behavior"]["afk_rounds"]
#                 # Player score
#                 player_total_score = player["stats"]["score"]
#                 # Player damage
#                 player_damage_given = player["damage_made"]
#                 player_damage_received = player["damage_received"]
#                 # Agent
#                 assets_agent_bust = player["assets"]["agent"]["bust"]
#                 assets_agent_killfeed = player["assets"]["agent"]["killfeed"]
#                 # Card 
#                 assets_card_wide = player["assets"]["card"]["wide"]
#             # Get round data
#             team = data_list["teams"][player_team]
#             team_win_check = team["has_won"]
#             if team_win_check == False:
#                 team_win = "Lost"
#                 win_color = "#FF0000"
#             else:
#                 team_win = "Won"      
#                 win_color = "#00FF00"
#             team_rounds_won = team["rounds_won"]
#             team_rounds_lost = team["rounds_lost"]

#             # Get average score
#             player_average_score = round(player_total_score / (team_rounds_won + team_rounds_lost))
              
#             # Get players on enemy team
#             if player_team == "red":
#                 enemy_team = "blue"
#             else:
#                 enemy_team = "red"
#             enemy_players = data_list["players"][enemy_team]
#             enemy_players_list = []
#             enemy_players_score = []
#             for players in enemy_players:
#                 enemy_players_list.append(players["name"])
#                 enemy_players_score.append(round((players["stats"]["score"])/ (team_rounds_won + team_rounds_lost)))
                
#             # Get players on team
#             team_players = data_list["players"][player_team]
#             team_players_list = []
#             team_players_score = []
            
#             for players in team_players:
#                 team_players_list.append(players["name"])
#                 team_players_score.append(round((players["stats"]["score"])/ (team_rounds_won + team_rounds_lost)))
            
#             # Team dict
#             team_dict = dict(zip(team_players_list, team_players_score))
#             team_dict = dict(sorted(team_dict.items(), key=lambda item: item[1], reverse=True))
#             team_players_list = list(team_dict)
#             # Enemy dict
#             enemy_dict = dict(zip(enemy_players_list, enemy_players_score))
#             enemy_dict =  dict(sorted(enemy_dict.items(), key=lambda item: item[1], reverse=True))
#             enemy_players_list = list(enemy_dict)
            
            

            
            
#             mvp = ""    
#             # Check if team MVP (in average)
#             if all(x <= player_average_score for x in team_players_score):
#                 mvp = "☆"
#             # Check if match MVP (in total)
#             if all(x <= player_total_score for x in all_score):
#                 mvp = "★"


            
#             # Check leaderboard MVP
#             if team_dict[team_players_list[0]] > enemy_dict[enemy_players_list[0]]:
#                 team_bonus = "★"
#                 enemy_bonus = "☆"
#             else:
#                 enemy_bonus = "★"
#                 team_bonus = "☆"
    




















































@valorant_group.child
@lightbulb.option("tag", "The tag of who you want to check eg. Lean")
@lightbulb.option("username", "The username of who you want to check eg. Trake")
@lightbulb.command("latest", "get valorant rank")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def latest_subcommand(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
    f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{ctx.options.username}/{ctx.options.tag}?filter=Competitive") as response:
        res = await response.json()
        status = res["status"]
        # If we dont find a user
        if (status != 200):
            await ctx.respond(f"Couldn't find: {ctx.options.username}#{ctx.options.tag}")
        # If a user is found
        if (status == 200):
            name = ctx.options.username
            # Access data
            data = res["data"]
            history = []
            color_tracker = 0
            # List of info in data
            for x in range(5):
                data_list = data[x]
                all_players = data_list["players"]["all_players"]
                for player in all_players:
                    curr_player = player["name"]
                    if curr_player.lower() == name.lower():
                        player_team = player["team"].lower()
                        player_name = player["name"]
                        player_tag = player["tag"]
                        assets_card_small = player["assets"]["card"]["small"]
                        # Get round data
                        team = data_list["teams"][player_team]
                        team_win_check = team["has_won"]
                        if team_win_check == False:
                            history.append("🟥 ")
                        else:
                            history.append("🟩 ")
                            color_tracker += 1
                        if color_tracker < 3:
                            embed_color = "#FF0000"
                        else:
                            embed_color = "#00FF00"
                            
            embed = (hikari.Embed(title= f"{player_name}#{player_tag}",
                                  description=f"{history[0]}{history[1]}{history[2]}{history[3]}{history[4]}",
                                  color=embed_color)
                     .set_thumbnail(assets_card_small))
            message = await ctx.respond(embed)
            print("Command: Valorant-latest used by:", ctx.author, datetime.now())
            await asyncio.sleep(60)
            await message.delete()



















    
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(valorant_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(valorant_plugin)