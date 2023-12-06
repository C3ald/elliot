import discord
import os
from utils import ping, meme, get_htb_top_100, get_user_info_username

token = open('./token.txt', 'r').read()



intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in client.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1



@client.event
async def on_message(message):
    print(message)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        c = message.content.replace('$hello ', '')
        await message.channel.send(f'Hello {c}!')
    if message.content.startswith('$ping') or message.content.startswith('$Ping'):
        data = ping()
        await message.channel.send(f'pinged google.com with: {data} latency!')
    if message.content.startswith('$meme'):
        data = meme()
        response = f"here's one from {data['sub']} posted by, {data['op']} \n\n{data['title']} \n {data['preview']}"
        await message.channel.send(response)
# HTB Stuff
    if message.content == ('$topusers'):
        limit = message.content.replace('$topusers', '')
        try:
                limit = message.content.replace(' ', '')
        except:
                limit = 5
        print(limit)
        if limit == '' or limit == '$topusers':
                limit = 5
        data = get_htb_top_100(limit)
        response = f'obtained the top: {limit} users: \n{data}'
        await message.channel.send(response)
    
    if message.content.startswith('$user'):
        user = message.content.replace('$user ', '')
        data = get_user_info_username(user)
        response = f"user: {data['name']} \n{data['avatar']}\nbloods 🩸: {data['bloods']} \npoints ♢: {data['points']} \nrank: {data['rank']} \nrank progress: {data['rank progress']}% \ncompletion: {data['completion']}% \nglobal rank 🌐: {data['global rank']}"
        await message.channel.send(response)
                
        
        
client.run(token)