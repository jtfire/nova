import discord
import asyncio
import logging
import json
import os
from discord.ext import commands
#import pdb; pdb.set_trace()

'#logging code'
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
@client.event
async def on_message(message):
    if message.content.startswith("do you work"):
        await client.send_message(message.channel, "yes!!")
    elif message.content.startswith("report"):
        if not os.path.isfile('tournament_results.txt'):
            tournament_results_list = []
        else:
            with open("tournament_results.txt", 'r+') as tournament_results_file:
                tournament_results_list = json.load(tournament_results_file)
        tournament_results_list.append(message.content[7:])
        with open("tournament_result.txt", 'a') as tournament_results_file:
            json.dump(tournament_results_list, tournament_results_file, indent=True)

#command to add the captain role
    elif message.content.startswith("i'm a captain"):
        role = discord.utils.get(message.server.roles, name='Team Captain')
        await client.add_roles(message.author, role)
        await client.send_message(message.channel, "Done, make you can see all the channels you need to. if you can't ping a mod.")
 
#command for team roles
    elif message.content.startswith('''i'm on'''):
        name = message.content[7:]
        role = discord.utils.get(message.server.roles, name=name)
        if role == 'None':
            await client.create_role(message.channel.server, name=name, mentionable=True)
            await client.send_message(message.channel, "a team role has been made for you")
            add_role = discord.utils.get(message.server.roles, name=name)
            await client.add_roles(message.author, add_role)
            await client.send_message(message.channel.server, "you should have your role now")
        elif role != "None":
            await client.add_roles(message.author, role)
            await client.send_message(message.channel, "you should be on {0} now".format(role.name))
        else:
            client.send_message(message.channel, "for some reason i don't have that role and i didn't make it. you should probbly tell one of the mods so they can help you")

       

client.run('')
