import discord
import youtube_dl
import os
from pydub import AudioSegment

async def play_song(message, song, game_on):
    print("deleting old file")
    for file in os.listdir():
        if file.endswith(".mp3") or file.endswith(".webm") or file.endswith(".part"):
            os.remove(file)
    print("joining voice channel")
    if not message.author.voice:
        await message.channel.send("{} is not connected to a voice channel".format(message.message.author.name))
        return
    await message.author.voice.channel.connect()
    print("choosing youtube api settings")
    ydl_opts = {
        "noplaylist": True,
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        ydl.download([f"ytsearch1: {song}"])
    print("renaming file")
    for file in os.listdir():
        if file.endswith(".mp3"):
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    if game_on:
        start_min = 1
        start_sec = 1
        end_min = 1
        end_sec = 59
        # Time to miliseconds
        start_time = start_min * 60 * 1000 + start_sec * 1000
        end_time = end_min * 60 * 1000 + end_sec * 1000
        song = AudioSegment.from_mp3("song.mp3")
        extract = song[start_time:end_time]
        # Saving
        extract.export("song" + '-extract.mp3', format="mp3")
        os.remove("song.mp3")

        #TODO: play sound
    else:
        print("playing sound")
        message.guild.voice_client.play(discord.FFmpegPCMAudio(executable="../bin/ffmpeg.exe", source="song.mp3"))
        await message.channel.send('**Now playing:** {}'.format("song.mp3"))


###############################


    if game_on:
        start_min = 1
        start_sec = 1
        end_min = 1
        end_sec = 59
        # Time to miliseconds
        start_time = start_min * 60 * 1000 + start_sec * 1000
        end_time = end_min * 60 * 1000 + end_sec * 1000
        song = AudioSegment.from_mp3("song.mp3")
        extract = song[start_time:end_time]
        # Saving
        extract.export("song" + '-extract.mp3', format="mp3")
        os.remove("song.mp3")

        #TODO: play sound