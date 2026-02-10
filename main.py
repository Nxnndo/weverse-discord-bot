import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1470655437182599201  

PRODUCT_URLS = [
    "https://shop.weverse.io/en/shop/USD/artists/2/sales/54380",
    "https://shop.weverse.io/en/shop/USD/artists/2/sales/54379"
]

CHECK_INTERVAL = 180  # seconds

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def is_in_stock(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        button = soup.find("button")
        if button and "sold out" not in button.text.lower():
            return True
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return False

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    while True:
        for url in PRODUCT_URLS:
            print(f"Checking {url}")
            if is_in_stock(url):
                await channel.send(
                    f"@everyone 🔔 **BTS item is BACK IN STOCK!**\n👉 {url}"
                )
                await client.close()
                return

        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!test":
        await message.channel.send("@everyone 🔔 **TEST ALERT** — bot is working!")

client.run(TOKEN)

