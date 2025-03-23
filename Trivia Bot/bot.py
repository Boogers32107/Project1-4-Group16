import discord
import asyncio
import aiohttp
import html
from Leaderboard_1 import update_score, get_leaderboard

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_question = None
current_answer = None

async def fetch_trivia():
    url = 'https://opentdb.com/api.php?amount=1&category=15&type=boolean'
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

    if message.content.startswith('!trivia'):
        questions = await fetch_trivia()
        if questions:
            for question in questions:
                current_question = question['question']
                current_answer = question['correct_answer']
                await message.channel.send(f"Category: {question['category']}\nQuestion: {html.unescape(question['question'])}\nReply with 'True' or 'False'.")
                await asyncio.sleep(15)
        else:
            await message.channel.send("Please try again later.")

    elif current_question and message.content in ['True', 'False']:
        if message.content == current_answer:
            await message.channel.send("Correct")
            update_score(str(message.author), 1)
        else:
            await message.channel.send("Incorrect")
        current_question = None
        current_answer = None

    elif message.content.startswith('!leaderboard'):
        lb = get_leaderboard()
        if lb:
            leaderboard_message = "\n".join([f"{entry['name']}: {entry['score']}" for entry in lb])
            await message.channel.send(f"Leaderboard:\n{leaderboard_message}")
        else:
            await message.channel.send("Leaderboard is empty.")

client.run(TOKEN)