import json
from discord.ext import commands
from main import client
from discord.utils import get
from files.embedDictionary import dictionary


class OnRawReactionAdd(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        channel = payload.channel_id
        member = payload.member
        reaction = payload.emoji
        guild = client.get_guild(payload.guild_id)

        if channel == 890138529940795443:
            if not member.bot:
                emoji = client.get_emoji(891105594612797450)
                if str(reaction) == str(emoji):
                    role = get(guild.roles,name="Unit")
                    await member.add_roles(role)
                    
        if channel == 905888377071616090:
            if not member.bot:
                channel = get(guild.channels,id=channel)
                for emoji,role in dictionary.items():
                    if str(reaction) == str(emoji):
                        role = get(guild.roles,name=role)
                        await member.add_roles(role)

        
        with open("files/captainHalls.json") as file:
            captainHalls = json.load(file)

        for gemi,id in captainHalls.items():
            if channel == id:
                if str(reaction) == "🚀":
                    if not member.bot:
                        role = get(guild.roles,name=f"🚀{gemi} - Captain" )
                        await member.add_roles(role)
                        gemi = str(f"{gemi}").lower()
                        channel = get(guild.channels,name=f"🚀{gemi}-hall")
                        await channel.delete()


def setup(client):
    client.add_cog(OnRawReactionAdd(client))

