import discord
import os
from discord.ext import commands
from utilities.json_handler import *
from utilities.load_cogs import *

intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True

#Bot init
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    for guild in bot.guilds:
        print(f"  - {guild.name} (ID: {guild.id})")
    
    print(f"Loaded cogs: {list(bot.cogs.keys())}")
    print(f"Registered commands: {[cmd.name for cmd in bot.tree.get_commands()]}")
    
    guild_id = 1120125445476724737
    
    try:
        # Clear guild-specific commands first
        bot.tree.clear_commands(guild=discord.Object(id=guild_id))
        
        # Copy global commands to guild
        bot.tree.copy_global_to(guild=discord.Object(id=guild_id))
        
        # Sync to guild
        synced = await bot.tree.sync(guild=discord.Object(id=guild_id))
        print(f"Synced {len(synced)} command(s) to guild {guild_id}")
        for cmd in synced:
            print(f"  - {cmd.name}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
async def main():
    async with bot:
        data = load_json("./token.json")
        token = get_value(data, "token")
        print("Starting to load cogs...")
        await load_cogs(bot)
        print("Cogs loaded successfully!")
        print("Starting bot...")
        await bot.start(token)
        
        



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())