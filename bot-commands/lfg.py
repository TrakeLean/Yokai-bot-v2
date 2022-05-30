import asyncio
import hikari
import lightbulb
import requests
import json
import concurrent
import os.path
from collections import defaultdict
from constants import CONSTANTS

API_KEY = CONSTANTS.KEY

region = 'EU'
    #region = 'any'
links = [f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any',
         f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any',
         f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any',
         f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any',
         f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any',
         ]
single_link = f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any'


def write(response):
    with open('bot-commands/lfg_dir/lfg.json', 'w') as json_file:
        json_file.write(response.text)

def do_scrap(link):
    region = 'EU'
    #region = 'any'
    #link = f'https://api.tracker.gg/api/v1/valorant/lfg/search?region{region}&playlist=competitive&skill=any'
    #api_link = f"http://api.scraperapi.com?api_key={API_KEY}&url={link}"
    payload = {'api_key': API_KEY, 'url': link, 'keep_headers': 'true'}
    head = {
        'authority': 'api.tracker.gg',
        'method': 'GET',
        'path': '/api/v1/valorant/lfg/search?region=any&playlist=competitive&skill=any',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'nb-NO,nb;q=0.9,no;q=0.8,en-US;q=0.7,en;q=0.6,ru;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': '__cflb=02DiuFQAkRrzD1P1mdkJhfdTc9AmTWwYkL5dhc6BaWz7E; X-Mapping-Server=s14; __cf_bm=eCW52EohIqvzfugOyKvNvo4spvffbOwnBy5YZBvh4gQ-1653777883-0-AYz5PvgOpqpL7/UCjWN7/dokINYUw/EV1D4T6eY5n9YecMF2lY0M4TWWdDyySEalQ3lzxua3IYwD9KUjzZtmFdM=',
        'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        }
    count = 0
    while True:
        response = requests.get('http://api.scraperapi.com', params=payload, headers=head)
        if response.status_code == 200:
            print(f'Success:',response.status_code)
            return response
        else:
            print(f'Failure:',response.status_code)
            count += ''
            if count >= 2:
                return None
            continue

def get_info():
    file = open('bot-commands/lfg_dir/lfg.json')
    data = json.load(file)['data']['entries']
    placement_ID = 0
    player_dictionary = defaultdict(list)
    for person in data:
        if person['bio']['statsJson'] != 'null':
            placement_ID += 1
            # Random valotrack account info
            userinfo = person['userInfo']
            
            userinfo_id = userinfo['userId']
            is_premium = userinfo['isPremium']
            is_verified = userinfo['isVerified']
            is_Influencer = userinfo['isInfluencer']
            region = userinfo['countryCode']
            is_suspicious = userinfo['isSuspicious']
            
            # Valorant info
            platform_info = person['platformInfo']
            
            valo_name = platform_info['platformUserHandle']
            avatar_url = platform_info['avatarUrl']
            
            # User bio/info
            bio = person['bio']
            
            has_mic = bio['hasMicrophone']
            playstyle = bio['playStyle']
            about = bio['about']
            
            # Valo account stats
            valo = person['profileSummary']
            rank_image = person['profileSummary']['featureStat']['metadata']['iconUrl']
            rank_tier = int(bio['statsJson'].split(' ')[1].replace(',', ''))
            rank = valo['featureStat']['value']
            winrate = valo['stats']['matchesWinPct']['value']
            kda = valo['stats']['kDRatio']['value']
            dmg_per_round = valo['stats']['damagePerRound']['value']

            # Get links to different medias
            social_accounts = userinfo['socialAccounts']
            socials = []
            for social in social_accounts:
                if social['platformUserHandle'] != None:
                    platform = social['platformSlug']
                    user_handle = social['platformUserHandle']
                    socials.append([platform, user_handle])
            #taken_keys = player_dictionary.keys()
            current_player = [
                            valo_name,
                            rank,
                            rank_tier,
                            winrate,
                            kda,
                            dmg_per_round,
                            region,
                            socials,
                            has_mic,
                            playstyle,
                            about,
                            is_verified,
                            is_premium,
                            is_Influencer,
                            is_suspicious,
                            avatar_url,
                            rank_image,
                            ]
            player_dictionary[rank_tier].append(current_player)
     
        # dictionary_items = player_dictionary.items()
        # sorted_dictionary = sorted(dictionary_items) 
        # return sorted_dictionary
    return player_dictionary

def all_in_one(links):
    write(do_scrap(links))

def read():
    with open('bot-commands/lfg_dir/lfg.json') as json_file:
        response = json.load(json_file)
        return response

def activate():
    # file_exists = os.path.exists('bot-commands/lfg_dir/lfg.json')
    # while not file_exists:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(all_in_one, links)
    # if file_exists:
    #     print('Did not scrape')

def by_winrate(rank):
    lowest = rank - 1
    highest = rank + 1
    sorted_by_winrate = {}
    for i in range(lowest,highest):
        # Open at current rank
        response = get_info()[i]
        # Get players within current rank
        for x in range(len(response)):
            current = response[x]
            name = current[0]
            rank = current[1]
            rank_tier = current[2]
            winrate = current[3]
            kda = current[4]
            dmg_pr_round = current[5]
            region = current[6]
            
            socials = current[7]
            
            has_mic = current[8]
            playstyle = current[9]
            about = current[10]
            
            is_verified = current[11]
            is_influencer = current[12]
            is_premium = current[13]
            is_suspicious = current[14]
            avatar_url = current[15]
            rank_image = current[16]
            sorted_by_winrate[winrate] = [name, rank, winrate, kda, dmg_pr_round, region, socials, has_mic, playstyle, about, is_verified, is_influencer, is_premium, is_suspicious, avatar_url, rank_image]
    dictionary_items = sorted_by_winrate.items()
    sorted_items = sorted(dictionary_items, reverse = True)
    return sorted_items

def rank_converter(rank):
    rank = rank.split()
    rank[0].lower()
    converted = 0
    if rank[0] == 'iron':
        converted = 2
    if rank[0] == 'bronze':
        converted = 5
    if rank[0] == 'silver':
        converted = 8
    if rank[0] == 'gold':
        converted = 11
    if rank[0] == 'platinum':
        converted = 14
    if rank[0] == 'diamond':
        converted = 17
    if rank[0] == 'immortal':
        converted = 20
    if rank[0] == 'radiant':
        converted = 23
    converted += int(rank[1])
    return converted

lfg_plugin = lightbulb.Plugin("Lfg")

@lfg_plugin.command
@lightbulb.command("lfg", "shhhh")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def lfg_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here




# Picks a random agent for you
@lfg_group.child
@lightbulb.option("rank", "what rank are you looking for")
@lightbulb.command("find", "find person")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def find_subcommand(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="People looking for group!")
    await ctx.respond(embed)
    rank_converted = rank_converter(ctx.options.rank)
    response = by_winrate(rank_converted)
    for i in range(len(response)):
        current = response[i][1]
        name = current[0]
        rank = current[1]
        winrate = current[2]
        kda = current[3]
        dmg_pr_round = current[4]
        region = current[5]
        socials = current[6]
        # has_mic = current[7]
        playstyle = current[8]
        about = current[9]  
        # Verified, influencer, premium, suspicious
        is_verified = current[10]
        is_influencer = current[11]
        is_premium = current[12]
        is_suspicious = current[13]
        profile_url = current[14]
        rank_image_url = current[15]
        bonus = ''
        if is_verified:
            bonus = f'{bonus} ✅'
        if is_influencer:
            bonus = f'{bonus} ⭐'
        if is_premium:
            bonus = f'{bonus} 💎'
        if is_suspicious:
            bonus = f'{bonus} 🤨'
        name = f'{name} {bonus}'

        embed = (hikari.Embed(title= f'{name} - {region}',
                            description = f'{about}')
                            #.set_footer('Verified: ✅ - Influencer: ⭐ - Premium: 💎 - Suspicious: 🤨')
                            )
        if profile_url != None:
            embed.set_thumbnail(f'{profile_url}')
        else:
            embed.set_thumbnail(f'{rank_image_url}')
        embed.add_field(
                        f'Rank: {rank}',
                        f'Winrate: {winrate}% - DamagePR: {dmg_pr_round} - KDA: {kda}%',
                        inline=False)
        for x in range(len(socials)):
            account = str(socials[x][0])
            link = None
            # if account == 'discord':
            #     link = f'https://discord.com/invite/{socials[x][1]}'
            if account == 'youtube':
                link = f'https://https://www.youtube.com/channel/{socials[x][1]}'
            if account == 'twitch':
                link = f'https://twitch.tv/{socials[x][1]}'
            if account   == 'twitter':
                link = f'https://twitter.com/{socials[x][1]}'

            embed.add_field(
                            f'{socials[x][0]}',
                            f'[{socials[x][1]}]({link})',
                            inline=True)
        if playstyle != None:
            embed.add_field(
                            f'Playstyle',
                            f'{playstyle}',
                            inline=False)
        await ctx.respond(embed)




# Picks a random agent for you
@lfg_group.child
@lightbulb.command("search", "search for people")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def search_subcommand(ctx: lightbulb.Context) -> None:
    await ctx.respond('Searching for people, wait a bit then try "/lfg find"')
    activate()













def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lfg_plugin)
    
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(lfg_plugin)