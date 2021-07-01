# Change Status of Bot

```python
bot = discord.Client()

# Setting `Playing ` status
await bot.change_presence(activity=discord.Game(name="a game"))

# Setting `Streaming ` status
await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

# Setting `Listening ` status
await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# Setting `Watching ` status
await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
```



# Change Availability of Bot

```python
# Status to Online (The green one)
await client.change_presence(status=discord.Status.online)

# Status to Idle (The orange one)
await client.change_presence(status=discord.Status.idle)

# Status to Do not disturb (The red one)
await client.change_presence(status=discord.Status.dnd)
```





