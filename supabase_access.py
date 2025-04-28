from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_user_data(user_id): # Supabase初期化
    user_data = {
        "discord_id": user_id,
        "parent_area_code": 400000, # 福岡県
        "area_code": 400010, # 福岡市
    }
    supabase.table("users").upsert(user_data).execute()
    print("[Initialize]:", user_data) #debug

def get_user_data(user_id): # Supabase取得・初期化
    user_data = supabase.table("users").select("*").eq("discord_id", user_id).execute()

    if len(user_data.data) == 0:
        initialize_user_data(user_id)

    # 再度取得
    user_data = supabase.table("users").select("*").eq("discord_id", user_id).execute()

    print("[Get]:", user_data) #debug

    return user_data.data[0]

def save_user_data(user_id, user_data):# Supabase保存
    supabase.table("users").update(
        {
            "parent_area_code": user_data["parent_area_code"],
            "area_code": user_data["area_code"],
        }
    ).eq("discord_id", user_id).execute()

    print("[Save]:", user_data) #debug