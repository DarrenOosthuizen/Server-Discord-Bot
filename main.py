import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import time
import os
import asyncio
import socket

from functions import get_StartServer,get_LinDISK,get_LinDrives,get_CPU, get_DISK, get_Drives, get_NETWORKCONNECTIONS, get_NETWORKIO, get_RAM ,get_NSSTATUS,get_NSSTART,get_NSSTOP,get_PMSTATUS,get_PMSTART,get_PMSTOP
import rconclient
from dotenv import load_dotenv          
load_dotenv()

# Setting what prefix will be used to call commands
client = commands.Bot(command_prefix='?')

# Command Handler to check for errors and display message and send Help Display Command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title=f"INVALID COMMAND",description=f"Command : {ctx.message.content} not found.", color=discord.Colour.red())
        await ctx.send(embed=em)
        await Help(ctx)

# Displaying in console that Bot is running and connected
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="?Help"))

#region DarrenServer Commands
# Command for switching on Darren Server
@client.command()
async def startserver(ctx):
    GAMEADMINID = int(os.getenv('ADMINID'))
    PALWORLDCHANNELID = int(os.getenv('PALWORLDCHANNELID'))
    palworldChannel = client.get_channel(PALWORLDCHANNELID)
    role = discord.utils.get(ctx.guild.roles, id= GAMEADMINID)
    palworldRole = discord.utils.get(ctx.guild.roles, name = 'Palworld')
    print(ctx.author.roles)
    if role in ctx.author.roles:
        message = f'{palworldRole.mention} Flystudio Palworld Server is up running'
        serverRunning = get_StartServer()
        if serverRunning:
            await ctx.send('Server is already running!')
        else:
            await palworldChannel.send(message)
    else:
        await ctx.send(f'```Sorry {ctx.author} but you do not have the correct permissions to run the Command!! Please aquire the correct permissions to perform this command!```')

#endregion
        
async def sendUnathorizedResponse(ctx):
    await ctx.send(f'```Sorry {ctx.author} but you do not have the correct permissions to run the Command!! Please aquire the correct permissions to perform this command!```')
        
# Command for switching on Darren Server
@client.command()
async def palworld(ctx,command : str):

    adminCommand = isAdminRCONCommand(command)
    if adminCommand:
        isServerAdmin = isPalworldServerAdmin(ctx)
        if isServerAdmin :
            await sendPalworldRconResponse(ctx,command)
        else:
            await sendUnathorizedResponse(ctx,command)
    else:
        await sendPalworldRconResponse(ctx,command)

       
#endregion
        
async def sendPalworldRconResponse(ctx,command):
    SERVERIP = os.getenv('SERVERIP')
    SERVERPORT = int(os.getenv('SERVERPORT'))
    SERVERPASSWORD = os.getenv('SERVERPASSWORD')
    with rconclient.RCONClient(SERVERIP, SERVERPORT, SERVERPASSWORD) as client:
        response = client.command(command)
        await ctx.send(f'{response}') 
        
def isPalworldServerAdmin(ctx):
    ADMINID = int(os.getenv('ADMINID'))
    role = discord.utils.get(ctx.guild.roles, id= ADMINID)
    return role in ctx.author.roles

def isAdminRCONCommand(command : str):
    return command.lower() == 'info'or command.lower() == 'showplayers'



#region Ubuntu Server Commands
# Command to display CPU Specs
@client.command()
async def cpu(ctx):
    await ctx.send(f'```{get_CPU()}```')

@client.command()
async def invite(ctx):
    em = discord.Embed(
        url="https://darren.flystudio.co.za",
        title=f"Discord Invite Link",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyStudio Commands",
        icon_url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.set_thumbnail(
        url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.add_field(
        name="Link Below",
        value="http://discord.flystudio.co.za",
        inline=True)
    await ctx.send(embed=em)

# Command to display RAM Specs
@client.command()
async def ram(ctx):
    await ctx.send(f'```{get_RAM()}```')

# Command to get all Drives in the server
@client.command()
async def drives(ctx):
    drives = []
    drives = get_LinDrives()
    driveavailable = "List of current drives installed:"
    for d in drives:
        driveavailable += '\n-{0}'.format(d)
    await ctx.send(f'```{driveavailable}```')

# Command to get Disk Info
@client.command()
async def disk(ctx, arg):
    await ctx.send(f'```{get_LinDISK(arg)}```')

# Command to Display Network IO
@client.command()
async def netio(ctx):
    await ctx.send(f'```{get_NETWORKIO()}```')
#endregion

#region Public Server Commands
# Start Command for COD4 Public Server   
@client.command()
async def NSSTART(ctx):
    result = GameCheck(ctx)
    if result == True:
            value = get_NSSTART()
            if value == True:
                await ctx.send(f'```Starting Server```')
                time.sleep(3)
                await ctx.send(f'```Server is now Running```')
            elif value == False:
                await ctx.send(f'```Server Failed to Start```')
                await ctx.send(f'```Please retry to start server```')
    else:
        await ctx.send(f'```Sorry {ctx.author} but you do not have the permissions to Start the Server! Contact a Game Admin to start it!```')

# Status Command for COD4 Public Server  	
@client.command()
async def NSSTATUS(ctx):
	value = get_NSSTATUS()
	if value == True:
		await ctx.send(f'```COD4 Public Server is running!```')
	elif value == False:
		await ctx.send(f'```COD4 Public Server is offline!```')

# Stop Command for COD4 Public Server
@client.command()
async def NSSTOP(ctx):
    permis = GameCheck(ctx)
    if permis == True:
        result = get_NSSTATUS()
        if result == True:
            res = get_NSSTOP()
            if res == True:
                await ctx.send(f'```COD4 Public Server Shutting Down```')
                time.sleep(3)
                await ctx.send(f'```COD4 Public Server Now Offline```')
            elif res == False:
                await ctx.send(f'```Failed to shutdown COD4 Public Server```')
        elif result == False:
            await ctx.send(f'```COD4 Public Server is already Offline```')
    else:
        await ctx.send(f'```Sorry {ctx.author} but you do not have the permissions to Start the Server! Contact a Game Admin to start it!```')
#endregion

#region Promod Server Commands
# Start Command for COD4 Promod Server   
@client.command()
async def PMSTART(ctx):
    result = GameCheck(ctx)
    if result == True:
        value = get_PMSTART()
        if value == True:
            await ctx.send(f'```Starting Server```')
            time.sleep(3)
            await ctx.send(f'```Server is now Running```')
        elif value == False:
            await ctx.send(f'```Server Failed to Start```')
            await ctx.send(f'```Please retry to start server```')
    elif result == False:
        await ctx.send(f'```Sorry {ctx.author} but you do not have the permissions to Start the Server! Contact a Game Admin to start it!```')
	
# Status Command for COD4 Promod Server  	
@client.command()
async def PMSTATUS(ctx):
	value = get_PMSTATUS()
	if value == True:
		await ctx.send(f'```COD4 Promod Server is running!```')
	elif value == False:
		await ctx.send(f'```COD4 Promod Server is offline!```')

# Stop Command for COD4 Promod Server
@client.command()
async def PMSTOP(ctx):
    permis = GameCheck(ctx)
    if permis == True:
        result = get_PMSTATUS()
        if result == True:
            res = get_PMSTOP()
            if res == True:
                await ctx.send(f'```COD4 Promod Server Shutting Down```')
                time.sleep(3)
                await ctx.send(f'```COD4 Promod Server Now Offline```')
            elif res == False:
                await ctx.send(f'```Failed to shutdown COD4 Promod Server```')
        elif result == False:
            await ctx.send(f'```COD4 Promod Server is already Offline```')
    else:
        await ctx.send(f'```Sorry {ctx.author} but you do not have the permissions to Start the Server! Contact a Game Admin to start it!```')
#endregion

#region COD4 Server Commands
# Commands Display for Cod4 Public Server  
@client.command()
async def COD4NS(ctx):
    em = discord.Embed(
        url="https://discord.flystudio.co.za",
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

# Command to check if user has correct permissions to stop and start the server
def GameCheck(ctx):
    GAMEADMINID = int(os.getenv('ADMINID'))
    role = discord.utils.get(ctx.guild.roles, id= GAMEADMINID)
    if role in ctx.author.roles:
        return(True)
    else:
        return(False)

# Commands Display for Cod4 Promod Server
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
        icon_url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.set_thumbnail(
        url="https://i.imgur.com/CDWxjUZ.jpg"
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

# Commands Display for Cod4 Sniper Only Server
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
#endregion

#region Display Commands
# Commands Display for Game Server 
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

# Commands Display for FlyStudio Server
@client.command()
async def flystudio(ctx):
    em = discord.Embed(
        url="https://discord.flystudio.co.za",
        title=f"Ubuntu Commands List",
        description=f"Find current list of commands available for FlyStudio Server",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyStudio Commands",
        icon_url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.set_thumbnail(
        url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.add_field(
        name="FTP Details",
        value="`?ftp`",
        inline=True)
    em.add_field(
        name="VPN Details",
        value="`?vpn`",
        inline=True)
    em.add_field(
        name="PLEX Details",
        value="`?plex`",
        inline=True)
    await ctx.send(embed=em) 

# Display Commands for Ubuntu Server
@client.command()
async def ubuntu(ctx):
    em = discord.Embed(
        url="https://discord.flystudio.co.za",
        title=f"Ubuntu Commands List",
        description=f"Find current list of commands available for Ubuntu Server",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyUbuntu Commands",
        icon_url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.set_thumbnail(
        url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.add_field(
        name="CPU Monitor",
        value="`?cpu`",
        inline=True)
    em.add_field(
        name="RAM Levels",
        value="`?ram`",
        inline=True)
    em.add_field(
        name="Disk Usage",
        value="`?disk {Drive Letter}`",
        inline=True)
    em.add_field(
        name="Display Network Stats",
        value="`?netio`",
        inline=True)
    em.add_field(
        name="Display Drives",
        value="`?DRIVES`",
        inline=True)
    await ctx.send(embed=em)  

# Commands Display for Help to display all available Commands
@client.command()
async def Help(ctx):
    em = discord.Embed(
        url="https://discord.flystudio.co.za",
        title=f"FlyStudio Bot Commands List",
        description=f"Find current list of commands available for Bot",
        color=discord.Colour.green(),
    )
    em.set_author(
        name="FlyStudio Bot Commands",
        icon_url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.set_thumbnail(
        url="https://i.imgur.com/CDWxjUZ.jpg"
    )
    em.add_field(
        name="Display Plex Streaming Commands",
        value="`?plex`",
        inline=True)
    em.add_field(
        name="Display Game Server Commands",
        value="`?gameserver`",
        inline=True)
    em.add_field(
        name="Display FlyStudio Commands",
        value="`?flystudio`",
        inline=True)
    em.add_field(
        name="Palworld Server Commands",
        value="`?palworld`",
        inline=True)
    em.add_field(
        name="Discord Invite Link",
        value="`?invite`",
        inline=True)

    await ctx.send(embed=em)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="?Help"))
#endregion

#region FlyStudio Server Commands
# Command for Displaying Plex Server Details
@client.command()
async def plex(ctx):
    await ctx.send(f'```Please find the FlyStudio Plex Streaming Server link below:```')
    await ctx.send(f'https://www.plex.tv/sign-in/')
    await ctx.send(f'```Username : plex@flystudio.co.za\nPassword : PlexFlyStudio```')

# Command for Displaying VPN Details
@client.command()
async def vpn(ctx):
    await ctx.send(f'```Please Insert FlyStudio Username so that i can retrieve your details:```')
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
        
    try:
        msg = await client.wait_for("message", check=check, timeout=30) # 30 seconds to reply

    except asyncio.TimeoutError:
        await ctx.send(f'```{ctx.author} you have taken too long to respond and have canceled the operation!```')
    await ctx.send(f'{msg.content}')

# Command for Displaying FTP Details

#endregion

# Get Token and Run Discord Bot
client.run(os.getenv('TOKEN'))
