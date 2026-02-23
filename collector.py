import requests
from bs4 import BeautifulSoup
import re
import os

CHANNEL_URL = "https://t.me/s/persianvpnhub"
MAX_MESSAGES = 30
MAX_CONFIGS = 40

patterns = r"(vmess://\S+|vless://\S+|trojan://\S+|ss://\S+)"

def fetch_messages():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(CHANNEL_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    messages = soup.find_all("div", class_="tgme_widget_message_text")

    # فقط 30 پیام آخر
    return messages[-MAX_MESSAGES:]

def extract_configs(messages):
    configs = []

    for msg in messages:
        text = msg.get_text(separator="\n")
        found = re.findall(patterns, text)

        for f in found:
            cleaned = f.strip()
            if cleaned not in configs:
                configs.append(cleaned)

    return configs

def load_existing():
    if not os.path.exists("configs.txt"):
        return []

    with open("configs.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_configs(configs):
    with open("configs.txt", "w", encoding="utf-8") as f:
        for c in configs:
            f.write(c + "\n")

def main():
    messages = fetch_messages()
    new_configs = extract_configs(messages)
    existing_configs = load_existing()

    # جدیدها اول
    combined = new_configs + [c for c in existing_configs if c not in new_configs]

    # فقط 40 تای اول
    final = combined[:MAX_CONFIGS]

    save_configs(final)

if __name__ == "__main__":
    main()
