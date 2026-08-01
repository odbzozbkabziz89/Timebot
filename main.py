import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

# ساخت ایونت‌لوپ
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import Client
from pyrogram.errors import FloodWait

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

TIMEZONE = ZoneInfo("Asia/Tehran")

app = Client(
    "name_time_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# نام اصلی شما که می‌خواهید کنار ساعت باشد
MY_NAME = "⚡️"

# تابع تبدیل اعداد به فونت جذاب Double-Struck
def to_fancy_time(time_str: str) -> str:
    fancy_digits = {
        '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜',
        '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡', ':': ':'
    }
    return "".join(fancy_digits.get(char, char) for char in time_str)

async def update_name_loop():
    last_time = ""
    while True:
        try:
            # دریافت ساعت فعلی تهران
            now = datetime.now(TIMEZONE)
            raw_time = now.strftime("%H:%M")
            
            # تبدیل به فونت سفارشی
            fancy_time = to_fancy_time(raw_time)
            
            # فقط زمانی که دقیقه تغییر کند، first_name آپدیت می‌شود
            if fancy_time != last_time:
                new_first_name = f"{MY_NAME} {fancy_time}"
                
                # قرار دادن ترکیب اسم و ساعت روی first_name
                await app.update_profile(first_name=new_first_name)
                
                last_time = fancy_time
                print(f"First Name Updated to: {new_first_name}", flush=True)

        except FloodWait as e:
            print(f"FloodWait: Waiting for {e.value} seconds...", flush=True)
            await asyncio.sleep(e.value)
            
        except Exception as e:
            print(f"Error in loop: {e}", flush=True)
            await asyncio.sleep(5)

        # بررسی هر ۳۰ ثانیه
        await asyncio.sleep(30)

async def main():
    while True:
        try:
            async with app:
                print("Connected to Telegram!", flush=True)
                await update_name_loop()
        except Exception as e:
            print(f"Connection lost ({e}), reconnecting in 10 seconds...", flush=True)
            await asyncio.sleep(10)

if __name__ == "__main__":
    loop.run_until_complete(main())
