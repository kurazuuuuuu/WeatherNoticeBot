import requests
import json
import datetime

parent_area_code = "400000"  # 福岡県
area_code = "400010"  # 福岡市

# 気象庁データの取得

def get_jma_data(parent_area_code, area_code):
    jma_overview_url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{parent_area_code}.json"
    jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{parent_area_code}.json"

    jma_response = requests.get(jma_url).json()
    jma_overview_response = requests.get(jma_overview_url).json()
    today_overview_report = jma_overview_response["text"].replace("\n", " ")

    print("Get from JMA URL:", jma_url)
    print("Get from JMA Overview URL:", jma_overview_url)

    today_report = {}
    tomorrow_report = {}

    for i in range(len(jma_response[0]["timeSeries"][0]["areas"])):
        if jma_response[0]["timeSeries"][0]["areas"][i]["area"]["code"] == area_code:
            area_data = jma_response[0]["timeSeries"][0]["areas"][i]
            time_defines = jma_response[0]["timeSeries"][0]["timeDefines"]

            today_report = {
                "date": time_defines[0][:10],
                "area": area_data["area"]["name"],
                "weather": area_data["weathers"][0],
                "temp": jma_response[0]["timeSeries"][2]["areas"][i]["temps"][0],
            }

            tomorrow_report = {
                "date": time_defines[1][:10],
                "area": area_data["area"]["name"],
                "weather": area_data["weathers"][1],
                "temp_max": jma_response[1]["timeSeries"][1]["areas"][i]["tempsMax"][1],
                "temp_min": jma_response[1]["timeSeries"][1]["areas"][i]["tempsMin"][1],
                "pops": jma_response[1]["timeSeries"][0]["areas"][i]["pops"][1],
            }
            break

    today_report["weather"] = today_report["weather"].replace("　", " ")
    tomorrow_report["weather"] = tomorrow_report["weather"].replace("　", " ")
    
    return today_report, tomorrow_report, today_overview_report