import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime, time
import logging
from script import get_cleaner

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

taipei_tz = pytz.timezone('Asia/Taipei')

class CleanerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        await self.add_cog(CleanerCog(self))
        self.get_cog('CleanerCog').weekly_check.start()

class CleanerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @tasks.loop(hours=168)
    async def weekly_check(self):
        try:
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                date, sweep, mop = get_cleaner()
                await channel.send(f"Date: {date}\n🧹掃地+倒垃圾: {sweep}\n🧺拖地+整理大桌子: {mop}")
                print("Finished sending message")
        except Exception as e:
            logging.error(f"Error in weekly_check: {e}")

    @weekly_check.before_loop
    async def before_weekly_check(self):
        await self.bot.wait_until_ready()
        logging.info("Starting the scheduled weekly cleaner check.")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'{self.bot.user.name} is online and ready!')

if __name__ == "__main__":
    cleaner_bot = CleanerBot()
    cleaner_bot.run(TOKEN)
