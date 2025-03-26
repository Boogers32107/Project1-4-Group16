import discord
import asyncio
import aiohttp
import html
from leaderboard import update_score, get_leaderboard #Pulls from the leaderboard.py file

TOKEN = '' # INPUT BOT TOKEN HERE

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_question = None
current_answer = None

async def fetch_trivia(): #Tells it where to fetch the question from
    url = 'https://opentdb.com/api.php?amount=1&category=15&type=boolean' #URL for Open Trivia DataBase
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            else:
                return None

@client.event
async def on_ready():
    print(f'Successfully started up as {client.user}') #Prints a Ready Message

@client.event
async def on_message(message):
    global current_question, current_answer
    if message.author == client.user:
        return

    if message.content.startswith('!trivia'): #Sets up the !trivia as a command to generate a question in the discord server
        questions = await fetch_trivia()
        if questions:
            for question in questions:
                current_question = question['question']
                current_answer = question['correct_answer']
                await message.channel.send(f"Category: {question['category']}\nQuestion: {html.unescape(question['question'])}\nReply with 'True' or 'False'.")
                await asyncio.sleep(15)
        else:
            await message.channel.send("Please try again later.")

    elif current_question and message.content in ['True', 'False']: #Looks for True or False and respones accordingly 
        if message.content == current_answer:
            await message.channel.send("Correct")
            update_score(str(message.author), 1)
        else:
            await message.channel.send("Incorrect")
        current_question = None
        current_answer = None

    elif message.content.startswith('!leaderboard'): #Makes it display leaderboard that would be stored in the data.json file
        lb = get_leaderboard()
        if lb:
            leaderboard_message = "\n".join([f"{entry['name']}: {entry['score']}" for entry in lb])
            await message.channel.send(f"Leaderboard:\n{leaderboard_message}")
        else:
            await message.channel.send("Leaderboard is empty.") #Will display if there is no questions anwsered so far

client.run(TOKEN)
