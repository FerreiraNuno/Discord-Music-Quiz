from play_music import play_song, stop, pause, resume

import yt_dlp
import os
import discord
from dotenv import load_dotenv

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.boolean = False

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        await play_song(message)

    if message.content.startswith('!stop'):
        await stop(message)

    if message.content.startswith("!pause"):
        await pause(message)

    if message.content.startswith('!resume'):
        await resume(message)


if __name__ == "__main__" :
    load_dotenv()
    client.run(os.getenv("discord_token"))
