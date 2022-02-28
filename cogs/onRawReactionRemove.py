from turtle import onrelease
from discord.ext import commands
from main import client
from discord.utils import get
from files.embedDictionary import dictionary

class OnRawReactionRemove(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        channel = payload.channel_id
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        reaction = payload.emoji
        if channel == 905888377071616090:
            if not member.bot:
                channel = get(guild.channels,id=channel)
                for emoji,role in dictionary.items():
                    if str(reaction) == str(emoji):
                        role = get(guild.roles,name=role)
                        await member.remove_roles(role)

def setup(client):
    client.add_cog(OnRawReactionRemove(client))