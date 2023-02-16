import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
import story


load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def zkillstory(ctx, url, tokens=500, topic="An EVE Online story"):
    async with ctx.channel.typing():
        zkillstory = story.Story(zkill_link=url)
        zkillstory = await story.populate_story(zkillstory)

        zkillstory.response = await story.get_story(zkillstory, tokens=int(tokens), topic=topic)
        zkillstory.response += '\n\nAnd that was just another day in New Eden'
        response = zkillstory.response
        
        await ctx.send(response)

bot.run(DISCORD_TOKEN)