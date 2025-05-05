import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from embed import embed_weather_today, embed_scheduling_morning, embed_scheduling_evening
from supabase_access import get_user_data, get_notice_users, save_user_data
import schedule
import time
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
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

@bot.event
async def send_report(time):
    notice_users = get_notice_users()
    print("[Notice Users]:", notice_users) #debug

    for user_id in notice_users:
        try:
            if time == "morning":
                embed = embed_scheduling_morning(user_id, f"<@{user_id}>")
            elif time == "evening":
                embed = embed_scheduling_evening(user_id, f"<@{user_id}>")
            else:
                continue

            user = await bot.fetch_user(user_id)
            await user.send(embed=embed)
            print(f"Sent {time} report to {user.name}")

        except Exception as e:
            print(f"Failed to send DM to {user_id}: {e}")

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
    
def schedule_send_report(time_str):
    asyncio.run_coroutine_threadsafe(send_report(time_str), bot.loop)

schedule.every().day.at("07:00").do(lambda: schedule_send_report("morning"))
schedule.every().day.at("18:00").do(lambda: schedule_send_report("evening"))


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

import threading
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

bot.run(TOKEN)
