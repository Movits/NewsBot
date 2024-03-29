# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

async def get_articles(country):
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}&pageSize=1'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles')
    else:
        return None

def format_news(news_dict):
    title = news_dict['title']
    url = news_dict['url']
    return f"[{title}]({url})"

@bot.command()
async def news(ctx):
    print("News command received")

    brazil_articles = await get_articles("br")
    argentina_articles = await get_articles("ar")
    world_articles = await get_articles("us")

    try:
        news_msg = ""

        if brazil_articles:
            response_brazil = brazil_articles
            brazil_title = response_brazil[0].get('title', 'N/A')
            brazil_url = response_brazil[0].get('url', 'N/A')
            news_msg += f"[**{brazil_title}**]({brazil_url})\n\n"
        else:
            raise KeyError('articles')

        if argentina_articles:
            response_argentina = argentina_articles
            argentina_title = response_argentina[0].get('title', 'N/A')
            argentina_url = response_argentina[0].get('url', 'N/A')
            news_msg += f"[**{argentina_title}**]({argentina_url})\n\n"
        else:
            raise KeyError('articles')

        if world_articles:
            response_world = world_articles
            world_title = response_world[0].get('title', 'N/A')
            world_url = response_world[0].get('url', 'N/A')
            news_msg += f"[**{world_title}**]({world_url})"
        else:
            raise KeyError('articles')

        embed = discord.Embed(description=news_msg)
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Error fetching news: {e}")
        print("Brazil response:", brazil_articles)
        print("Argentina response:", argentina_articles)
        print("World response:", world_articles)
        await ctx.send("Error fetching news. Please try again later.")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
