import discord
from discord.ext import commands

from utilities.json_handler import *


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        data = load_json("config.json")
        channel_id = get_value(data, "logs_channel_id")
        self.logs_channel = self.bot.get_channel(channel_id)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        before_roles = set(before.roles)
        after_roles = set(after.roles)
        added_roles = after_roles - before_roles
        
        #Geting a moderator
        moderator = None
        try:
            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=5):
                if entry.target.id == after.id:
                    moderator = entry.user
                    break
        except Exception as e:
            print(f"Error fetching audit logs: {e}")

        if (added_roles):
            for role in added_roles:
                print(f"+: {role}")
                embed = discord.Embed(
                    title = "✅ Nadano rangę",
                    description= (
                        f"**👤 Użytknownik: ** {after.mention}\n"
                        f"**🥇 Ranga: ** {role.mention}\n"
                        f"**🕒 Czas:** <t:{int(discord.utils.utcnow().timestamp())}:R>\n"
                        f"**👨‍💻 Moderator: ** {moderator.mention}"
                    ),
                    color = discord.Color.green()
                )
            await self.logs_channel.send(embed=embed)
            
        removed_roles = before_roles - after_roles
        if (removed_roles):
            for role in removed_roles:
                print(f"X : {role}")
                embed = discord.Embed(
                    title = "⛔ Zabrano rangę",
                    description= (
                        f"**👤 Użytknownik: ** {after.mention}\n"
                        f"**🥇 Ranga: ** {role.mention}\n"
                        f"**🕒 Czas:** <t:{int(discord.utils.utcnow().timestamp())}:R>\n"
                        f"**👨‍💻 Moderator: ** {moderator.mention}"
                    ),
                    color = discord.Color.red()
                )
            await self.logs_channel.send(embed=embed)
        
        print("3")
    
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (message.author.bot):
            return
        
        embed = discord.Embed(
            title = f"❌ Wiadomość została usunięta!",
            description= f"**📍 Kanał: ** {message.channel.mention}\n**👤 Użytkownik: ** {message.author.mention}\n**🕐 Czas: ** <t:{int(discord.utils.utcnow().timestamp())}:R>\n\n**Usunięta wiadomość: ** `{message.content}`",
            color = discord.Color.purple()    
        )
        
        data = load_json("config.json")
        channel_id = get_value(data, "logs_channel_id")
        channel = self.bot.get_channel(channel_id)
        
        
        await channel.send(embed=embed)
        
    
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (before.author.id == self.bot.user.id):
            return
    
        if (before.content == after.content):
            return
    
        embed = discord.Embed(
            title= f"📝 Wiadomość została edytowana!",
            description= f"**📍 Kanał: ** {after.channel.mention}\n**👤 Użytkownik: ** {after.author.mention}\n**🕐 Czas: ** <t:{int(after.edited_at.timestamp())}:R>\n\n**Przed: ** `{before.content}`\n**Po: ** `{after.content}`",
            color= discord.Color.purple()
        )
        
                
        data = load_json("config.json")
        channel_id = get_value(data, "logs_channel_id")
        channel = self.bot.get_channel(channel_id)
        
        await channel.send(embed=embed)
    





async def setup(bot):
    await bot.add_cog(Logs(bot))