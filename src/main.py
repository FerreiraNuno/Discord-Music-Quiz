import yt_dlp
import os
import discord
from dotenv import load_dotenv

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        if len(message.content.split()) < 2:
            await message.channel.send("You need to choose a songname")
            return
        await message.channel.send("yplay!!")
        for file in os.listdir("../downloads"):
            if file.endswith(".mp3") or file.endswith(".webm") or file.endswith(".part"):
                os.remove("../downloads/" + file)
        ydl_opts = {
            "noplaylist": True,
            "format": "bestaudio/best",
            "outtmpl": "../downloads/%(title)s-%(id)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now")
            #ydl.download([f"ytsearch1: {message.content.split()[1:]}"])
            data = ydl.extract_info(f"ytsearch1: {message.content.split()[1:]}")
            title_name = data['entries'][0]['title']

        song_name = ""
        for file in os.listdir("../downloads"):
            if file.startswith(title_name[:5]):
                song_name = file

        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
            return
        await message.author.voice.channel.connect()
        message.guild.voice_client.play(discord.FFmpegPCMAudio(f"../downloads/{song_name}"))
        await message.channel.send(f'**Now playing:** {song_name}')

    if message.content.startswith('!stop'):
        await message.guild.voice_client.disconnect()
        await message.channel.send("Song was stopped.")

    if message.content.startswith("!pause"):
        if message.guild.voice_client.is_playing():
            message.guild.voice_client.pause()
            await message.channel.send("Paused the song.")
        else:
            await message.channel.send("The bot is not playing anything at the moment.")

    if message.content.startswith('!resume'):
        if message.guild.voice_client is not None and message.guild.voice_client.is_paused:
            message.guild.voice_client.resume()
        elif message.guild.voice_client is not None and message.guild.voice_client.is_playing:
            await message.channel.send("Song is already playing.")
        else:
            await message.channel.send("Bot not in any voice channel.")

if __name__ == "__main__" :
    load_dotenv()
    client.run(os.getenv("discord_token"))
