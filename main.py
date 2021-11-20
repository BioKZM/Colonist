import discord 
import os
import sys
import asyncio
import random
from discord.ext import commands,tasks
from discord.utils import get
from keep_alive import keep_alive
from discord_ui import *
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from Files.levels import nextXP, nextLevel
from discord import ChannelType

keep_alive()
TOKEN = os.environ["TOKEN"]
client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
ui = UI(client)
slash = SlashCommand(client,sync_commands=True)
guildID = [888759899226538025]




@client.event
async def on_ready():
	print("On Mars Way!")
	await client.change_presence(status=discord.Status.online,activity=discord.Game("🚀 On My Way To Mars!"))
	
@client.event
async def on_message(message):
	channel = str(message.channel)
	memberName = message.author.name
	memberID = message.author.id
	if message.author.bot:
		pass
	else:
		if channel == "kendini-tanıt":
			with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
				okuma = dosya.read().splitlines()
				XP = int(okuma[0])
				modifier = okuma[1]
				level = okuma[2]
				_nextLevel = okuma[3]
				mesaj = okuma[4]
				dosya.close()
			
			if mesaj == "True":
				XP += 250
				mesaj = "False"
				channel = client.get_channel(id=910547555245494322)
				await channel.send(f"<@{memberID}>,<#901248994922098718> kanalında kendinizi tanıttığınız için **250 XP** kazandınız!")
				with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
					dosya.write("{}\n{}\n{}\n{}\n{}\n".format(XP,modifier,level,_nextLevel,mesaj))
					dosya.close()
			else:
				pass
	await client.process_commands(message)



@client.command(aliases=["help","komutlar"])
async def yardım(ctx):
	member = ctx.author
	embed = discord.Embed(title="Yardım komutları",description="\n",color=0x8d42f5)
	embed.add_field(name="!yardım `[ !help, !komutlar ]`",value="Bot üzerinde bulunan mevcut komutları görüntülemenizi sağlar.",inline=False)
	embed.add_field(name="!seviye `[ !level ]`",value="Mevcut ve gelecek seviye değerlerini gösteririr.",inline=False)
	embed.add_field(name="!sıralama `[ !rank ]`",value="Güncel liderlik tablosunu gösterir.",inline=False)
	await ctx.channel.send(embed=embed)

@client.command()
async def ekle(ctx):
	await ctx.message.delete()
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		
		guild = ctx.guild
 		liste = ["Partner","Chief of the Colony","Mars Lover","Colony Manager","Judge","Captain","Crew","Open Crew","Colony Member","Guest"]
		#liste = ["Partner","Chief of the Colony","Mars Lover","Colony Manager","Judge","Captain","Crew","Open Crew","Colony Member","Guest"]
		for role in liste:
			await guild.create_role(name=role)
		message = await ctx.send("Rol ekleme işlemi başarıyla tamamlandı!")
		await asyncio.sleep(3)
		await message.delete()
	else:
		message = await ctx.send("Bu komutu kullanmaya izniniz yok!")
		await asyncio.sleep(3)
		await message.delete()

@client.command()
async def sil(ctx):
	await ctx.message.delete()
	if ctx.author.id == 373457193271558145:

		liste = ["Partner","Chief of the Colony","Mars Lover","Colony Manager","Judge","Captain","Crew","Open Crew","Colony Member","Guest"]
		for roleName in liste:
			role = discord.utils.get(ctx.message.guild.roles,name=f"{roleName}")
			await role.delete()
		await ctx.channel.send("İşlem tamam!")
	else:
		message = await ctx.channel.send("Bu komutu kullanmaya izniniz yok!")
		await asyncio.sleep(2)
		await message.delete()


@client.event
async def on_voice_state_update(member,prev,cur):
	members = [m for m in client.get_all_members()]
	for member in members:
		memberName = member.name
		memberID = member.id
		if prev.channel and cur.channel:
			if cur.self_stream:
				if member.bot:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						level = okuma[2]
						nextInt = okuma[3]
						mesaj = okuma[4]
						dosya.close()
					
					with open("Files/yayınÇarpanı.txt") as dosya:
						okuma = dosya.read().splitlines()
						modifier = okuma[0]
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:	
						dosya.write("{}\n{}\n{}\n{}\n{}".format(str(XP),str(modifier),str(level),nextInt,mesaj))
						dosya.close()
			
			if cur.self_video:
				if member.bot:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						level = okuma[2]
						nextInt = okuma[3]
						mesaj = okuma[4]
						dosya.close()
					
					with open("Files/kameraÇarpanı.txt") as dosya:
						okuma = dosya.read().splitlines()
						modifier = okuma[0]
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:	
						dosya.write("{}\n{}\n{}\n{}\n{}".format(str(XP),str(modifier),str(level),nextInt,mesaj))
						dosya.close()
		
			if cur.self_stream and cur.self_video:
				if member.bot:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						level = okuma[2]
						nextInt = okuma[3]
						mesaj = okuma[4]
						dosya.close()
					with open("Files/kameraÇarpanı.txt") as dosya:
						okuma = dosya.read().splitlines()
						kameraÇarpanı = okuma[0]
						dosya.close()
					with open("Files/yayınÇarpanı.txt") as dosya:
						okuma = dosya.read().splitlines()
						yayınÇarpanı = okuma[0]
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						modifier = int(yayınÇarpanı)+int(kameraÇarpanı)
						dosya.write("{}\n{}\n{}\n{}\n{}".format(str(XP),str(modifier),str(level),nextInt,mesaj))
						dosya.close()
			elif not cur.self_stream and not cur.self_video:
				if member.bot:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						level = okuma[2]
						nextInt = okuma[3]
						mesaj = okuma[4]
						dosya.close()
					
					with open("Files/dakikaÇarpanı.txt") as dosya:
						okuma = dosya.read().splitlines()
						modifier = okuma[0]
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:	
						if memberName == "Bazzars":
							modifier = 3
						dosya.write("{}\n{}\n{}\n{}\n{}".format(str(XP),str(modifier),str(level),nextInt,mesaj))
						dosya.close()
	

@client.command()
async def deneme(ctx):
	if ctx.author.id == 373457193271558145:

		print("qRnt")
		members = [m for m in client.get_all_members()]
		for member in members:
			memberName = member.name
			memberID = member.id
			print(memberName)
			if member.name == "Colonist":
				pass
			else:

				with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
					okuma = dosya.read().splitlines()
					XP = okuma[0]
					modifier = okuma[1]
					level = okuma[2]
					_nextLevel = okuma[3]
				if member.name == "Colonist":
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("{}\n{}\n{}\n{}\n{}\n".format(XP,modifier,level,_nextLevel,"True"))
						dosya.close()	
	else:
		pass

@tasks.loop(minutes=1)
async def voicech():
	vcList = [channel.id for channel in client.get_all_channels() if channel.type==ChannelType.voice]
	guild = client.guilds[0]
	for channelID in vcList:
		voicechannel = client.get_channel(channelID)
		members_ = [m for m in client.get_all_members()]
		for member in members_:
			memberID = member.id
			memberName = member.name
			file_there = os.path.isfile(f"voiceLevels/{memberName}-{memberID}.txt")
			if not file_there:
				if not member.bot:
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("0\n")
						dosya.write("1\n")
						dosya.write("Guest\n")
						dosya.write("1\n")
						dosya.write("True\n")
						dosya.close()
			else:
				pass

		members = voicechannel.members
		
		for member in members:
			if member.bot:
				pass
			else:
				memberID = member.id
				memberName = member.name
				with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
					okuma = dosya.read().splitlines()
					XP = int(okuma[0])
					modifier = int(okuma[1])
					level = okuma[2]
					_nextLevel = int(okuma[3])
					mesaj = okuma[4]
					XP = XP + modifier
					dosya.close()
					
					if XP < 699:
						level = "Guest"
						role = get(guild.roles,name="Guest")
						await member.add_roles(role)
						_nextLevel = 1
					if XP > 699 and XP < 1987:
						level = "Colony Member"
						role = get(guild.roles,name="Colony Member")
						await member.add_roles(role)
						_nextLevel = 2

					if XP > 1987 and XP < 6666:
						level = "Open Crew"
						role = get(guild.roles,name="Open Crew")
						await member.add_roles(role)
						_nextLevel = 3

					if XP > 6666 and XP < 9999:
						level = "Crew"
						role = get(guild.roles,name="Crew")
						await member.add_roles(role)
						_nextLevel = 4

					if XP > 9999 and XP < 30000:
						level = "Captain"
						role = get(guild.roles,name="Captain")
						await member.add_roles(role)
						_nextLevel = 5

					if XP > 30000 and XP < 90000:
						level = "Judge"
						role = get(guild.roles,name="Judge")
						await member.add_roles(role)
						_nextLevel = 6

					if XP > 90000 and XP < 300000:
						level = "Colony Manager"
						role = get(guild.roles,name="Colony Manager")
						await member.add_roles(role)
						_nextLevel = 7
				
					if XP > 300000 and XP < 900000:
						level = "Mars Lover"
						role = get(guild.roles,name="Mars Lover")
						await member.add_roles(role)
						_nextLevel = 8
					
					if XP > 900000 and XP < 10000001:
						level = "Chief of the Colony"
						role = get(guild.roles,name="Chief of the Colony")
						await member.add_roles(role)
						_nextLevel = 9

					if XP > 10000001:
						level = "Partner"
						role = get(guild.roles,name="Partner")
						await member.add_roles(role)
						_nextLevel = 10
						dosya.close()
						
				with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
					dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
					dosya.close()
			
@voicech.before_loop
async def before_voicech():
	await client.wait_until_ready()
	print("Channel Update Loop OK!")
voicech.start()



@client.command()
async def emojiMessage(ctx):
	gameDirector = "🎬"
	gameDesigner = "🎮"
	levelDesigner = "🕹️"
	scriptWriter = "📕"
	interpreter = "🌍"
	uxDesigner = "⚠️"
	socialMediaExpert = "👍"
	gameDeveloper = "⌨️"
	visualArtist = "🎨"
	pixelArtist = "👾"
	_3dArtist = "🧊"
	_2dArtist = "🖼️"
	cellAnimator = "🏃‍♀️"
	vfxArtist = "💥"
	uiDesigner = "📺"
	soundDesigner = "🎵"
	folleyArtist = "📣"
	voiceActor = "🎤"
	singer = "👩‍🎤"
	dancer = "💃"
	detective = "🕵️"
	vampire = "🧛"
	fighter = "⚔️"
	ranger = "🏹"
	wizard = "🧙‍♂️"
	astronaut = "🚀"
	duhan = "🌪️"

	emojis = [gameDirector,gameDesigner,levelDesigner,scriptWriter,interpreter,uxDesigner,socialMediaExpert,gameDeveloper,visualArtist,pixelArtist,_3dArtist,_2dArtist,cellAnimator,vfxArtist,uiDesigner,soundDesigner,folleyArtist,voiceActor,singer,dancer]
	emojis2=[detective,vampire,fighter,ranger,wizard,astronaut,duhan]
	embed = discord.Embed(title="Yeteneklerin",description="Gemide eksik olan mürettebat sen olabilirsin.\nYeteneklerini işaretle! Rolünü seç! Gizli yetenek olmaktan çık!\n\n🎬:Game Director\n🎮:Game Designer\n🕹️: Level Designer\n📕:Script Writer\n🌍:Interpreter\n⚠️:UX Designer\n👍:Social Media Expert\n⌨️: Game Developer\n🎨: Visual Artist\n👾:Pixel Artist\n🧊:3D Artist\n🖼️:2D Artist\n🏃‍♀️:Cell Animator\n💥:VFX Artist\n📺:UI Designer\n🎵:Sound Designer\n📣:Folley Artist\n🎤:Voice Actor\n👩‍🎤:Singer\n💃:Dancer\n🕵️:Detective\n🧛:Vampire\n⚔️:Fighter\n:🏹Ranger\n🧙‍♂️:Wizard\n🚀:Astronaut\n🌪️:Duhan",color=0x6A0DAD)
	message = await ctx.channel.send(embed=embed)
	message2 = await ctx.channel.send("Aşağıdaki emojilere basarak rollerini seçebilirsin.")
	message3 = await ctx.channel.send("Devamı ↓ ")
	for emoji in emojis:
		await message2.add_reaction(emoji)
	for emoji in emojis2:
		await message3.add_reaction(emoji)



@client.event
async def on_raw_reaction_add(payload):
	channel = payload.channel_id
	member = payload.member
	reaction = payload.emoji
	guild = client.get_guild(payload.guild_id)

	if channel == 874040848239718431:
		if member.bot:
			pass

		if str(reaction) == "🎬":
			role = get(payload.guild.roles,name="Game Director 🎬")

		if str(reaction) == "🎮":
			role = get(payload.guild.roles,name="Game Designer 🎮")

		if str(reaction) == "🕹️":
			role = get(payload.guild.roles,name="Level Designer 🕹️")

		if str(reaction) == "📕":
			role = get(payload.guild.roles,name="Script Writer 📕")		
		
		if str(reaction) == "🌍":
			role = get(payload.guild.roles,name="Interpreter 🌍")
		
		if str(reaction) == "⚠️":
			role = get(payload.guild.roles,name="UX Designer ⚠️")
		
		if str(reaction) == "👍":
			role = get(payload.guild.roles,name="Social Media Expert 👍")
		
		if str(reaction) == "⌨️":
			role = get(payload.guild.roles,name="Game Developer ⌨️")
		
		if str(reaction) == "🎨":
			role = get(payload.guild.roles,name="Visual Artist 🎨")
		
		if str(reaction) == "👾":
			role = get(payload.guild.roles,name="Pixel Artist 👾")
		
		if str(reaction) == "🧊":
			role = get(payload.guild.roles,name="3D Artist 🧊")
		
		if str(reaction) == "🖼️":
			role = get(payload.guild.roles,name="2D Artist 🖼️")
		
		if str(reaction) == "🏃‍♀️":
			role = get(payload.guild.roles,name="Cell Animator 🏃‍♀️")
		
		if str(reaction) == "💥":
			role = get(payload.guild.roles,name="VFX Artist 💥")

		if str(reaction) == "📺":
			role = get(payload.guild.roles,name="UI Designer 📺")
		
		if str(reaction) == "🎵":
			role = get(payload.guild.roles,name="Sound Designer 🎵")

		if str(reaction) == "📣":
			role = get(payload.guild.roles,name="Folley Artist 📣")
		
		if str(reaction) == "🎤":
			role = get(payload.guild.roles,name="Voice Actor 🎤")
		
		if str(reaction) == "👩‍🎤":
			role = get(payload.guild.roles,name="Singer 👩‍🎤")
		
		if str(reaction) == "💃":
			role = get(payload.guild.roles,name="Dancer 💃")
		
		if str(reaction) == "🕵️":
			role = get(payload.guild.roles,name="Detective 🕵️")
		
		if str(reaction) == "🧛":
			role = get(payload.guild.roles,name="Vampire 🧛")

		if str(reaction) == "⚔️":
			role = get(payload.guild.roles,name="Fighter ⚔️")
		
		if str(reaction) == "🏹":
			role = get(payload.guild.roles,name="Ranger 🏹")

		if str(reaction) == "🧙‍♂️":
			role = get(payload.guild.emojis,name="Wizard 🧙‍♂️")
		
		if str(reaction) == "🚀":
			role = get(payload.guild.emojis,name="Astronaut 🚀")

		if str(reaction) == "🌪️":
			role = get(payload.guild.emojis,name="Duhan 🌪️")
			
		await member.add_roles(role)
	
	
	
	
	# gameDirector = payload.get_emoji("🎬")
	# gameDesigner = payload.get_emoji("🎮")
	# levelDesigner = payload.get_emoji("🕹️")
	# scriptWriter = payload.get_emoji("📕")
	# interpreter = payload.get_emoji("🌍")
	# uxDesigner = payload.get_emoji("⚠️")
	# socialMediaExpert = payload.get_emoji("👍")
	# gameDeveloper = payload.get_emoji("⌨️")
	# visualArtist = payload.get_emoji("🎨")
	# pixelArtist = payload.get_emoji("👾")
	# _3dArtist = payload.get_emoji("🧊")
	# _2dArtist = payload.get_emoji("🖼️")
	# cellAnimator = payload.get_emoji("🏃‍♀️")
	# vfxArtist = payload.get_emoji("💥")
	# uiDesigner = payload.get_emoji("📺")
	# soundDesigner = payload.get_emoji("🎵")
	# folleyArtist = payload.get_emoji("📣")
	# voiceActor = payload.get_emoji("🎤")
	# singer = payload.get_emoji("👩‍🎤")
	# dancer = payload.get_emoji("💃")
	# detective = payload.get_emoji("🕵️")
	# vampire = payload.get_emoji("🧛")
	# fighter = payload.get_emoji("⚔️")
	# ranger = payload.get_emoji("🏹")
	# wizard = payload.get_emoji("🧙‍♂️")
	# astronaut = payload.get_emoji("🚀")
	# duhan = payload.get_emoji("🌪️")
	# emojis = [gameDirector,gameDesigner,levelDesigner,scriptWriter,interpreter,uxDesigner,socialMediaExper,gameDeveloper,visualArtist,pixelArtist,_3dArtist,_2dArtist,cellAnimator,vfxArtist,uiDesigner,soundDesigner,folleyArtist,voiceActor,signer,dancer,detective,vampire,fighter,ranger,wizard,astronaut,duhan]





# @client.command()
# async def x(ctx):
# 	member = ctx.author
# 	emoji = client.get_emoji=("🎬")
# 	await ctx.channel.send(emoji)			

@client.command(aliases=["level"])
async def seviye(ctx,member:discord.Member=None):
	if member == None:
		member = ctx.author
		memberName = ctx.author.display_name
		memberID = ctx.author.id
	else:
		memberID = member.id
		memberName = member.display_name
	
	with open(f"voiceLevels/{member.name}-{memberID}.txt") as dosya:
		okuma = dosya.read().splitlines()
		XP = int(okuma[0])
		rütbe = okuma[2]
		level = okuma[3]
		nextInt = int(okuma[3])
		_nextXP = nextXP[nextInt-1] - XP
		
		dosya.close()
		if nextInt == 9:
			embed = discord.Embed(title=f"{memberName}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
			embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = {}\n Puanı = **{}**\n Rütbesi = **{}**\n".format(level,XP,rütbe),inline=False)
			embed.add_field(name="Bir sonraki değerler - 🚀 ",value="Maksimum seviyeye ulaştınız!",inline=False)
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title=f"{memberName}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
			embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\nRütbesi = **{}**".format(level,XP,rütbe),inline=False)
			embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{nextLevel[nextInt-1]}** rütbesi için kalan puan = **{_nextXP}**",inline=False)
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
# async def seviye(ctx,member:discord.Member):
# 	if member == None:
# 		member = ctx.author
# 	else:
# 		with open(f"voiceLevels/{member.name}-{member.id}.txt") as dosya:
# 			okuma = dosya.read().split()
# 			XP = okuma[0]
# 			level = okuma[2]
# 			dosya.close()
# 			embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=member.top_role.color)
# 			embed.add_field(name="Mevcut değerler ",value="Puanı = {}\n Rütbesi = {}".format(XP,level),inline=False)
# 			embed.add_field(name="Bir sonraki değerler - 🏆",value=f"{level}",inline=False)
# 			await ctx.send(embed=embed)
		


@slash.slash(
	name="çarpan",
	description="Bir çarpan değeri gir!",
	guild_ids=guildID,
	options=[
		create_option(
			name="görüntü",
			description="Değiştirmek istediğin çarpan değerini seç!",
			option_type=3,
			required=True,
			choices=[
				create_choice(
					name="Kamera Çarpanı",
					value="Kamera",
				),
				create_choice(
					name="Yayın Çarpanı",
					value="Yayın"
				),
				create_choice(
					name="Dakika Çarpanı",
					value="Dakika"
				)
			]
		),
		create_option(
			name="çarpan",
			description="Çarpan değerini değiştir!",
			option_type=4,
			required=True,
		)

	]
)
async def _çarpan(ctx:SlashContext,çarpan:int,görüntü:str):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:

		if görüntü == "Kamera":
			embed = discord.Embed(
				title="Kamera çarpanı değişimi!",
				description=f"Kamera çarpanı şu değere değiştirildi! = **{çarpan}**",
				color=0xCC0000)
			with open("Files/kameraÇarpanı.txt","w") as dosya:
				dosya.write(str(çarpan))
				dosya.close()
			await ctx.send(embed=embed)
			
		if görüntü == "Yayın":
			embed = discord.Embed(
				title="Yayın çarpanı değişimi!",
				description=f"Yayın çarpanı şu değere değiştirildi! = **{çarpan}**",
				color=0xCC0000)
			with open("Files/yayınÇarpanı.txt","w") as dosya:
				dosya.write(str(çarpan))
				dosya.close()
			await ctx.send(embed=embed)

		if görüntü == "Dakika":
			embed = discord.Embed(
				title="Dakika çarpanı değişimi!",
				description=f"Dakika çarpanı şu değere değiştirildi! = **{çarpan}**",
				color=0xCC0000)
			with open("Files/dakikaÇarpanı.txt","w") as dosya:
				dosya.write(str(çarpan))
				dosya.close()
			await ctx.send(embed=embed)
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")


# @slash.slash(
# 	name = "sıralama",
# 	description="Liderlik sıralamasını görmek için kullan!",
# 	guild_ids=guildID,
# )
@client.command(aliases=["rank"])
async def sıralama(ctx):
	member = ctx.author
	top10 = 1
	embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)	
	di = {}	
	members = [m for m in client.get_all_members()]
	for member in members:
		memberID = member.id
		memberName = f"{member.display_name} [ A.K.A : {member.name} ]"
		if member.bot:
			pass
		else:
			with open(f"voiceLevels/{member.name}-{memberID}.txt") as dosya:
				okuma = (dosya.read().splitlines())
				level = okuma[2]
				di[memberName] = [int(okuma[0]),level]
				sözlük = dict(sorted(di.items(),key=lambda item:item[1],reverse=True))
				dosya.close()	
	for key,value in sözlük.items():
		if top10 == 11:
			break
		embed.add_field(name="{} - {}".format(top10,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
		top10 += 1
				

		
	await ctx.send(embed=embed)

@slash.slash(
	name="gemipuan",
	description = "Kullanıcılara ekstra puan vermek için kullan!",
	guild_ids=guildID,
	options=[
		create_option(
			name="gemi",
			description="Bir gemi seç!",
			option_type=8,
			required=True

		),
		create_option(
			name = "platform",
			description="Seçilen platforma göre puan ver",
			option_type=3,
			required=True,
			choices=[
				create_choice(
					name="PC",
					value="PC"
				),
				create_choice(
					name="Mobil",
					value="Mobil",
				),
				create_choice(
					name="Hypercasual",
					value="Hypercasual",
				),
				create_choice(
					name="GameJam",
					value="GameJam"
				)
			]
		)
	]
)
async def _puan(ctx:SlashContext,platform:str,gemi:str):
	if ctx.author.id == 275971871047024640 or ctx.author.id == 373457193271558145:
		checkRole = get(ctx.guild.roles,name=str(gemi))
		if platform == "PC":
			members = [m for m in client.get_all_members()]
			for member in members:
				memberName = member.name
				memberID = member.id
				if checkRole not in member.roles:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						modifier = int(okuma[1])
						level = okuma[2]
						_nextLevel = okuma[3]
						mesaj = okuma[4]
						XP += 10000
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
						dosya.close()
			embed=discord.Embed(title="Puan artışı",description="**{}** adlı geminin mürettebatına **10.000** puan eklendi".format(checkRole.mention),color=member.top_role.color)
			await ctx.send(embed=embed)	

		if platform == "Mobil":
			members = [m for m in client.get_all_members()]
			for member in members:
				memberName = member.name
				memberID = member.id
				if checkRole not in member.roles:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						modifier = int(okuma[1])
						level = okuma[2]
						_nextLevel = okuma[3]
						mesaj = okuma[4]
						XP += 5000
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
						dosya.close()
			embed=discord.Embed(title="Puan artışı",description="**{}** adlı geminin mürettebatına **5.000** puan eklendi".format(checkRole.mention),color=member.top_role.color)
			await ctx.send(embed=embed)
		
		if platform == "Hypercasual":
			members = [m for m in client.get_all_members()]
			for member in members:
				memberName = member.name
				memberID = member.id
				if checkRole not in member.roles:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						modifier = int(okuma[1])
						level = okuma[2]
						_nextLevel = okuma[3]
						mesaj = okuma[4]
						XP += 2000
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
						dosya.close()
			embed=discord.Embed(title="Puan artışı",description="**{}** adlı geminin mürettebatına **2.000** puan eklendi".format(checkRole.mention),color=member.top_role.color)
			await ctx.send(embed=embed)	

		if platform == "GameJam":
			members = [m for m in client.get_all_members()]
			for member in members:
				memberName = member.name
				memberID = member.id
				if checkRole not in member.roles:
					pass
				else:
					with open(f"voiceLevels/{memberName}-{memberID}.txt") as dosya:
						okuma = dosya.read().splitlines()
						XP = int(okuma[0])
						modifier = int(okuma[1])
						level = okuma[2]
						_nextLevel = okuma[3]
						mesaj = okuma[4]
						XP += 1000
						dosya.close()
					with open(f"voiceLevels/{memberName}-{memberID}.txt","w") as dosya:
						dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
						dosya.close()
			embed=discord.Embed(title="Puan artışı",description="**{}** adlı geminin mürettebatına **1.000** puan eklendi".format(checkRole.mention),color=member.top_role.color)
			await ctx.send(embed=embed)


@slash.slash(
	name = "kişiselpuan",
	description="Kişiye özel puan vermek için kullan!",
	guild_ids=guildID,
	options=[
		create_option(
			name = "kullanıcı",
			description="Bir kullanıcı seç!",
			option_type=6,
			required=True,
		),
		create_option(
			name="puan",
			description="Bir puan değeri gir!",
			option_type=4,
			required=True,
		)
	]
)
async def _kişiselpuan(ctx:SlashContext,kullanıcı:discord.Member,puan:int):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		kullanıcıID = kullanıcı.id
		kullanıcıİsmi = kullanıcı.name
		with open(f"voiceLevels/{kullanıcıİsmi}-{kullanıcıID}.txt") as dosya:
			okuma = dosya.read().splitlines()
			XP = int(okuma[0])
			modifier = okuma[1]
			level = okuma[2]
			_nextLevel = okuma[3]
			mesaj = okuma[4]
			XP += puan
			dosya.close()

		with open(f"voiceLevels/{kullanıcıİsmi}-{kullanıcıID}.txt","w") as dosya:
			dosya.write("{}\n{}\n{}\n{}\n{}".format(XP,modifier,level,_nextLevel,mesaj))
			dosya.close()
		
		embed=discord.Embed(title="Puan ekleme işlemi",description=f"**{kullanıcıİsmi}** adlı kullanıcıya **{puan}** puan eklendi!",color=kullanıcı.top_role.color)
		await ctx.send(embed=embed,hidden=True)
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")
		
# @client.command()
# async def sustur(ctx):
# 	if isinstance(ctx.channel,discord.channel.DMChannel):
# 		member = get(client.get_all_members(), id=275971871047024640)
# 		await member.edit(mute = True)
		# channel = client.get_channel(id=860636538701611050)
		# await channel.send("İşlem tamam")

@client.command()
async def DM(ctx,user:discord.Member,*,message=None):
	await ctx.message.delete()
	# await user.edit(mute = True)
	message = message or "Bu mesaj DM yoluyla gönderildi"
	await user.send(message)
client.run(TOKEN) 	

