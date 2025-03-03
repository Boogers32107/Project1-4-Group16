import discord
import asyncio
import aiohttp
import json
import html 


TOKEN = 'MTMzNDI1OTIzODQ0MDI3NjA5Mg.GohmT3.bgCbmt6JuFo7FHPVayfE39ZYNscyGuVt5XnMdI' #Please don't abuse the token it is for my discord server with just me and a bot.

intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

current_question = None
current_answer = None


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
    global current_question, current_answer
    if message.author == client.user:
        return

    if message.content.startswith('!trivia'): #This is the command it will watch in chat for.
        questions = await fetch_trivia()
        print(f"{html.unescape(questions)}")
        if questions:
            for question in questions:
                current_question = question['question']
                current_answer = question['correct_answer']
                await message.channel.send(f"Category: {question['category']}\nQuestion: {question['question']}\nReply with 'True' or 'False' otherwise it will break and give me an error.")
                await asyncio.sleep(15) #Delay of 15 seconds so it doesn't get spammed.
        else:
            await message.channel.send("Please don't spam try again in a bit.")

    elif current_question and message.content in ['True', 'False']:
                if message.content == current_answer:
                    await message.channel.send ("Correct")
                else:
                    await message.channel.send("Not Correct")
                    current_question = None
                    current_answer = None
   
    
#@client.event
#async def on_message(message):
        #if message.author == client.user:
            #return 
        
        #if message.content.startswith('!leaderboard'): #Will pull up Leaderboard


client.run(TOKEN) #Pulls from the uptop token not doing a .env cause this is a private repo.