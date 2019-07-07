# osrs xp api lookup for discord

import discord
import pandas as pd
import requests
from secrets import token

token = token()

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('!skill'):
        channel = message.channel

        # uses csv as skill labels
        read_path = 'osrs_skills.csv'
        skills = pd.read_csv(read_path, header=None)

        # reads users message and identifies variables
        lookups = list(message.content.split(' '))

        # allows for names with spaces
        if len(lookups) > 4:
            lookups[1] = (' '.join(lookups[1:-2]))
            del lookups[2:-2]

        # set name to lookup stats
        player_name = lookups[1]
        skill = lookups[2].title()
        category = lookups[3].lower()

        # get data from api listed
        api = ('http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=%s' % player_name)

        get_data = requests.get(api)

        player_stats = get_data.text.splitlines()

        # creates list from api text data
        stats = list(player_stats)
        stats_mat = []

        # creates a matrix for easier indexing
        for stat in stats[:24]:
            s = stat.split(',')
            stats_mat.append(s)

        # converts data into pd dataframe with column names and row names
        df = pd.DataFrame(stats_mat, columns=['rank', 'level', 'exp'])
        df['Skills'] = skills
        df_hiscores = df.set_index('Skills')

        # lookup code based on user input
        df_lookup = df_hiscores[category][skill]

        # creates message based on parameters set
        skill_message = '{}: {} {}: {}'.format(player_name, skill, category, df_lookup)
        await channel.send(skill_message)

        # info message
    elif message.content.startswith('!info'):
        channel = message.channel
        info_message = "\nUsage:\n!skill 'Player Name' 'Skill' 'Category (rank, level, exp)'\n\n"
        example = "Example:\n!skill PBRbeer Mining level"
        await channel.send(info_message + example)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
