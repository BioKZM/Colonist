from discord.ext import commands
from main import client
from functions.userClass import User

class OnMessage(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = str(message.channel)
        member = message.author
        if not message.author.bot:
            if channel == "kendini-tanıt":
                user = User(member.id)
                if user.data['messageBool'] == True:
                    channel = client.get_channel(id=910547555245494322)
                    await channel.send(f"<@{member.id}>,<#901248994922098718> kanalında kendinizi tanıttığınız için **250 XP** kazandınız!")
                    user.addXP(250)
                else:
                    pass
        # await self.client.process_commands(message)

def setup(client):
    client.add_cog(OnMessage(client))


