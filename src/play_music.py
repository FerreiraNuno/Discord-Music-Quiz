import yt_dlp
import os
import discord


async def play_song(message, guilds):
    if not message.author.voice:
        await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
        return
    if len(message.content.split()) < 2:
        await message.channel.send("You need to choose a songname")
        return
    if guilds[message.guild].song_on:
        await message.channel.send("Queue!!")

    guilds[message.guild].song_on = True
    await message.channel.send("Fetching Song!!")

    if message.guild.voice_client is None or message.guild.voice_client.is_paused():
        for file in os.listdir("../downloads/" + message.guild.name):
            if file.endswith(".mp3") or file.endswith(".webm") or file.endswith(".part"):
                os.remove(f"../downloads/{message.guild.name}/{file}")

    file_name = await download_from_yt(message)

    if message.guild.voice_client is None:
        await message.author.voice.channel.connect()
    if message.guild.voice_client.is_playing():
        message.guild.voice_client.pause()
    message.guild.voice_client.play(discord.FFmpegPCMAudio(f"../downloads/{message.guild.name}/{file_name}"))
    await message.channel.send(f'Now playing: **{file_name[:-16]}** ')

async def stop(message, guilds):
    if message.guild.voice_client is not None and message.guild.voice_client.is_connected():
        await message.guild.voice_client.disconnect()
        await message.channel.send("Song was stopped.")

async def pause(message, guilds):
    if message.guild.voice_client is not None and message.guild.voice_client.is_playing():
        message.guild.voice_client.pause()
        await message.channel.send("Paused the song.")
    else:
        await message.channel.send("The bot is not playing anything at the moment.")

async def resume(message, guilds):
    if message.guild.voice_client is not None and message.guild.voice_client.is_paused():
        message.guild.voice_client.resume()
    elif message.guild.voice_client is not None and message.guild.voice_client.is_playing():
        await message.channel.send("Song is already playing.")
    else:
        await message.channel.send("Bot not in any voice channel.")


async def download_from_yt(message) -> str:
    ydl_opts = {
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": f"../downloads/{message.guild.name}/%(title)s-%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        # ydl.download([f"ytsearch1: {message.content.split()[1:]}"])
        data = ydl.extract_info(f"ytsearch1: {message.content.split()[1:]}")
        title_name = data['entries'][0]['title']

    for file in os.listdir("../downloads/" + message.guild.name):
        if file.startswith(title_name[:5]):
            return file