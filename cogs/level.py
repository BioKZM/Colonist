import discord
import asyncio
import random
from discord.ext import commands
from functions.userClass import User,levelNames,experiences


class Level(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases=["level"])
    async def seviye(self,ctx,member:discord.Member=None):
        if member == None:
            member = ctx.author

        user = User(member.id)
        if not member.bot:
            if member.id == 276066808887508992:
                embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı ku½ll#n$cının de\4r½l%i",description="",color=0x8d42f5)
                embed.add_field(name="M#vc&-*/$ De¨eßrL3r - ❌",value="Seviyesi = **{}**\nPuanı = **-999999999999**\nRütbesi = **{}**".format("∞","undefined",inline=False))
                embed.add_field(name="B1r s0½rak` r#t!e - 🔒",value="Bir sonraki rütbe = **unknown**\n[_Hata] = **k[]ll4n1c1 v3R1lEri h4$arLI**",inline=False)
                embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
                message = await ctx.send(embed=embed)
                
                embed2 = discord.Embed(title="f adlı ku½ll#n$cının de\4r½l%i",description="",color=0x8d42f5)
                embed2.add_field(name="P4/7(+n De¨eßrL3r - ❌",value="Er0oR = **{}**\nRütbesi = **{}**\nMevcut = **{}**".format("√52734156","undefined",random.randint(-999999,999999)),inline=False)
                embed2.add_field(name="B'r s0½rak# r}£!æ - 🔒",value="H½3t_l| d3ğ½9oken = **unknown**\n[_Hata] = **k[u]ll4n1c1 v3R~|Eri hæ$ar/I**",inline=False)
                embed2.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
                for i in range(0,1000):
                    numbers = [1,2,3]
                    await asyncio.sleep(random.choice(numbers))
                    await message.edit(embed=embed2)
                    await asyncio.sleep(random.choice(numbers))
                    await message.edit(embed=embed)
                    
            else:
                embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
                embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\n Rütbesi = **{}**\n".format(user.level,user.XP,user.levelName,inline=False))
               
                if user.isMaxLevel():
                    embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-1])-user.XP}**" if not user.isMaxLevel() else "Maksimum seviyeye ulaştınız!",inline=False)
                
                elif not user.isMaxLevel():
                    if experiences[user.level] - user.XP <= 0:
                        embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level+1]}** rütbesine ulaştın! Seviye atlamak için ses kanalına girebilirsin.",inline=False)
                        
                    else:
                        if user.level == 0:
                            embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level])-user.XP}**",inline=False)
                        else:
                            embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level+1]}** rütbesi için kalan puan = **{(experiences[user.level])-user.XP}**",inline=False)

                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Level(client))