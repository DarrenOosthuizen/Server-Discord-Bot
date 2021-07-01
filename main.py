import discord
from discord.ext import commands
import os

from readings import get_CPU, get_DISK, get_NETWORKCONNECTIONS, get_NETWORKIO, get_RAM
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='`')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Recording Stats"))


@client.command()
async def CPU(ctx):
    await ctx.send(ctx.channel.id) #Displays Channel ID
    await ctx.send(ctx.author.id) #Displays User who sent message ID
    await ctx.send(f'```{get_CPU()}```')


@client.command()
async def RAM(ctx):
    await ctx.send(f'```{get_RAM()}```')


@client.command()
async def DISK(ctx):
    await ctx.send(f'```{get_DISK()}```')


@client.command()
async def NETCON(ctx):
    await ctx.send(f'```{get_NETWORKCONNECTIONS()}```')


@client.command()
async def NETIO(ctx):
    await ctx.send(f'```{get_NETWORKIO()}```')


@client.command()
async def helpme(ctx):
    help_statements = [
        '.ip : Returns the IP Address for klazeM`s CSGO server.',
        '.start_server : Launches klazeM`s CSGO server',
        '.end_server : Shuts down klazeM`s CSGO server'
    ]

    for statement in help_statements:
        await ctx.send(statement)


client.run(os.getenv('TOKEN'))
