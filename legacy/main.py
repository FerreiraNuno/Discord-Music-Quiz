import discord
from src import play_music
from src.play_music import Scores
from fuzzywuzzy import fuzz
import asyncio
import random
from spotify_module import song_list

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Music")
    await client.change_presence(status=discord.Status.online, activity=game)
    print(client.guilds)
    for guild in client.guilds:
        print(f"Logged into {guild.name}")
    server = discord.utils.get(client.guilds, name="Bot Testing")
    for i in server.text_channels:
        print(f"Channels on Server: {i.name}")


#song_list = song_list()
song_list = ["Umbrella - Rihana", "Intro - Cro", "Bros - Rin"]

client.game = False
client.number_input = False

@client.event
async def on_message(message):
    # ignores bot messages
    if message.author == client.user:
        return
    # normal music bot play command
    if message.author != client.user and message.content.startswith("play") and client.game is False:
        song = message.content.replace('play ', '')
        await message.author.voice.channel.connect()
        play_music.play_song(message, client, song, client.game)

    # start quiz
    if message.content.startswith("!quiz"):
        if message.author.voice is None:
            await message.channel.send("**You're not even in a voicechannel**")
        else:
            client.number_input = True
            await message.channel.send("Plase select the number of rounds you want to play by sending the"
                                       "command **!num** followed by the number of desired rounds\n"
                                       "eg. !num 10")

    if message.content.startswith("!num") and client.number_input is True:
        client.number_input = False
        desired_rounds = int(message.content.replace("!num", ""))
        if type(desired_rounds) is int:
            await message.channel.send(f"**Okay, we are playing {desired_rounds} rounds**")
        else:
            await message.channel.send("**Invalid input, you need to put an integer after the !num command**")
        if desired_rounds >= 31:
            await message.channel.send(f"**That number is way too high, the maximum number of rounds to play is 30**")
        else:
            client.game_rounds = desired_rounds + 1
            client.game = True

        # create player list
        client.players = []
        await message.add_reaction('\U0001F44D')
        for member in message.author.voice.channel.members:
            if member.display_name != "Nuno´s Music Bot" and member != client.user:
                client.players.append(f"{member.mention}")

        # create scoring system
        text = ""
        for player in client.players:
            text += f"{player}\n"
        embed = discord.Embed(title="The players are:", description=text)
        embed.add_field(name="**rules**",
                        value="1: type the name of the artist (not the feat.), and the track in separate messages\n"
                              "2: use the command !pass if you do not know any of the answers\n"
                              "3: if two people guess at the same time (tolerance of 0.5 seconds) both get a point\n"
                              "4: the person who guessed most artists and tracks correctly wins",
                        inline=False)
        embed.add_field(name="next round", value=f"round 1/{client.game_rounds - 1}", inline=False)
        await message.channel.send(embed=embed)
        client.score = Scores()
        client.score.add_players(client.players)

        # create player library with number of passes used per round
        client.pass_count_user = {}
        for player in client.players:
            client.pass_count_user.update({player: 0})

        # start quiz
        await message.channel.send(f"**Quiz starting in a few seconds!**")
        await message.author.voice.channel.connect()

        # get songs
        client.imported_songs = []
        for song in random.sample(song_list, client.game_rounds):
            client.imported_songs.append(song)
        client.active_guild = message.author.guild  # current server the game is running on

        # variables
        client.counter = 0  # round number
        client.pass_count = 0  # pass number
        client.validate = [0, 0]  # metadata validator
        client.points_shown = False  # prevents double display of points
        client.say_next = False  # determine if the bot has to say "playing next song!"
        client.wrong_counter = 0

        # amount of passes needed
        if len(client.players) == 1:
            client.needed_passes = 1
        elif 2 <= len(client.players) <= 3:
            client.needed_passes = 2
        elif 4 <= len(client.players) < 6:
            client.needed_passes = 3
        else:
            client.needed_passes = 4

        # play song
        play_music.play_song(message, client, client.imported_songs[client.counter], client.game)

        # create song metadata
        client.final_songs = []
        for song in client.imported_songs:
            client.final_songs.append(song.split(" - "))
        print(client.final_songs)
        print(client.final_songs[client.counter])

    # core game
    if client.game is True:
        # option for players to pass a song if they don't know the answer
        if message.content.startswith("!pass") and client.wrong_counter > 0 \
                and client.pass_count_user.get(message.author.mention) == 0:
            if client.pass_count <= client.needed_passes:
                client.pass_count += 1
                client.pass_count_user.update({message.author.mention: client.pass_count_user.get(message.author.mention) + 1})
                await message.channel.send(f'**pass {client     .pass_count}/{client.needed_passes}**')
            if client.pass_count == client.needed_passes:
                client.pass_count = 0
                client.counter += 1
                client.validate = [0, 0]
                client.wrong_counter = 0
                for player in client.players:
                    client.pass_count_user.update({player: 0})
                voice = discord.utils.get(client.voice_clients, guild=message.channel.guild)
                voice.stop()
                await message.channel.send('**aight fam skipping this one**')
                await message.channel.send(f"**The songs name was:** {str(client.final_songs[client.counter - 1][0])} - "
                                           f"{str(client.final_songs[client.counter - 1][-1])}")
                client.say_next = True
                # end game if number of rounds is at the predefined value
                if client.counter == client.game_rounds:  # game is finished
                    await message.channel.send('**The Game is over!**')
                    client.game = False
                else:
                    text = ""
                    for player in client.score.get_scores():
                        text += f"{player}: {client.score.get_scores().get(player)}\n"
                    embed = discord.Embed(title="The current score is:", description=text)
                    embed.add_field(name="next round is:", value=f"round {client.counter + 1}/{client.game_rounds - 1}", inline=False)
                    await message.channel.send(embed=embed)
        elif message.content.startswith("!pass") and client.wrong_counter == 0 \
                and client.pass_count_user.get(message.author.mention) == 0:
            await message.channel.send("Why dont you all try at least once before passing?\nBut okay just type "
                                       "the pass command again if you're sure you don't know the answer...")
            client.wrong_counter += 1
        elif message.content.startswith("!pass") and client.wrong_counter > 0 \
                and client.pass_count_user.get(message.author.mention) > 0:
            await message.channel.send("**You already used your pass command**")

        # input
        if not message.content.startswith("!") and message.author.guild == client.active_guild and client.game is True:
            # check if word matches track
            if fuzz.ratio(message.content.lower(), client.final_songs[client.counter][0].lower()) >= 85 \
                    and client.validate[0] == 0 and message.author != client.user:
                await message.add_reaction('\U0001F44D')
                await message.channel.send('**Track correct!**')
                client.validate[0] = 1
                print(client.validate)
                await asyncio.sleep(0.5)
                await message.channel.send(f'+1 point for {message.author.mention}')
                client.score.add_point(message.author.mention)
            # check if word matches artist
            elif fuzz.ratio(message.content.lower(), client.final_songs[client.counter][-1].lower()) >= 85 and client.validate[1] == 0:
                await message.add_reaction('\U0001F44D')
                await message.channel.send('**Artist correct!**')
                client.validate[1] = 1
                print(client.validate)
                await asyncio.sleep(0.5)
                await message.channel.send(f"**+1 point for** {message.author.mention}")
                client.score.add_point(message.author.mention)
            # else if both are wrong give thumbs down
            elif message.author != client.user and message.author != "Nuno´s Music Bot":
                await message.add_reaction('\U0001F44E')
                client.wrong_counter += 1
            # skip song if both track and artist are correct
            if client.validate == [1, 1]:
                client.counter += 1
                client.validate = [0, 0]
                client.wrong_counter = 0
                for player in client.players:
                    client.pass_count_user.update({player: 0})
                voice = discord.utils.get(client.voice_clients, guild=message.channel.guild)
                voice.stop()
                await message.channel.send(f"**The songs name was:** {str(client.final_songs[client.counter-1][0])} - "
                                           f"{str(client.final_songs[client.counter-1][-1])}")
                # send scores
                if client.counter + 1 < client.game_rounds:
                    text = ""
                    for player in client.score.get_scores():
                        text += f"{player}: {client.score.get_scores().get(player)}\n"
                    embed = discord.Embed(title="The current score is:", description=text)
                    embed.add_field(name="next round is :", value=f"round {client.counter + 1}/{client.game_rounds - 1}", inline=False)
                    await message.channel.send(embed=embed)
                    client.say_next = True
                elif client.counter == client.game_rounds:  # game is finished
                    await message.channel.send('**The Game is over!**')
                    client.game = False

        # end game
        if client.game_rounds == client.counter + 1 and client.points_shown is False:
            # display points
            client.points_shown = True
            text = ""
            for player in client.score.get_scores():
                text += f"{player}: {client.score.get_scores().get(player)}\n"
            embed = discord.Embed(title="The final score is:", description=text)
            await message.channel.send(embed=embed)
            client.say_next = False
            try:
                await client.voice_clients[0].disconnect()
            except IndexError:
                pass

        # skip current song
        if client.say_next is True:
            client.pass_count = 0
            await message.channel.send('**Playing next song in a few seconds!**')
            play_music.play_song(message, client, client.imported_songs[client.counter], client.game)
            print(client.counter)
            print(client.final_songs[client.counter])
            client.say_next = False

        if message.content.startswith("!end"):
            print("ended game")
            client.game = False
            try:
                await client.voice_clients[0].disconnect()
            except IndexError:
                pass


client.run('NzA0NDczNTMwNDg1NzAyNzQ4.XqdqGg.31vM6-txvhySiHRV8ooDXuRIAvI')