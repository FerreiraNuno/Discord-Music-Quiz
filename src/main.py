from play_music import play_song, stop, pause, resume
from server_class import Server

import os
import discord
from dotenv import load_dotenv

client = discord.Client()
guilds = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        guilds.update({guild: Server()})
        try:
            os.mkdir("../downloads/" + guild.name)
        except FileExistsError:
            pass



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        await play_song(message, guilds)

    if message.content.startswith('!stop'):
        await stop(message, guilds)

    if message.content.startswith("!pause"):
        await pause(message, guilds)

    if message.content.startswith('!resume'):
        await resume(message, guilds)

    if message.content.startswith('!test'):
        pass

if __name__ == "__main__" :
    load_dotenv()
    client.run(os.getenv("discord_token"))
