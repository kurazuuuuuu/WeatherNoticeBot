import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import supabase
from supabase_access import get_user_data
from jma_weather_api import get_jma_data
from google_gemini import weather_report_response

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

bot = commands.Bot(
    command_prefix="/", 
    intents=intents,
    activity=discord.Game("お天気観察")
)

def embed_weather_today(user_id, user_mention):
    user_data = get_user_data(user_id)
    area_code = user_data["area_code"]

    response, jma_data = weather_report_response(user_id)

    embed = discord.Embed(
        title=f"{user_mention} | 現在の天気情報",
        color=discord.Color.green()
    )
    embed.add_field(name="今日の気象情報", value=jma_data[0], inline=False)
    embed.add_field(name="AIからの一言", value=response, inline=True)
    embed.set_footer(text="気象庁のデータを元に生成しています。")

    return embed

@bot.event
async def on_ready():
    await bot.tree.sync()  # 自動生成された tree を使う
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content == "今日の天気":
        embed = embed_weather_today(message.author.id, message.author.mention)
        await message.channel.send(embed=embed)

bot.run(TOKEN)