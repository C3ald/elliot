import discord
import os
from utils import ping, meme, get_htb_top_100, get_user_info_username, get_user_info_id, get_unreleased
import time as t

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
    if message.content.startswith('$topusers'):
        limit = message.content.replace('$topusers ', '')
        if limit == '' or limit == '$topusers':
            limit = 5
        print(limit)
        data = get_htb_top_100(limit)
        response = f'obtained the top: {limit} users'
        await message.channel.send(response)
        place = 1
        for user in data:
            await message.channel.send(f"""#{place}: {user['country']}'s {user["name"]}, 🩸s:{user["bloods"]}, ♢s:{user["points"]}, and {user['owns']} owns""")
            place = place + 1
            t.sleep(0.01)
    
    if message.content.startswith('$user'):
        user = message.content.replace('$user ', '')
        try:
            data = get_user_info_username(user)
            response = f"user: {data['name']} \n{data['avatar']}\nbloods 🩸: {data['bloods']} \npoints ♢: {data['points']} \nrank: {data['rank']} \nrank progress: {data['rank progress']}% \ncompletion: {data['completion']}% \nglobal rank 🌐: {data['global rank']}"

        except:
            try:
                data = get_user_info_id(user)
                response = f"user: {data['name']} \n{data['avatar']}\nbloods 🩸: {data['bloods']} \npoints ♢: {data['points']} \nrank: {data['rank']} \nrank progress: {data['rank progress']}% \ncompletion: {data['completion']}% \nglobal rank 🌐: {data['global rank']}"

            except:
                response = f"user: {user} not in Elliot's database!"
        await message.channel.send(response)
    if message.content.startswith('$unreleased'):
        machines = get_unreleased()
        for machine in machines:
            response = f"""machine name: {machine['name']}\n
                            {machine['avatar']}\n
                            difficulty: {machine['difficulty']}\n
                            OS: {machine['os']}\n
                            creators: {machine['creators']}\n
                            release data: {machine['release date']}\n\n"""
            await message.channel.send(response)
        
        
    if message.content.startswith('$help'):
        response = """Command list: \n
              `$unreleased` gets the unreleased machine list
              `$user` 'id or username'\n
              `$topusers` 'top number' gets the top number of users ex: '`$topusers 5`' gets the top 5 users\n
              `$hello` 'who to say hello to' \n
              `$meme` gets a meme\n 
              `$ping` pings google.com"""
        await message.channel.send(response)
        
        
client.run(token)