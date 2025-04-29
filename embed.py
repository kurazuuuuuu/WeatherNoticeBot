import discord
from google_gemini import weather_report_response, weather_report_response_tomorrow
from jma_weather_api import get_jma_data

def embed_scheduling_morning(user_id, user_mention):
    response, today_report, tomorrow_report = weather_report_response(user_id)

    message = f"""
        {today_report["date"]}の{today_report["area"]}の天気は{today_report["weather"]}です。
        現在の気温は{today_report["temp"]}度です。
    """

    embed = discord.Embed(
        title=f"{user_mention}さん！おはようございます！",
        color=discord.Color.green()
    )
    embed.add_field(name="今日の気象情報", value=message, inline=True)
    embed.add_field(name="AIからの一言", value=response, inline=True)
    embed.set_footer(text="気象庁のデータを元に生成しています。")

    return embed

def embed_scheduling_evening(user_id, user_mention):
    response, today_report, tomorrow_report = weather_report_response_tomorrow(user_id)

    message = f"""
        明日({tomorrow_report["date"]})の天気は{tomorrow_report["weather"]}で、最高気温は{tomorrow_report["temp_max"]}度、最低気温は{tomorrow_report["temp_min"]}度です。
        明日の降水確率は{tomorrow_report["pops"]}%です。
    """

    embed = discord.Embed(
        title=f"{user_mention}さん！お疲れ様です。",
        color=discord.Color.green()
    )
    embed.add_field(name="明日の気象情報", value=message, inline=True)
    embed.add_field(name="AIからの一言", value=response, inline=True)
    embed.set_footer(text="気象庁のデータを元に生成しています。")

    return embed

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