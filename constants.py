import os
import random
import lightbulb
import hikari
from __init__ import GUILD_ID

class CONSTANTS:
    PREFIX = "."
    TOKEN = "ODk2NDA3MDY2OTkyODM2NjQ4.G4aXwV.NTi9b33JR0fqa2ZxU_IFfPBHKKrEpuV3w1H9TQ"
    LAVALINK_PASSWORD = "youshallnotpass"
    HOST = "0.0.0.0:2333"
    INVISIBLE_LETTER = "‎"
    KEY = '1783319260d70f84da21868ce0fd6207'
    
    
    # Create the main bot instance with all intents.
    bot = lightbulb.BotApp(
        token=TOKEN,
        prefix=PREFIX,
        intents=hikari.Intents.ALL,
        help_slash_command = True,
        default_enabled_guilds= GUILD_ID,
)
    
class Lists:
    valorant_agents_sentinel = ["Cypher", "Killjoy", "Sage", "Chamber"]
    valorant_agents_initiator = ["Kay/o", "Skye", "Sova", "Breach", "Fade"]
    valorant_agents_duelist = ["Jett", "Phoenix", "Raze", "Reyna", "Yoru", "Neon"]
    valorant_agents_controller = ["Omen", "Brimstone", "Viper", "Astra"]
    
    valorant_agents = valorant_agents_sentinel + valorant_agents_initiator  + valorant_agents_duelist + valorant_agents_controller
    
    gutta = ["Tarek", "Danan", "Robin",
            "Thomas", "Daniel", "Minh",
            "Trym", "Ramtin", "Kashvin"]
    
    
    fmk = ["Billie Eilish","Yinka","Karina Skjold","Oddveig","Jezebel", "Caitlyn Jenner", "Greta Thunberg","Alexandra","Edle","Dara","Milly Bobby Brown","Rihanna",
    "Beyonce","Selena Gomez","Kendall Jenner","Gigi Hadid","Cara Delevingne","Annelies Marie Frank",
    "Malala Yousafzai","Kylie Jenner","Emma Ellingsen","Cardi B","En liten jente","Sultan"],
    ["Lil Wayne", "Elon Musk","Jeff Bezos","Abel Berhane","Sindre Simp","Hugh Jackman","Denzel Washington","Daniel (Secamore)",
    "Pete Davidson", "Connor McGregor","A$AP Rocky","Tyler The Creator", "Kendrick Lamar","Jack Black","Tarek", "Robin", "Daniel",
    "Minh", "Trym", "Thomas", "Ramtin","Ed Sheran", "Gud", "En liten gutt", "SixNine","Lionel Messi", "Christiano Ronaldo", "Mario", "Sonic",
    "Samuel Sewall","Sultan","XQC"]
    
    quote_tarek = ["Hva skal du ha minh.", "Pang sa det!", f"\*Sender {random.randint(0,444)} TikToker\*","Bare si det om du ikke vil, det går bra liksom.",
        "Hvaaaa meeeener du?!"]
    
    quote_danan = ["Hadde du giftet deg med faren din for 50kr?","Det er godt spørsmål","*Spytter*", "HADDE DU?", "Du vet faren? ja dette var faren til faren mann!", "GINI, MUNJAÑO!", "Hold kjeft...", "Jeg har sosial angst",
        "Blirre apex elle gutta?", "Tarek la meg logge på tindern din a",
        "Skal dere ha noe på banggood?", "Jeg skal på jokern, skal dere ha noe?", "JEG SITTER OG GJØR SKOLE!", "Mamma! {} sier hei, si hei tilbake.".format(random.choice(gutta)),
        "Jeg er deprimert"]
    # "Danan: {}\n{}: Ja hva skjer?\nDanan: ...".format(random.choice(gutta), random.choice(gutta)),
    
    quote_robin = ["Funka som kuk i kram snø! takk for tipset ;)","Kuk i kram snø :)","Hva faen? er klokken allerede så mye... Nei jeg går og legger meg", "NÆHhh...", "Jeg har tæsja jomfrudommen til mange jenter",
         "Gutta: Skal vi se \*skrekkfilm\*\nRobin: Ei jeg ville ikke se film egentlig uansett, men dere kan se da.","De spiller som en gjeng pakkiser"]
    
    quote_thomas = ["Jeg kan ikke jeg facetimer MAGOHMED", "MAGOOHMEDH<3",
         "Hva faen hold kjeft!", "Oi er klokken 24? jeg skal på jobb imorgen... klokken 16 :)"]
    
    quote_daniel = ["Hmm", "Greit gi meg 5 min", "Jeg skal bare dusje", "Greit, skal bare lage mat først",
        "Ṡ̸̡̡̨͎̦̬̬̯̱̩̦̰͖̙̳͙̤̓̆̈͂̾̒̒̅̂͌̈́̀̐̐͜͜͠e̶̡̨̧̮̬̩̠͔̬͚̥̦̪̻̩͖̗̝͎̘̺̦̖͒͑̉̾͛̂͆̽̉̈́͗̀̆̉̓͒̍͒̆͆̾̈́̿͘̚͜͠͠͠͝c̶̡̦͎̬̝̠̠͓͔͍͉̱̍̓̋̍̍͂̆̿̽̇͛̓̓͜a̸̧̨̧̤̹̰̫̯̥̬̟̹̺̥͇̜̞̜̹͎͎̳̯͂̄͛̄̍̋̀̓̓̔́̇̀̀̓̾͘͜͜͜͜͝͠ͅm̷̢̢̢̢̧̨̢̹̤̩͍̟͇͇̹̼̗̱̗̖̻̺̞͈̌̀̋͘ơ̶̡̧̜͇̮͈̠̦͈̗̠̽͊͛͌̽ŗ̵̛͔͇̹͓̭̙̰̟͙̻̗̳̬̣̰͎̱͍̋͛̌͂̓̔͛̈́̿̌̇̑̈́̀̉͆e̷̫̖̩̼̘͈͚̩̹̞̬̓̈́̾̀͛̂̇͂͘", "JeG MeNEr..."]
    
    quote_minh = ["JeG mENeR!", "Fuck jenter, jeg skal game!", "Greit, da stikker jeg da!", "Fuck det a.", "Hva skjer mine ***CENSORED***",
        "Nei vel da...", "Stream da!", "Del skjerm"]
    
    quote_trym = ["Neeeeiiiiii", "Hahahahhahahahahaha", "Trym: \*stille i flere\*\nNoen: Trym... Er du her?\nTrym: Ja heisann!",
        "Heisann hoppsann!"]
    
    quote_ramtin = ["Jeg prøvde å jacke til det men det gikk ikke.","Ey kiddo!"]
    
    quote_toan = ["https://www.youtube.com/watch?v=eAgrtY_qI6M"]
