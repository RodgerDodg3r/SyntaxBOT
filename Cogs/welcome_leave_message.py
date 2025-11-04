import discord
from discord.ext import commands

from utilities.json_handler import *

class WelcomeLeaveMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="> 🧠 Nowy użytkownik połączył się z serwerem",
            description=(
                f"Witaj, {member.mention}!\n\n"
                f"Cieszymy się, że dołączyłeś/aś do **{member.guild.name}** 💻\n\n"
                "▪️ Przeczytaj regulamin w <#1434034956836802651>\n"
                "▪️ Wybierz swoje role w <#1434941589108822026>\n"
                "▪️ Dołącz do dyskusji w <#1434036507009876148>\n\n"
                "Zespół **Syntax** życzy udanej kompilacji! ⚙️"
            ),
            color=discord.Color.green()  # pasuje do TokyoNight
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Syntax • system powitalny", icon_url=member.guild.icon.url if member.guild.icon else None)
        embed.timestamp = discord.utils.utcnow()
        
        
        config = load_json("config.json")
        welcome_channel = get_value(config, "welcome_channel_id")
        channel = self.bot.get_channel(welcome_channel)
        if (channel is None):
            return
        
        await channel.send(embed=embed)
        
        
    
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="> ⚙️ Użytkownik opuścił serwer",
            description=(
                f"Użytkownik **{member.name}** zakończył sesję na **{member.guild.name}**.\n\n"
                "🧩 Dzięki za wspólny czas i wkład w społeczność.\n"
                "📡 Mamy nadzieję, że jeszcze kiedyś się zobaczymy.\n\n"
                "— System **Syntax** zamknął połączenie 💻"
            ),
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Syntax • system pożegnalny", icon_url=member.guild.icon.url if member.guild.icon else None)
        embed.timestamp = discord.utils.utcnow()

        config = load_json("config.json")
        welcome_channel = get_value(config, "leave_channel_id")
        channel = self.bot.get_channel(welcome_channel)
        if (channel is None):
            return


        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeLeaveMessage(bot))