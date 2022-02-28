from main import client
from discord.ext import commands
from discord.utils import get
from functions.userClass import User

class OnMemberJoin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        channel = client.get_channel(915299360202448978)
        await member.edit(nick="👁 WATCHER")
        role = get(guild.roles,name="Guest")
        await member.add_roles(role)
        await channel.send(f"**{member.name}** ({member.mention}) sunucuya iniş yaptı! Hoşgeldin!")
        user = User(member.id)

def setup(client):
    client.add_cog(OnMemberJoin(client))