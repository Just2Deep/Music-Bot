import discord 
from discord.ext import commands, tasks
import youtube_dl
import random 
import os 
import pypi

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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
        self.url = data.get('url')


@classmethod
async def from_url(cls, url, *, loop=None, stream=False):
  loop = loop or asyncio.get_event_loop()
  data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

  if 'entries' in data:
            # take first item from a playlist
    data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix = '.')

status = ["Bass!", "Alternative!", "Pop!", "Hip-hop!", "Chill!", "Indie!", "R&B", "EDM", "Punk!", "Soul"]

@client.event
async def on_ready():
  change_status.start()
  print('Bot is Online!')

@client.event
async def on_member_join():
  channel = discord.utils.get(member.guild.channels, name = 'general')
  await channel.send(f'Welcome {member.mention}! Ready to jam? see `help` for details')

@client.command(name= 'ping', help='This command return the latency')
async def ping(ctx):
  await ctx.send(f'**Ping!** Latency {round(client.latency * 1000)}ms')

@client.command(name= 'hello', help='This command returns a random welcome message')
async def hello(ctx):
  responses = ['***grumble*** Why did you wake me?', 'Top of the morning to you lad!', 'Wassup?', 'Well Hello Beautiful.', 'Hello there! how are you?']
  await ctx.send(random.choice(responses))

@client.command(name= 'die', help='This command returns last message')
async def die(ctx):
  responses = ['I could have done so much more','i have a family, kill them instead', 'Why have you brought my short life to an end']
  await ctx.send(random.choice(responses))

@client.command(name= 'credits', help='This command returns credits')
async def credits(ctx):
  await ctx.send('Made by `Just2Deep`')
  await ctx.send('Thanks for visiting the server!')

@client.command(name= 'play', help='This command plays music')
async def play(ctx):
  if not ctx.message.author.voice:
    await ctx.send('You are not connected to a voice channel')
    return

  else:
    channel = ctx.message.author.voice.channel

  await channel.connect()

@client.command(name= 'stop', help='This command stops music and makes bot leave voice channel')
async def stop(ctx):
  voice_client = ctx.message.guide.voice_client
  await voice_client.disconnect()

@tasks.loop(seconds = 200)
async def change_status():
  await client.change_presence(activity= discord.Game(random.choice(status)))

client.run(os.getenv('TOKEN'))
