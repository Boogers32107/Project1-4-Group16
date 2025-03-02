import discord
import asyncio
import aiohttp
import json

TOKEN = 'MTMzNDI1OTIzODQ0MDI3NjA5Mg.GohmT3.bgCbmt6JuFo7FHPVayfE39ZYNscyGuVt5XnMdI' #Please don't abuse the token it is for my discord server with just me and a bot.

intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

async def fetch_trivia(): #Pulls from URL
    url = 'https://opentdb.com/api.php?amount=1&category=15&type=boolean' #This is our Video Games API URL it will pull from a pool questions.
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            else:
                return None

@client.event
async def on_ready():
    print(f'Successfully started up as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!trivia'): #This is the command it will watch in chat for.
        questions = await fetch_trivia()
        if questions:
            for question in questions:
                await message.channel.send(f"Category: {question['category']}\nQuestion: {question['question']}")
                await asyncio.sleep(15) #Delay of 15 seconds so it doesn't get spammed.
        else:
            await message.channel.send("Please don't spam try again in a bit.")

client.run(TOKEN) #Pulls from the uptop token not doing a .env cause this is a private repo.