import os

import discord
from discord.ext import commands
import random
from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='-', intents=intents)

# // BOT events //
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(conditional_loop())


# // Bot commands //
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def hau(ctx):
    rnum = random.randint(1, 2)
    if rnum == 1:
        await ctx.send("Better than ever!")
    else:
        await ctx.send("Good I suppose.")

@bot.command()
@commands.has_permissions(administrator=True)
async def createrole(ctx, role_name, hex_color):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        await ctx.send(f"'{role_name}' already exists.")
    else:

        hex_color = hex_color.replace('#', "")
        color = discord.Colour(int(hex_color, 16))

        await guild.create_role(
            name=role_name, 
            color=color,
            hoist=True,
            )
        await ctx.send(f"**'{role_name}'** has been created.")

@bot.command()
@commands.has_permissions(administrator=True)
async def giverole(ctx, role_name, member: discord.Member):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"**{member.mention}** has been given the role **'{role_name}'**.")
    else:
        await ctx.send(f"'{role_name}' does not exist.")

@bot.command()
@commands.has_permissions(administrator=True)
async def deleterole(ctx, role_name):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        await role.delete()
        await ctx.send(f"**'{role_name}'** has been deleted.")
    else:
        await ctx.send(f"'{role_name}' does not exist.")

async def conditional_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(1477283105764147412)
    if channel is None:
        print("Channel not found.")
        return

    while not bot.is_closed():
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        current_time = f"{hour}:{minute}"
        if current_time == "13:48":
            await channel.send("It's 1:48 PM!")
        await asyncio.sleep(5)  # Check every minute

# Alarms
@bot.command()
async def setalarm(ctx, year: str, month: str, day: str, hour: str, minute: str, *, text: str):
    
    try:
        alarm_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
        now = datetime.now()
        
        if alarm_time <= now:
            await ctx.send(f"The time {alarm_time} is already past. Alarm will trigger immediately.")
            await ctx.send(text)
            return
        
        diff = (alarm_time - now).total_seconds()
        await ctx.send(f"Alarm set for {alarm_time}.")
        
        await asyncio.sleep(diff)
        await ctx.author.send(f"**⏰ Alarm!**  {text}")

    except ValueError:
        await ctx.send("Invalid date or time format. Please use numbers in YYYY MM DD HH MM.")

# DMs
@bot.command()
async def dm(ctx, member: discord.Member, *, message: str):
    await member.send(message)
    await ctx.send(f"Message sent to {member.mention}.")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)