import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import time
import os

from functions import get_NSSTATUS,get_NSSTART,get_CPU, get_DISK, get_Drives, get_NETWORKCONNECTIONS, get_NETWORKIO, get_RAM
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='?')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title=f"INVALID COMMAND",
                           description=f"Command : {ctx.message.content} not found.", color=discord.Colour.red())
        await ctx.send(embed=em)
        await HELP(ctx)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Recording Stats"))


@client.command()
async def CPU(ctx):
    await ctx.send(f'```{get_CPU()}```')


@client.command()
async def RAM(ctx):
    await ctx.send(f'```{get_RAM()}```')


@client.command()
async def DRIVES(ctx):
    drives = []
    drives = get_Drives()
    driveavailable = "List of current drives installed:"
    for d in drives:
        driveavailable += '\n {0}'.format(d)
    await ctx.send(f'```{driveavailable}```')


@client.command()
async def DISK(ctx, arg):
    arg += ":"
    drives = []
    drives = get_Drives()
    found = False
    for d in drives:
        if(arg == d):
            found = True

    if(found == True):
        await ctx.send(f'```{get_DISK(arg)}```')
    else:
        notfound = 'Drive {0} was not found! Please see list Below'.format(arg)
        await ctx.send(f'```{notfound}```')
        await DRIVES(ctx)


@client.command()
async def NETCON(ctx):
    await ctx.send(f'```{get_NETWORKCONNECTIONS()}```')


@client.command()
async def NETIO(ctx):
    await ctx.send(f'```{get_NETWORKIO()}```')

@client.command()
async def GAMESERVER(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"Gaming Server Commands List",
        description=f"Find current list of commands available for FlyStudio Game Server",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyGaming Commands",
        icon_url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.set_thumbnail(
        url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.add_field(
        name="COD4X Public",
        value="`?COD4NS`",
        inline=True)
    em.add_field(
        name="COD4X Promod",
        value="`?COD4PM`",
        inline=True)
    em.add_field(
        name="COD4X Snipers Only",
        value="`?COD4SO`",
        inline=True)
    await ctx.send(embed=em)
    
@client.command()
async def COD4NS(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"COD4 Public Server Commands List",
        description=f"Find current list of commands available for COD4",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyGaming Commands",
        icon_url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.set_thumbnail(
        url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.add_field(
        name="Start Server",
        value="`?NSSTART`",
        inline=True)
    em.add_field(
        name="Stop Server",
        value="`?NSSTOP`",
        inline=True)
    em.add_field(
        name="Server Status",
        value="`?NSSTATUS`",
        inline=True)
    await ctx.send(embed=em)    
    
@client.command()
async def NSSTART(ctx):
	value = get_NSSTART()
	if value == True:
		await ctx.send(f'```Starting Server```')
		time.sleep(3)
		await ctx.send(f'```Server is now Running```')
	elif value == False:
		await ctx.send(f'```Server Failed to Start```')
		await ctx.send(f'```Please retry to start server```')
	
	
@client.command()
async def NSSTATUS(ctx):
	value = get_NSSTATUS()
	if value == True:
		await ctx.send(f'```COD4 Public Server is running!```')
	elif value == False:
		await ctx.send(f'```COD4 Public Server is offline!```')
     


@client.command()
async def COD4PM(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"COD4 Promod Server Commands List",
        description=f"Find current list of commands available for Promod Server",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyGaming Commands",
        icon_url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.set_thumbnail(
        url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.add_field(
        name="Start Server",
        value="`?PMSTART`",
        inline=True)
    em.add_field(
        name="Stop Server",
        value="`?PMSTOP`",
        inline=True)
    em.add_field(
        name="Server Status",
        value="`?PMSTATUS`",
        inline=True)
    await ctx.send(embed=em)  
 
 
 
@client.command()
async def COD4SO(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"COD4 Sniper Only Server Commands List",
        description=f"Find current list of commands available for Snipers Only Server",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyGaming Commands",
        icon_url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.set_thumbnail(
        url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.add_field(
        name="Start Server",
        value="`?SOSTART`",
        inline=True)
    em.add_field(
        name="Stop Server",
        value="`?SOSTOP`",
        inline=True)
    em.add_field(
        name="Server Status",
        value="`?SOSTATUS`",
        inline=True)
    await ctx.send(embed=em)  


@client.command()
async def HELP(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"Server01 Commands List",
        description=f"Find current list of commands available for Server01 Bot",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="Server 01 Commands",
        icon_url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.set_thumbnail(
        url="https://www.nicepng.com/png/full/207-2078307_ubuntu-server-logo-ubuntu.png"
    )
    em.add_field(
        name="CPU Monitor",
        value="`?CPU`",
        inline=True)
    em.add_field(
        name="RAM Levels",
        value="`?RAM`",
        inline=True)
    em.add_field(
        name="Disk Usage",
        value="`?DISK {Drive Letter}`",
        inline=True)
    em.add_field(
        name="Display Network Stats",
        value="`?NETIO`",
        inline=True)
    em.add_field(
        name="Display Drives",
        value="`?DRIVES`",
        inline=True)
    em.add_field(
        name="Display Game Server Commands",
        value="`?GAMESERVER`",
        inline=True)

    await ctx.send(embed=em)


client.run(os.getenv('TOKEN'))
