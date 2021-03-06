import discord
import os
import json
from datetime import datetime
import requests
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand

from keep_alive import keep_alive

TOKEN = os.environ["TOKEN"]
# serverURL = os.environ["serverURL"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
INSTAGRAM_USERNAME = os.environ['INSTAGRAM_USERNAME']


client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
intents = discord.Intents.all()
intents.members = True

slash = SlashCommand(client,sync_commands=True)
guildID = [857253101199425598]
embedColor = 0x8d42f5

keep_alive()

@client.event
async def on_ready():
	print("On Mars Way!")
	await client.change_presence(status=discord.Status.online,activity=discord.Game("🚀 On My Way To Mars!"))

@client.command()
async def rolver(ctx):
    role = get(ctx.guild.roles,name="Guest")
    for member in client.get_all_members():
        await member.add_roles(role)

		
cogs = ["cogs.abilityTree","cogs.addLink","cogs.addPointToSpaceShip","cogs.clear","cogs.createRole","cogs.createSpaceShip","cogs.deleteLink","cogs.destroySpaceShip","cogs.help","cogs.instagram","cogs.level","cogs.showLinks","cogs.modifier","cogs.onMemberJoin","cogs.onMessage","cogs.onRawReactionRemove","cogs.onReactionAdd","cogs.onVoiceStateUpdate","cogs.personalPoint","cogs.rank","cogs.voiceChannel"]

for cog in cogs:
	client.load_extension(cog)

client.run(TOKEN)

