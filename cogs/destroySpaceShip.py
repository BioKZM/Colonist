import discord
import json
from discord.ext import commands
from discord.utils import get
# from cogs.personalPoint import PersonalPoint
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashContext,cog_ext
from main import client,guildID

class DestroySpaceShip(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name="gemipatlat",
        description="Bir gemiyi imha etmek için kullan.",
        guild_ids=guildID,
        options=[
            # create_option(
            #     name="gemi",
            #     description="İmha edilecek geminin ismini girin.",
            #     option_type=3,
            #     required=True
            # ),
            create_option(
                name="kategori",
                description="İmha edilecek geminin bulunduğu kategoriyi seçiniz.",
                option_type=7,
                required=True
            )
        ]
    )
    async def _gemipatlat(self,ctx,kategori:int):
        guild = ctx.guild
        role = get(guild.roles,name=f"{kategori.name}")
        captainRole = get(guild.roles,name=f"{kategori.name} - Captain")
        # print(kategori.name)
        # role = get(guild.roles,name=f"🚀{gemi}")
        # captainRole = get(guild.roles,name=f"🚀{gemi} - Captain")
        embed = discord.Embed(
            title = "Gemi İmha İşlemi",
            description = f"{role.mention} gemisi patlatılıyor!",
            color = 0x8d42f5
        )
        message = await ctx.send(embed=embed)
        channel = client.get_channel(id = kategori.id)
        for channel in channel.text_channels:
            await channel.delete()
        channel = client.get_channel(id = kategori.id)
        for voicechannel in channel.voice_channels:
            await voicechannel.delete()
        await channel.delete()
        
        await role.delete()
        await captainRole.delete()
        with open("files/captainHalls.json") as file:
            captainHalls = json.load(file)
            del captainHalls[f'{kategori.name[1:]}']
        
        with open("files/captainHalls.json","w") as file:
            json.dump(captainHalls,file,indent = 4)
        with open("files/openShips.py","w",encoding="utf-8") as dosya:
            dosya.write("captainHalls = ")
            dosya.write(str(captainHalls))
            dosya.close()
        embed = discord.Embed(
            title = "İşlem Başarılı!",
            description = "Gemi başarıyla imha edildi!",
            color = 0x8d42f5
        )
        await message.edit(embed=embed)

def setup(client):
    client.add_cog(DestroySpaceShip(client))