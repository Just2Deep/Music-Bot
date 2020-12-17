import discord 
from discord.ext import commands, tasks
import youtube_dl
import random 
import os 

client = commands.Bot(command_prefix = '.')

status = ["Bass!", "Alternative!", "Pop!", "Hip-hop!", "Chill!"]

@client.event
async def on_ready():
  change_status.start()
  print('Bot is Online!')

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

@tasks.loop(seconds = 200)
async def change_status():
  await client.change_presence(activity= discord.Game(random.choice(status)))

client.run(os.getenv('TOKEN'))
