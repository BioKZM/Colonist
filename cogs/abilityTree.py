import discord
import json
from discord.ext import commands
# from Colonist.cogs.personalPoint import PersonalPoint
from discord_slash.utils.manage_commands import create_option
from discord.utils import get
from discord_slash import cog_ext
from main import client
from main import guildID
from files.embedDictionary import dictionary

class AbilityTree(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name = "yetenekağacı",
        description = "Yetenek ağacına rol eklemek için kullan!",
        guild_ids = guildID,
        options=[
            create_option(
                name= "rol",
                description = "Bir rol seç.",
                option_type=8,
                required=True, 
            ),
            create_option(
                name = "emoji",
                description="Bir emoji gir.",
                option_type=3,
                required=True,
            ),
            create_option(
                name="message_id",
                description = "Emojinin eklenmesini istediğin mesaj id'sini gir.",
                option_type=3,
                required=True
            )
            
            ]
    )
    async def embed(self,ctx,rol,emoji:str,message_id:int):
        channel = get(ctx.guild.channels,name="colonist")
        message = await channel.fetch_message(946743465889382410)
        # embed = message.embeds[0]
        # dictionary = embed.to_dict()
        # description = str(dictionary['description'])
        # description += "\n"+f"{emoji}:{str(rol)[:-2]}"
        # dictionary['description'] = description
        # embed = discord.Embed.from_dict(dictionary)
        # dictionary[str(emoji)] = str(rol)
        
        # channel = client.get_channel(905888377071616090)
        # message = await channel.fetch_message(911627236510146611)
        embed = message.embeds[0]
        di = embed.to_dict()
        description = str(di['description'])
        
        di['description'] = description
        embed = discord.Embed.from_dict(di)
        dictionary[str(emoji)] = str(rol)
        with open("files/embedDictionary.py","w") as dosya:
            dosya.write("dictionary = ")
            dosya.close()
        with open("files/embedDictionary.py","a",encoding="utf-8") as dosya:
            dosya.write(str(dictionary))
            dosya.close()
        await message.edit(embed=embed)
        emojiMessage = await channel.fetch_message(message_id)
        await emojiMessage.add_reaction(str(emoji))
        await ctx.send(embed=discord.Embed(title="Yetenek ağacı güncellemesi",description=f"{str(rol.mention)} rolü yetenek ağacına eklendi!"))

def setup(client):
    client.add_cog(AbilityTree(client))