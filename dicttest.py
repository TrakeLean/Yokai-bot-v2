agent_dict = {
    "brimstone": {"name": "Brimstone", "role": "Controller", "quote": "my boyfriend is Robin"},
    "robin": {"name": "Robin", "role": "Controller", "quote": "I love Brimstone!"},
    "neon": {"name": "Neon", "role": "Duelist", "quote": "I envy the love and chemistry i see between Brimstone and Robin!"}
}

print("")
print("")
print("")
agent_list = ["brimstone", "robin", "neon"]
for agent in agent_list:
    curr_agent = agent_dict[agent]
    print("Agent: " + curr_agent["name"] + "\nRole: " + curr_agent["role"] + "\nQuote: " + curr_agent["quote"])
    print("")
