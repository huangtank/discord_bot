import discord
import datetime
import pytz
from discord.ext import commands, tasks

class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TIMEZONE = pytz.timezone('Asia/Shanghai')
        self.統測 = 1219296088729849968
        self.模考 = 1247180660502827118
        self.update_countdown_daily.start()

    async def countdown_daily(self):
        target_date = datetime.datetime(2025, 4, 25, 22, 59, 59, tzinfo=pytz.UTC)
        current_date = datetime.datetime.now(self.TIMEZONE)
        time_difference = target_date - current_date
        target_date_simulation = datetime.datetime(2025, 2, 16, 22, 59, 59, tzinfo=pytz.UTC)
        time_difference_simulation = target_date_simulation - current_date
        now = datetime.datetime.now(self.TIMEZONE)
        print('更改成功')
        print(now)
        print(f'統測剩餘{time_difference.days}天')
        print(f'三模剩餘{time_difference_simulation.days}天')
        if time_difference.days <= 0:
            await self.bot.get_channel(self.統測).send("祝各位統測順利！")
            await self.bot.get_channel(self.統測).send("寫快！但不要粗心阿")
            await self.bot.get_channel(self.統測).edit(name="祝各位統測順利！")
        else:
            days = time_difference.days
            await self.bot.get_channel(self.統測).edit(name=f"統測倒數{days}天")

        if time_difference_simulation.days <= 0:
            await self.bot.get_channel(self.模考).send("祝各位模考順利！")
            await self.bot.get_channel(self.模考).edit(name="祝各位模考順利！")
        else:
            days = time_difference_simulation.days
            await self.bot.get_channel(self.模考).edit(name=f"三模倒數{days}天")

    @tasks.loop(hours=24)
    async def update_countdown_daily(self):
        await self.countdown_daily()  # 每天 UTC+8 00:00 更新一次

    @update_countdown_daily.before_loop
    async def before_update_countdown_daily(self):
        now = datetime.datetime.now(self.TIMEZONE)
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=12)
        midnight = datetime.datetime.combine(tomorrow, datetime.time.min)
        # 等待到 UTC+8 00:00
        print(now)
        print("start")
        print(tomorrow)
        await discord.utils.sleep_until(tomorrow)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.countdown_daily()
        await update_countdown_daily.start()
        print('Countdown cog is ready')

async def setup(bot):
    await bot.add_cog(Countdown(bot))