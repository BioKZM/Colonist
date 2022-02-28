# import discord
import json
from discord.ext import commands,tasks
from main import client
from discord.utils import get
from discord import ChannelType
from functions.userClass import User,levelNames

class VoiceChannel(commands.Cog):
    def __init__(self,client):
        self.client = client

    @tasks.loop(minutes=1)
    async def voicech():
        guild = client.guilds[0]
        vcList = [channel.id for channel in client.get_all_channels() if channel.type==ChannelType.voice]
        for channelID in vcList:
            voicechannel = client.get_channel(channelID)
            members = voicechannel.members
            for member in members:
                if not member.bot:
                    user = User(member.id)
                    user.updateXP()
                    if not user.isMaxLevel():
                        if user.XP > user.currentLevelMaximumXP:
                            user.level += 1
                            user.levelName = levelNames[user.level-1]
                            with open(f"userFiles/levels/{member.id}.json") as file:
                                data = json.load(file)
                                data['level'] = user.level
                            with open(f"userFiles/levels/{member.id}.json","w") as file:
                                json.dump(data,file,indent=4)
                            role = get(guild.roles,name=user.levelName)
                            await member.add_roles(role)
                            channel = client.get_channel(id=910547555245494322)
                            await channel.send(f"Tebrikler <@{member.id}>! **{user.level}**. seviyeye ulaştın!")

    @voicech.before_loop
    async def before_voicech():
        await client.wait_until_ready()
        print("Channel Update Loop OK!")
    voicech.start()                   

def setup(client):
	client.add_cog(VoiceChannel(client))