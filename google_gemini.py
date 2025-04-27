import os
from dotenv import load_dotenv
import google.generativeai as genai
from jma_weather_api import get_jma_data
# from supabase_access import get_user_data

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
    # area_code = get_user_data(user_id)
    area_code = "400000"  # 福岡県
    jma_data, jma_overview_data = get_jma_data(area_code)

    jma_area = jma_overview_data["area"]


    prompt = ( f"""
              以下は気象庁から取得した{jma_area}の天気情報です。
              今日から３日間の気温・降水確率情報はこちらです＝＞{jma_data}
              気象庁からの概要はこちらです＝＞{jma_overview_data}
              必ず今日の天気について、服装や出かける際の注意など明るい雰囲気で一言お願いします。
              JSON形式ではなくて大丈夫です。必ずその一言だけを返してください。
    """
    )

    response = generate_response(prompt)

    return response, jma_data