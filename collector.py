from telethon import TelegramClient
import re
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

channel_username = "persianvpnhub"  # بدون @

patterns = r"(vmess://\S+|vless://\S+|trojan://\S+|ss://\S+)"

MAX_CONFIGS = 40

async def main():
    async with TelegramClient('session', api_id, api_hash) as client:
        extracted = []

        # خواندن 30 پیام آخر
        async for msg in client.iter_messages(channel_username, limit=30):
            if msg.text:
                found = re.findall(patterns, msg.text)
                for f in found:
                    cleaned = f.strip()
                    if cleaned not in extracted:
                        extracted.append(cleaned)

        # اگر فایل قبلی وجود دارد، آن را بخوان
        existing = []
        if os.path.exists("configs.txt"):
            with open("configs.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and line not in extracted:
                        existing.append(line)

        # ترکیب جدیدها + قدیمی‌ها
        combined = extracted + existing

        # فقط 40 تای اول نگه‌داشته شود
        final_list = combined[:MAX_CONFIGS]

        # نوشتن فایل
        with open("configs.txt", "w", encoding="utf-8") as file:
            for config in final_list:
                file.write(config + "\n")

with TelegramClient('session', api_id, api_hash) as client:
    client.loop.run_until_complete(main())
