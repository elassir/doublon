import asyncio
import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import yt_dlp as youtube_dl

import requests
import time
from riotwatcher import LolWatcher
import random

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.messages = True
intents.message_content = True

api_key = 'RGAPI-6bd4cf07-1201-4db2-ba19-47f26de5ed19'
region = 'euw1' 

lol_watcher = LolWatcher(api_key)







load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
    
@bot.command(name='play', help='To play song')
async def play(ctx,url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop)
        player = discord.FFmpegPCMAudio(executable="C:\\Users\\moi\\Desktop\\dossier bot\\ffmpeg-2023-07-19-git-efa6cec759-full_build\\bin\\ffmpeg.exe", source=filename)
        player = discord.PCMVolumeTransformer(player, volume=0.05)  # Réglez le volume ici
        voice_channel.play(player)
    await ctx.send('**Now playing:** {}'.format(filename))


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")
    


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

queue_id_to_name = {
    0: "Custom",
    400: "Draft Pick",
    420: "Ranked Solo",
    430: "Blind Pick",
    440: "Ranked Flex",
    450: "ARAM",
    460: "Blind Pick 3v3", 
    470: "Ranked Flex 3v3",
    700: "Clash",
    830: "Co-op vs. AI",
    840: "Co-op vs. AI",
    850: "Co-op vs. AI",
    900: "URF",
    910: "Co-op vs. AI",
    920: "Co-op vs. AI",
    930: "Co-op vs. AI",
    940: "Co-op vs. AI",
    950: "Co-op vs. AI",
    960: "Co-op vs. AI",
    980: "Star Guardian Invasion",
    990: "Star Guardian Invasion: Onslaught",
    1000: "PROJECT: Hunters",
    1010: "Snow ARURF",
    1020: "One for All",
    1030: "Odyssey Extraction: Intro",
    1040: "Odyssey Extraction: Cadet",
    1050: "Odyssey Extraction: Crewmember",
    1060: "Odyssey Extraction: Captain",
    1070: "Odyssey Extraction: Onslaught",
    1090: "TFT",
    1100: "Ranked TFT",
    1110: "TFT Tutorial",
    1200: "Nexus Blitz",
    1700: "arena",
    2000: "Tutorial 1",
    2010: "Tutorial 2",
    2020: "Tutorial 3",
}


@bot.command(name='split')
async def split_teams(ctx):
    if ctx.author.voice is None:
        await ctx.send("Vous devez être dans un salon vocal pour utiliser cette commande.")
        return

    voice_channel = ctx.author.voice.channel
    members = voice_channel.members
    random.shuffle(members)

    team_a_channel = discord.utils.get(ctx.guild.voice_channels, name='Equipe A')
    team_b_channel = discord.utils.get(ctx.guild.voice_channels, name='Equipe B')

    if team_a_channel is None or team_b_channel is None:
        await ctx.send("Les salons 'Equipe A' et 'Equipe B' doivent exister.")
        return

    half = len(members) // 2
    team_a = members[:half]
    team_b = members[half:]

    for member in team_a:
        await member.move_to(team_a_channel)

    for member in team_b:
        await member.move_to(team_b_channel)


@bot.command(name='quoi')
async def quoicou(ctx):
        await ctx.send(f"{ctx.message.author.mention}, coubeh")

    




@bot.command(name = 'age')
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')







@bot.command(name='statue')
async def statue(ctx):
    summoner_names = ['sampiklesyeux', 'barkeagles','meudon la foret', 'misterjlb', 'montépixou', 'itWas2short', 'katsuni', 'asmothy']

    # Télécharger la liste complète des champions
    response = requests.get('http://ddragon.leagueoflegends.com/cdn/13.14.1/data/en_US/champion.json')
    champions_data = response.json()
    champions = {champion['key']: champion['name'] for champion in champions_data['data'].values()}

    # Créer un message global pour contenir toutes les informations
    global_message = ""

    for summoner_name in summoner_names:
        try:
            summoner = lol_watcher.summoner.by_name(region, summoner_name)
        except Exception as e:
            global_message += f"Impossible de trouver le joueur : {summoner_name}\n"
            continue

        try:
            current_match = lol_watcher.spectator.by_summoner(region, summoner['id'])
        except Exception as e:
            global_message += f"Le joueur {summoner_name} n'est pas en partie.\n"
            continue

        # Get game start time and calculate elapsed time in minutes
        game_start_time_ms = current_match['gameStartTime']
        elapsed_time_min = (time.time() * 1000 - game_start_time_ms) // 60000

        # Get game queue id and look up queue name
        queue_id = current_match['gameQueueConfigId']
        queue_name = queue_id_to_name.get(queue_id, 'Unknown')

        # Obtenez des informations sur le match en cours
        for participant in current_match['participants']:
            if participant['summonerId'] == summoner['id']:
                champion_id = str(participant['championId'])
                champion_name = champions.get(champion_id, 'Unknown')
                global_message += f"Le joueur {summoner_name} est en partie {queue_name} avec {champion_name} depuis {elapsed_time_min} minutes.\n"

    await ctx.send(global_message)
    
@bot.command(name='sos')
async def aide(ctx):
    await ctx.send(f"{ctx.message.author.mention}, voila ce que je peux faire :\n !join puis !play suivi de l'url yt \n !statut\n !split\n !quoi \n !age" )


if __name__ == "__main__" :
    bot.run('MTEzMTI3MDIwNDEwNjc0Nzk1Ng.GWDiIU.bf40ISeny70PoLOdTf1Rqd4B1PBeeGxWjSS70w')



