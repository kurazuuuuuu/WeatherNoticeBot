import os
from dotenv import load_dotenv
import google.generativeai as genai
from jma_weather_api import get_jma_data
from supabase_access import get_user_data

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("APIキーが正しく読み込まれていません。")

genai.configure(api_key=GOOGLE_API_KEY)
gemini = genai.GenerativeModel("gemini-2.0-flash")

def generate_response(prompt):
    response = gemini.generate_content(prompt)
    return response.text

def weather_report_response(user_id):
    user_data = get_user_data(user_id)

    today_report, tomorrow_report, today_overview_report = get_jma_data(user_data["parent_area_code"], user_data["area_code"])

    prompt = ( f"""
              以下は気象庁から取得した{today_report["area"]}の天気情報です。
              今日の天気・気温の情報はこちらです＝＞{today_report}
              明日の天気・最高気温・最低気温・降水確率の情報はこちらです＝＞{tomorrow_report}
              気象庁からの概要はこちらです＝＞{today_overview_report}
              必ず、今日の天気について、服装や出かける際の注意など明るい雰囲気で絵文字なども使いながら一言お願いします。
              JSON形式ではなくて大丈夫です。必ずその一言だけを返してください。
    """
    )

    response = generate_response(prompt)

    return response, today_report, tomorrow_report

def weather_report_response_tomorrow(user_id):
    user_data = get_user_data(user_id)

    today_report, tomorrow_report, today_overview_report = get_jma_data(user_data["parent_area_code"], user_data["area_code"])

    prompt = ( f"""
              以下は気象庁から取得した{today_report["area"]}の天気情報です。
              今日の天気・気温の情報はこちらでした＝＞{today_report}
              明日の天気・最高気温・最低気温・降水確率の情報はこちらです＝＞{tomorrow_report}
              気象庁からの概要はこちらです＝＞{today_overview_report}
              必ず、明日の天気について、服装や出かける際の注意など明るい雰囲気で絵文字なども使いながら一言お願いします。
              JSON形式ではなくて大丈夫です。必ずその一言だけを返してください。
    """
    )

    response = generate_response(prompt)
    return response, today_report, tomorrow_report