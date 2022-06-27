import random

class Agent:
  def __init__(self, name, role, image):
    self.name = name
    self.role = role
    self.image = image
    
class Team:
    def __init__(self):
      self.controller = random.choice(valorant_agents_controller)
      self.sentinel = random.choice(valorant_agents_sentinel)
      self.duelist = random.choice(valorant_agents_duelist)
      self.initiator = random.choice(valorant_agents_initiator)
      self.random_role = random.choice(valorant_agents_random)
      self.random = random.choice(self.random_role)
      self.list = set((self.controller, self.sentinel, self.duelist, self.initiator, self.random))
      while len(self.list) < 5:
        self.random_role = random.choice(valorant_agents_random)
        self.random = random.choice(self.random_role)
        self.list = set((self.controller, self.sentinel, self.duelist, self.initiator, self.random))



# Controller
brimstone = Agent("Brimstone", "Controller", "pictures/valorant_heads/Brimstone_icon.png")
omen = Agent("Omen", "Controller", "pictures/valorant_heads/Omen_icon.png")
viper = Agent("Viper", "Controller", "pictures/valorant_heads/Viper_icon.png")
astra = Agent("Astra", "Controller", "pictures/valorant_heads/Astra_icon.png")

# Sentinel
cypher = Agent("Cypher", "Sentinel", "pictures/valorant_heads/Cypher_icon.png")
killjoy = Agent("Killjoy", "Sentinel", "pictures/valorant_heads/Killjoy_icon.png")
sage = Agent("Sage", "Sentinel", "pictures/valorant_heads/Sage_icon.png")
chamber = Agent("Chamber", "Sentinel", "pictures/valorant_heads/Chamber_icon.png")

# Duelist
jett = Agent("Jett", "Duelist", "pictures/valorant_heads/Jett_icon.png")
phoenix = Agent("Phoenix", "Duelist", "pictures/valorant_heads/Phoenix_icon.png")
raze = Agent("Raze", "Duelist", "pictures/valorant_heads/Raze_icon.png")
reyna = Agent("Reyna", "Duelist", "pictures/valorant_heads/Reyna_icon.png")
yoru = Agent("Yoru", "Duelist", "pictures/valorant_heads/Yoru_icon.png")
neon = Agent("Neon", "Duelist", "pictures/valorant_heads/Neon_icon.png")

# Initiator
skye = Agent("Skye", "Initiator", "pictures/valorant_heads/Skye_icon.png")
sova = Agent("Sova", "Initiator", "pictures/valorant_heads/Sova_icon.png")
kayo = Agent("Kay/o", "Initiator", "pictures/valorant_heads/KAYO_icon.png")
breach = Agent("Breach", "Initiator", "pictures/valorant_heads/Breach_icon.png")
fade = Agent("Fade", "Initiator", "pictures/valorant_heads/Fade_icon.png")

agent_list = [cypher, killjoy, sage, chamber,
              kayo, skye, sova, breach, fade,
              jett, phoenix, raze, reyna, yoru,
              neon, omen, brimstone, viper, astra]

valorant_agents_sentinel = [cypher, killjoy, sage, chamber]
valorant_agents_initiator = [kayo, skye, sova, breach, fade]
valorant_agents_duelist = [jett, phoenix, raze, reyna, yoru, neon]
valorant_agents_controller = [omen, brimstone, viper, astra]
valorant_agents_random = [valorant_agents_sentinel, valorant_agents_initiator, valorant_agents_duelist, valorant_agents_controller]

agent_team = Team()