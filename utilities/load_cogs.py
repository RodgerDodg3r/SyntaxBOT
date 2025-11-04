import os

async def load_cogs(bot):
    print("Loading cogs...")
    for file in os.listdir("./Cogs"):
        if not file.endswith('.py'):
            continue
        
        cog = f"Cogs.{file[:-3]}"
        try:
            await bot.load_extension(cog)
            print(f"Cog loaded: {cog}")
        except Exception as e:
            print(f"An error occurred while loading {cog}: {e}")