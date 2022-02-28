# import discord
# import asyncio
# import json
# from discord.ext import commands
# from discord.utils import get
# # from cogs.personalPoint import PersonalPoint
# from main import client
# from discord_ui import UI,Button
# from functions.userClass import User,experiences,levelNames
# from cogs.rank import getSortedMembers
# ui = UI(client)

# class Information(commands.Cog):
#     def __init__(self,client):
#         self.client = client


#     @commands.command()
#     async def bilgi(self,ctx):
#         embed = discord.Embed(title="Üye Bilgi Ekranı",description="Üye bilgi ekranına hoş geldin.\nAşağıdaki butonlara basarak\nbilgisini almak istediğin içeriği görebilirsin.",color = 0x8d42f5,)
#         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
#         message = await ctx.channel.send(
#             embed=embed,
#             components = [
#                 Button(
#                     label = "Mevcut Seviye",
#                     custom_id = "seviye",
#                     color = ButtonStyle.Green,
#                     emoji = "📰",
#                 ),
#                 Button(
#                     label = "Liderlik Tablosu",
#                     custom_id = "liderliktablosu",
#                     color = ButtonStyle.Green,
#                     emoji = "📋",
#                 ),
#                 Button(
#                     label = "Detaylı Bilgi",
#                     custom_id = "detaylıbilgi",
#                     color = ButtonStyle.Green,
#                     emoji = "📜",
#                     new_line=True
#                 ),
#                 Button(
#                     label="Görevler",
#                     custom_id = "görevler",
#                     color = ButtonStyle.Green,
#                     emoji = "🪧",
#                 ),
#                 Button(
#                     label="Seviyeler",
#                     custom_id = "seviyeler",
#                     color = ButtonStyle.Green,
#                     emoji = "🚩",
#                     new_line=True
#                 ),
#                 Button(
#                     label = "Mesajı Sil",
#                     custom_id = "sil",
#                     color = ButtonStyle.Red,
                    
#                 ),
#                 ]
#         )
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#             info[ctx.author.id] = message.id

#         with open("files/infoMessage.json","w") as file:
#             json.dump(info,file,indent=4)



#     @ui.components.listening_component('seviye')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#             else:
#                 await component.message.edit(components=[
#                     Button(
#                         label = "Mevcut Seviye",
#                         custom_id = "seviye",
#                         color = ButtonStyle.Green,
#                         emoji = "📰",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Liderlik Tablosu",
#                         custom_id = "liderliktablosu",
#                         color = ButtonStyle.Green,
#                         emoji = "📋",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Detaylı Bilgi",
#                         custom_id = "detaylıbilgi",
#                         color = ButtonStyle.Green,
#                         emoji = "📜",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label="Görevler",
#                         custom_id = "görevler",
#                         color = ButtonStyle.Green,
#                         emoji = "🪧",
#                         disabled=True
#                     ),
#                     Button(
#                         label="Seviyeler",
#                         custom_id = "seviyeler",
#                         color = ButtonStyle.Green,
#                         emoji = "🚩",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                         disabled=True
                        
#                     ),
#                     ])
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 member = component.author
#                 user = User(member.id)
#                 if not member.bot:
#                     embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
#                     embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\n Rütbesi = **{}**\n".format(user.level,user.XP,user.levelName,inline=False))
#                     if user.isMaxLevel():
#                         embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**Maksimum seviyeye ulaştınız!**",inline=False)
#                     elif not user.isMaxLevel():
#                         if experiences[user.level] - user.XP <= 0:
#                             embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.getLevel(user.XP)]}** rütbesine ulaştın! Seviye atlamak için ses kanalına girebilirsin.",inline=False)
#                         else:
#                             embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-2])-user.XP}**",inline=False)

#                     embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
                
#                 await component.message.edit(embed=embed,components=[
#                     Button(
#                         label="Geri",
#                         custom_id="geri",
#                         color=ButtonStyle.Grey,
#                         emoji="⬅️"
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                     )
#                     ])

#         except KeyError:
#             embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()
#             return
            

#         try:
#             await component.respond()
#         except:
#             pass
            

        

#     @ui.components.listening_component('liderliktablosu')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#             else:
#                 await component.message.edit(components=[
#                     Button(
#                         label = "Mevcut Seviye",
#                         custom_id = "seviye",
#                         color = ButtonStyle.Green,
#                         emoji = "📰",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Liderlik Tablosu",
#                         custom_id = "liderliktablosu",
#                         color = ButtonStyle.Green,
#                         emoji = "📋",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Detaylı Bilgi",
#                         custom_id = "detaylıbilgi",
#                         color = ButtonStyle.Green,
#                         emoji = "📜",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label="Görevler",
#                         custom_id = "görevler",
#                         color = ButtonStyle.Green,
#                         emoji = "🪧",
#                         disabled=True
#                     ),
#                     Button(
#                         label="Seviyeler",
#                         custom_id = "seviyeler",
#                         color = ButtonStyle.Green,
#                         emoji = "🚩",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                         disabled=True			
#                     ),
#                 ])
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 sortedMembers = getSortedMembers(component)

#                 embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
#                 embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)

#                 count = 1
                
#                 for key,value in sortedMembers.items():
#                     embed.add_field(name="{} - {}".format(count,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
#                     count += 1
#                     if count == 11:break

#                 await component.message.edit(embed=embed,components=[
#                     Button(
#                         label="Geri",
#                         custom_id="geri",
#                         color=ButtonStyle.Grey,
#                         emoji="⬅️"
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                     )
#                 ])
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()


#     @ui.components.listening_component('detaylıbilgi')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#             else:		
#                 await component.message.edit(components=[
#                     Button(
#                         label = "Mevcut Seviye",
#                         custom_id = "seviye",
#                         color = ButtonStyle.Green,
#                         emoji = "📰",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Liderlik Tablosu",
#                         custom_id = "liderliktablosu",
#                         color = ButtonStyle.Green,
#                         emoji = "📋",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Detaylı Bilgi",
#                         custom_id = "detaylıbilgi",
#                         color = ButtonStyle.Green,
#                         emoji = "📜",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label="Görevler",
#                         custom_id = "görevler",
#                         color = ButtonStyle.Green,
#                         emoji = "🪧",
#                         disabled=True
#                     ),
#                     Button(
#                         label="Seviyeler",
#                         custom_id = "seviyeler",
#                         color = ButtonStyle.Green,
#                         emoji = "🚩",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                         disabled=True			
#                     ),
#                 ])
#                 liste = {}
#                 XP = {}
#                 for i in range(1,11):
#                     liste[f'level{i}'] = 0
#                     XP[f'xp{i}'] = ""
#                     if i == 1:
#                         XP[f"xp{i}"] += f"{levelNames[i-1]}"
#                     else:
#                         XP[f'xp{i}'] += f"{levelNames[i-1]} - {experiences[i-2]}" 

#                 try:
#                     await component.respond()
#                 except:
#                     pass
                
#                 for member in client.get_all_members():
#                     if not member.bot:
#                         user = User(member.id)
#                         liste[f'level{user.level}'] += 1
                
#                 message = discord.Embed(title = "Detaylı Bilgi",description="**Aşağıda, hangi seviyede kaç kullanıcının bulunduğunu öğrenebilirsin**",color = 0x8d42f5)
                
#                 for level in range(1,11):
#                     XPs = XP[f'xp{level}']
#                     levels = liste[f'level{level}']		
#                     if levels == 0:
#                         if XP[f'xp{level}'] == "Guest":
#                             message.add_field(name=f"*Seviye {level}* / {XPs}:",value=f"Bu seviyede herhangi biri yok.",inline=False)
#                         else:
#                             message.add_field(name=f"*Seviye {level}* / {XPs} XP:",value=f"Bu seviyede herhangi biri yok.",inline=False)
                        
                        
#                     else:
#                         if XP[f'xp{level}'] == "Guest":
#                             message.add_field(name=f"*Seviye {level}* / {XPs}:",value=f"**{levels}** kişi bu seviyede.",inline=False)
#                         else:
#                             message.add_field(name=f"*Seviye {level}* / {XPs} XP:",value=f"**{levels}** kişi bu seviyede.",inline=False)
#                 message.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
#                 await component.message.edit(embed=message,components=[
#                     Button(
#                         label="Geri",
#                         custom_id="geri",
#                         color=ButtonStyle.Grey,
#                         emoji="⬅️"
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                     )

#                     ])
        
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()		
                
                    
        
        
#     @ui.components.listening_component('görevler')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#             else:
#                 await component.message.edit(components=[
#                     Button(
#                         label = "Mevcut Seviye",
#                         custom_id = "seviye",
#                         color = ButtonStyle.Green,
#                         emoji = "📰",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Liderlik Tablosu",
#                         custom_id = "liderliktablosu",
#                         color = ButtonStyle.Green,
#                         emoji = "📋",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Detaylı Bilgi",
#                         custom_id = "detaylıbilgi",
#                         color = ButtonStyle.Green,
#                         emoji = "📜",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label="Görevler",
#                         custom_id = "görevler",
#                         color = ButtonStyle.Green,
#                         emoji = "🪧",
#                         disabled=True
#                     ),
#                     Button(
#                         label="Seviyeler",
#                         custom_id = "seviyeler",
#                         color = ButtonStyle.Green,
#                         emoji = "🚩",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                         disabled=True			
#                     ),
#                     ])
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 embed = discord.Embed(
#                     title = "Görevler",
#                     description = "**Bir gemiye atla ve bir oyun üret**;\nPC/Platform .............................. 10.0000 XP\nMobil ............................................... 5.000 XP\nHyperCasual................................... 2.000 XP\nGameJam.......................................... 1.000XP\n*Oyun yayınlanırsa kazanılan deneyim puanı iki katına çıkar*",
#                     color = 0x8d42f5
#                 )
#                 embed.add_field(
#                     name = "\n\nSunucu Takviyesi",
#                     value = "Her sunucu takviyesi başına **250 XP**",
#                     inline=False
#                 )
#                 embed.add_field(
#                     name = "\n\nSes Kanallarına Aktif Ol",
#                     value = "Dakika başına 1 XP\n*Not: Kazanılan XP, yayın ve kamera açma durumuna göre değişiklik gösterir.*",
#                     inline=False
#                 )
#                 embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
#                 await component.message.edit(embed=embed,components=[
#                     Button(
#                         label="Geri",
#                         custom_id="geri",
#                         color=ButtonStyle.Grey,
#                         emoji="⬅️"
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                     )
#                     ])
        
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()


#     @ui.components.listening_component('seviyeler')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#             else:

#                 await component.message.edit(components=[
#                     Button(
#                         label = "Mevcut Seviye",
#                         custom_id = "seviye",
#                         color = ButtonStyle.Green,
#                         emoji = "📰",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Liderlik Tablosu",
#                         custom_id = "liderliktablosu",
#                         color = ButtonStyle.Green,
#                         emoji = "📋",
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Detaylı Bilgi",
#                         custom_id = "detaylıbilgi",
#                         color = ButtonStyle.Green,
#                         emoji = "📜",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label="Görevler",
#                         custom_id = "görevler",
#                         color = ButtonStyle.Green,
#                         emoji = "🪧",
#                         disabled=True
#                     ),
#                     Button(
#                         label="Seviyeler",
#                         custom_id = "seviyeler",
#                         color = ButtonStyle.Green,
#                         emoji = "🚩",
#                         new_line=True,
#                         disabled=True
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                         disabled=True			
#                     ),
#                     ])
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 embed = discord.Embed(
#                     title = "Seviyeler",
#                     description = "Aşağıda, sunucuda bulunan mevcut seviyeleri görebilirsin.",
#                     color = 0x8d42f5
#                 )
#                 embed.add_field(
#                     name = "Guest:",
#                     value = "Misafir statüsünde üye",
#                     inline = False,

#                 )
#                 embed.add_field(
#                     name = "Colony Member / 250 XP:",
#                     value = "Koloni üyesi",
#                     inline = False,
#                 )

#                 embed.add_field(
#                     name = "Open Crew / 1.987 XP:",
#                     value = "Açık gemilerde mürettebat olma hakkına sahip üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Crew / 6.666 XP:",
#                     value = "Bütün gemilerde mürettebat olma hakkına sahip üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Captain / 9.999 XP:",
#                     value = "Gemilere kaptanlık yapma hakkına sahip üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Judge / 30.000 XP:",
#                     value = "Oy kullanma hakkına sahip üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Colony Manager / 90.000 XP:",
#                     value = "Tasarlanacak oyunlara karar veren üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Mars Lover / 300.000 XP:",
#                     value = "Yayınlanan bütün oyunlarda adına teşekkür edilen üye",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Chief of the Colony / 900.000 XP:",
#                     value = "Kolonideki kamu yönetiminde, herhangi bir rolü alabilen üye, A.K.A Chief",
#                     inline = False,
#                 )
#                 embed.add_field(
#                     name = "Partner / 10.000.001 XP:",
#                     value = "Koloninin fahri ortağı",
#                     inline = False,
#                 )
#                 embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
#                 await component.message.edit(embed=embed,components = [
#                     Button(
#                         label="Geri",
#                         custom_id="geri",
#                         color=ButtonStyle.Grey,
#                         emoji="⬅️"
#                     ),
#                     Button(
#                         label = "Mesajı Sil",
#                         custom_id = "sil",
#                         color = ButtonStyle.Red,
#                     )
#                     ])
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()

#     @ui.components.listening_component('geri')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                     embed = discord.Embed(
#                         title = "Uyarı",
#                         description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                         color = 0xFF0000
#                     )
#                     try:
#                         await component.respond()
#                     except:
#                         pass
#                     message = await component.channel.send(embed=embed)
#                     await asyncio.sleep(5)
#                     await message.delete()
#             else:
#                 embed = discord.Embed(title="Üye Bilgi Ekranı",description="Üye bilgi ekranına hoş geldin.\nAşağıdaki butonlara basarak\nbilgisini almak istediğin içeriği görebilirsin.",color = 0x8d42f5)
#                 embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 await component.message.edit(
#                     embed=embed,
#                     components = [
#                         Button(
#                             label = "Mevcut Seviye",
#                             custom_id = "seviye",
#                             color = ButtonStyle.Green,
#                             emoji = "📰",

#                         ),
#                         Button(
#                             label = "Liderlik Tablosu",
#                             custom_id = "liderliktablosu",
#                             color = ButtonStyle.Green,
#                             emoji = "📋",

#                         ),
#                         Button(
#                             label = "Detaylı Bilgi",
#                             custom_id = "detaylıbilgi",
#                             color = ButtonStyle.Green,
#                             emoji = "📜",
#                             new_line=True,

#                         ),
#                         Button(
#                             label="Görevler",
#                             custom_id = "görevler",
#                             color = ButtonStyle.Green,
#                             emoji = "🪧",
                
#                         ),
#                         Button(
#                             label="Seviyeler",
#                             custom_id = "seviyeler",
#                             color = ButtonStyle.Green,
#                             emoji = "🚩",
#                             new_line=True,

#                         ),
#                         Button(
#                             label = "Mesajı Sil",
#                             custom_id = "sil",
#                             color = ButtonStyle.Red,
                    
#                         ),
#                         ]
#                 )
        
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()

#     @ui.components.listening_component('sil')
#     async def listening_component(component):
#         with open("files/infoMessage.json") as file:
#             info = json.load(file)
#         try:
#             if component.message.id != info[f"{component.author.id}"]:
#                 embed = discord.Embed(
#                     title = "Uyarı",
#                     description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                     color = 0xFF0000
#                 )
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 message = await component.channel.send(embed=embed)
#                 await asyncio.sleep(5)
#                 await message.delete()
#                 await component.message.delete()
#             else:
#                 try:
#                     await component.respond()
#                 except:
#                     pass
#                 await component.message.delete()
#                 del info[component.author.id]
#                 with open("files/infoMessage.py","w",encoding="utf-8") as dosya:
#                     dosya.write("info = ")
#                     dosya.write(str(info))
        
#         except KeyError:
#             embed = discord.Embed(
#                 title = "Uyarı",
#                 description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
#                 color = 0xFF0000
#             )
#             try:
#                 await component.respond()
#             except:
#                 pass
#             message = await component.channel.send(embed=embed)
#             await asyncio.sleep(5)
#             await message.delete()


# def setup(client):
#     client.add_cog(Information(client))