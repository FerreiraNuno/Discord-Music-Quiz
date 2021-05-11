import discord
import youtube_dl
import os
from pydub import AudioSegment


def play_song(message, client, song, game_on):
    for file in os.listdir("./"):
        if file.endswith(".mp3") or file.endswith(".webm") or file.endswith(".part"):
            os.remove(file)
    voice = discord.utils.get(client.voice_clients, guild=message.channel.guild)
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

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
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

        # play sound
        voice.play(discord.FFmpegPCMAudio("song-extract.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.45

    else:
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.45


class Scores:
    def __init__(self):
        self.players = {}

    def add_players(self, players_list):
        points = 0
        self.players = self.players.fromkeys(players_list, points)

    def get_scores(self):
        sorted_dict = {k: v for k, v in sorted(self.players.items(), reverse=True, key=lambda item: item[1])}
        return sorted_dict

    def add_point(self, player_name):
        players_score = self.players.get(player_name)
        self.players.update({player_name: players_score + 1})
