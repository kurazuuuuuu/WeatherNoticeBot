import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from embed import embed_weather_today, embed_scheduling_morning, embed_scheduling_evening
from supabase_access import get_user_data, get_notice_users, save_user_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

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

@bot.event
async def on_ready():
    await bot.tree.sync()  # 自動生成された tree を使う
    print(f"{bot.user.name}くん！起動完了！")
    schedule_jobs()   

def schedule_jobs():
    scheduler.add_job(lambda: bot.loop.create_task(send_report("morning")), 'cron', hour=13, minute=26)
    scheduler.add_job(lambda: bot.loop.create_task(send_report("evening")), 'cron', hour=18, minute=0)
    scheduler.start() 

@bot.event
async def send_report(time):
    notice_users = get_notice_users()
    print("[Notice Users]:", notice_users) #debug

    for user in notice_users:
        if time == "morning":
            embed = embed_scheduling_morning(user, f"<@{user}>")
            await bot.get_user(user).send(embed=embed)
        elif time == "evening":
            embed = embed_scheduling_evening(user, f"<@{user}>")
            await bot.get_user(user).send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content == "test":
        send_report("morning")

@bot.tree.command(name="weather", description="今日と明日の天気を教えてくれるよ！")
async def weather (interaction: discord.Interaction):
    embed = embed_weather_today(interaction.user.id, interaction.user.mention)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="setup", description="天気情報を取得する地域を設定するよ！")
async def setting(interaction: discord.Interaction, parent_area_code: int, area_code: int):
    await interaction.response.send_message(f"地域コードを{parent_area_code}と{area_code}に設定しました。", ephemeral=True)

@bot.tree.command(name="notice", description="天気情報を自動で通知するか設定できるよ！")
async def notice(interaction: discord.Interaction):
    user_data = get_user_data(interaction.user.id)
    notice_users = get_notice_users()

    if user_data["notice"] == True:
        await interaction.response.send_message("通知をオフにしました！", ephemeral=True)
        user_data["notice"] = False
        save_user_data(interaction.user.id, user_data)

    else:
        await interaction.response.send_message("通知をオンにしました！", ephemeral=True)
        user_data["notice"] = True
        save_user_data(interaction.user.id, user_data)


@bot.tree.command(name="help", description="このボットの使い方を教えてくれるよ！")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("/setting <親地域コード> <地域コード>で天気情報を取得する地域を設定できます。\n"
        "/weatherで今日と明日の天気を教えてくれます。\n")

bot.run(TOKEN)

