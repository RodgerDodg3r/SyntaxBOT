import discord
from discord.ext import commands

from utilities.json_handler import *

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        data = load_json("config.json")
        self.message_id = get_value(data, "ping_message_id")
        self.ping_role = get_value(data, "ping_role_id")
    
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        message_id = payload.message_id
        emoji = str(payload.emoji)
        guild_id = payload.guild_id
        if (user_id == self.bot.user.id):
            return
        if (message_id != self.message_id):
            return
        if (emoji != "✅"):
            return
        guild = self.bot.get_guild(guild_id)
        if (guild is None):
            return
        role = guild.get_role(self.ping_role)
        if (role is None):
            return

        member = guild.get_member(user_id)
        if (member is None):
            return
            
        embed = discord.Embed(
            title="🔔 Otrzymano rangę Ping!",
            description=(
                "Teraz będziesz **powiadamiany o nowych livestreamach!** 🎥\n\n"
                "Jeśli chcesz przestać otrzymywać powiadomienia, po prostu usuń rolę **Ping**."
            ),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await member.add_roles(role, reason="Accepted rules")
        await member.send(embed=embed)
    


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))