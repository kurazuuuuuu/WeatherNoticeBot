import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
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
    response, today_report, tomorrow_report = weather_report_response(user_id)

    message = f"""
        {today_report["date"]}の{today_report["area"]}の天気は{today_report["weather"]}です。
        現在の気温は{today_report["temp"]}度です。
        明日({tomorrow_report["date"]})の天気は{tomorrow_report["weather"]}で、最高気温は{tomorrow_report["temp_max"]}度、最低気温は{tomorrow_report["temp_min"]}度です。
        明日の降水確率は{tomorrow_report["pops"]}%です。
    """

    embed = discord.Embed(
        title=f"{user_mention} | 現在の天気情報",
        color=discord.Color.green()
    )
    embed.add_field(name="今日の気象情報", value=message, inline=True)
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