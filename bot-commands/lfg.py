import asyncio
import hikari
import lightbulb
import requests
import json
import concurrent
import os.path
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
    player_dictionary = {}
    for person in data:
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
        
        rank_tier = bio['statsJson'].split(' ')[1].replace(',', '')
        rank = valo['featureStat']['value']
        winrate = valo['stats']['matchesWinPct']['value']
        kda = valo['stats']['kDRatio']['value']
        dmg_per_round = valo['stats']['damagePerRound']['value']

        # Get links to different medias
        social_accounts = userinfo['socialAccounts']
        socials = []
        for social in social_accounts:
            platform = social['platformSlug']
            user_handle = social['platformUserHandle']
            socials.append([platform, user_handle])
            
        player_dictionary[placement_ID-1] = [valo_name,
                                          rank, rank_tier,
                                          winrate, kda,
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
                                          ]
    return player_dictionary

def all_in_one(links):
    write(do_scrap(links))

def read():
    with open('bot-commands/lfg_dir/lfg.json') as json_file:
        response = json.load(json_file)
        return response

def activate():
    file_exists = os.path.exists('bot-commands/lfg_dir/lfg.json')
    while not file_exists:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(all_in_one, links)
    if file_exists:
        print('Done :)')







lfg_plugin = lightbulb.Plugin("Lfg")

@lfg_plugin.command
@lightbulb.command("lfg", "shhhh")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def lfg_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here





# Picks a random agent for you
@lfg_group.child
@lightbulb.command("lfg", "find person")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def lfg_subcommand(ctx: lightbulb.Context) -> None:
    activate()

    
    
    response = get_info()[0]





















def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lfg_plugin)
    
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(lfg_plugin)