import requests
import json
import datetime

area_code = "400000"  # 福岡県

# 気象庁データの取得

def get_jma_data(area_code):
    jma_overview_url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{area_code}.json"
    jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

    jma_response = requests.get(jma_url).json()

    # 短期予報（当日の気温）を取得
    short_term_forecast = jma_response[0]["timeSeries"]
    temps_today = {}
    for series in short_term_forecast:
        for area in series["areas"]:
            if area["area"]["name"] == "福岡":
                if "temps" in area:
                    temps_today = dict(zip(series["timeDefines"], area["temps"]))

    # 短期予報（当日の降水確率）を取得
    short_term_pops = []
    for series in short_term_forecast:
        if "pops" in series["areas"][0]:  # "pops"があるseriesを探す
            short_term_pops = series["areas"][0]["pops"]
            break

    jma_overview_response = requests.get(jma_overview_url).json()

    jma_data = {}

    # 福岡市のデータだけ取り出す
    # 週間予報の情報は、配列の2番目の timeSeries に入ってる
    week_forecast = jma_response[1]["timeSeries"]

    # 日付一覧
    dates = week_forecast[0]["timeDefines"]

    # 降水確率
    pops = week_forecast[0]["areas"][0]["pops"]

    # 気温情報（最低・最高）
    temps_min = week_forecast[1]["areas"][0]["tempsMin"]
    temps_max = week_forecast[1]["areas"][0]["tempsMax"]

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    for i in range(len(dates)):
        date = dates[i][:10]  # "2025-04-28T00:00:00+09:00" → "2025-04-28"
        # デフォルトは週間予報の降水確率
        pop = pops[i] if pops[i] else "データなし"

        # 今日の日付なら短期予報の降水確率を優先
        if date == today_str and short_term_pops:
            valid_pops = [int(p) for p in short_term_pops if p.isdigit()]
            if valid_pops:
                pop = str(max(valid_pops))

        # デフォルトは週間予報のデータ
        temp_min = temps_min[i]
        temp_max = temps_max[i]

        # 今日の日付なら短期予報の気温を優先
        if date == today_str and temps_today:
            temp_min = temps_today.get(list(temps_today.keys())[0], "データなし")
            temp_max = temps_today.get(list(temps_today.keys())[1], "データなし")

        # どちらかが空ならスキップ
        if temp_min == "" or temp_max == "":
            continue

        jma_data[i] = f"{date} - 最低気温: {temp_min}度, 最高気温: {temp_max}度, 降水確率: {pop}%"

    jma_overview_data = {
        "date": jma_overview_response["reportDatetime"],
        "area": jma_overview_response["targetArea"],
        "text": jma_overview_response["text"],
    }

    return jma_data, jma_overview_data