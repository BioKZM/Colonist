import discord
import os
# import sys
import asyncio
# import random
from discord.ext import commands,tasks
from discord.utils import get
from keep_alive import keep_alive
# from discord_ui import *
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from firebase import firebase
from Files.levels import nextXP, nextLevel
from discord import ChannelType
global message2
global message3
embeds = []

keep_alive()
TOKEN = os.environ["TOKEN"]
serverURL = os.environ["serverURL"]
client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
intents = discord.Intents.all()
intents.members = True
# ui = UI(client) 
slash = SlashCommand(client)
guildID = [888759899226538025]




@client.event
async def on_ready():
	print("On Mars Way!")
	await client.change_presence(status=discord.Status.online,activity=discord.Game("🚀 On My Way To Mars!"))


@client.event
async def on_member_join(member):
	guild = client.guilds[0]
	channel = client.get_channel(915299360202448978)
	await member.edit(nick="👁 WATCHER")
	role = get(guild.roles,name="Unit")
	await member.add_roles(role)
	await channel.send(f"**{member.name}** sunucuya iniş yaptı! Hoşgeldin!")
@client.event
async def on_message(message):
	channel = str(message.channel)
	memberID = message.author.id
	user = User(memberID)
	if message.author.bot:
		pass
	else:
		if channel == "kendini-tanıt":
			if user.checkBoolMessage() == "True":
				user.addXP(250)
				user.changeBoolMessage("False")
				channel = client.get_channel(id=910547555245494322)
				await channel.send(f"<@{memberID}>,<#901248994922098718> kanalında kendinizi tanıttığınız için **250 XP** kazandınız!")
			else:
				pass
	await client.process_commands(message)



@client.command(aliases=["help","komutlar"])
async def yardım(ctx):
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
		liste = ["Game Director 🎬","Game Designer 🎮","Level Designer 🕹️","Script Writer 📕","Interpreter 🌍","UX Designer ⚠️","Social Media Expert 👍","Game Developer ⌨️","Visual Artist 🎨","Pixel Artist 👾","3D Artist 🧊","2D Artist 🖼️","Cell Animator️ 🏃‍♀️","VFX Artist 💥","UI Designer 📺","Sound Designer 🎵","Folley Artist 📣","Voice Actor 🎤","Singer 👩‍🎤","Dancer 💃","Detective 🕵️","Vampire 🧛","Fighter ⚔️","Ranger 🏹","Wizard 🧙‍♂️","Astronaut 🚀","Duhan 🌪️"]

		for role in liste:
			await guild.create_role(name=role)
		message = await ctx.send("Rol ekleme işlemi başarıyla tamamlandı!")
		await asyncio.sleep(3)
		await message.delete()
	else:
		message = await ctx.send("Bu komutu kullanmaya izniniz yok!")
		await asyncio.sleep(3)
		await message.delete()

def memberSituation(prev,cur):
	if prev.self_stream and cur.self_video:
		return "stream + cam"
	if not prev.self_stream and cur.self_video:
		return "cam"
	if not prev.self_stream and not cur.self_video:
		return ""
	if prev.self_stream and not cur.self_video:
		return "stream"


@client.event
async def on_voice_state_update(member,prev,cur):
	memberID = member.id
	if prev.channel and cur.channel:
		if not member.bot:
			user = User(memberID)
			if memberSituation(prev,cur) == "stream":
				modifier = user.getModifier(location="yayınÇarpanı")
				user.changeModifier(modifier=modifier)

			elif memberSituation(prev,cur) == "cam":
				modifier = user.getModifier(location="kameraÇarpanı")
			
				user.changeModifier(modifier=modifier)

			elif memberSituation(prev,cur) == "stream + cam":
				camModifier = user.getModifier(location="kameraÇarpanı")
				streamModifier = user.getModifier(location="yayınÇarpanı")
				modifier = camModifier + streamModifier
				user.chaneModifier(modifier=modifier)
		
			elif memberSituation(prev,cur) == "":
					modifier = user.getModifier(location="dakikaÇarpanı")
					user.changeModifier(modifier=modifier)
					




class User():
	def __init__(self,memberID):
		self.memberID = memberID
		self.serverURL = serverURL
		self.guild = client.guilds[0]
		self.firebase_ = firebase.FirebaseApplication(serverURL,None)
		if self.userNotExists() == None:
			self.create(self.memberID)

	def userNotExists(self):
		self.file_there = self.firebase_.get(self.serverURL,f"/voiceLevels/{self.memberID}")
		return self.file_there

	def updateXP(self,memberID):
		data = self.getData(memberID)
		XP = data['XP']
		modifier = data['modifier']
		self.firebase_.put(f"/voiceLevels/{memberID}",'XP',XP+modifier)


	async def addRole(self,role,member):
		role = get(self.guild.roles,name=role)
		await member.add_roles(role)
		self.firebase_.put(f"/voiceLevels/{self.memberID}",'currentLevel',str(role))

	def create(self,memberID):
		nextLevel_,maximumXP = self.getLevel(level=0)

		data = {
				'XP' : 0,
				'modifier' : 1,
				'maximumXP' : maximumXP,
				'currentLevel' : nextLevel_,
				'nextLevelIndex' : 0,
				'boolMessage' : 'True',
				}
			
		self.firebase_.put(self.serverURL,f"/voiceLevels/{memberID}",data)
	
	def checkBoolMessage(self):
		data = self.firebase_.get(f"voiceLevels/{self.memberID}",'')
		boolMessage = data['boolMessage']
		return boolMessage

	def getData(self,memberID):
		result = self.firebase_.get(f"/voiceLevels/{memberID}",'')
		return result
	
	def changeMaximumXP(self,index):
		self.firebase_.put(f"voiceLevels/{self.memberID}",'maximumXP',nextXP[index])

	def changeIndex(self,index):
		self.firebase_.put(f"/voiceLevels/{self.memberID}",'nextLevelIndex',index)

	def changeModifier(self,modifier):
		self.firebase_.put(f"/voiceLevels/{self.memberID}",'modifier',modifier)
	
	def getModifier(self,location):
		with open("Files/{}.txt".format(location)) as dosya:
			okuma = dosya.read().splitlines()
			modifier = okuma[0]
			return modifier

	def getLevel(self,level):
		nextLevel_ = nextLevel[level] 
		maximumXP = nextXP[level]
		return nextLevel_, maximumXP
	
	def addXP(self,XP):
		data = self.firebase_.get(f"voiceLevels/{self.memberID}",'')
		XP_ = data['XP']
		XP_ += XP
		self.firebase_.put(f"voiceLevels/{self.memberID}",'XP',XP_)
	
	def changeBoolMessage(self,message):
		self.firebase_.put(f"voiceLevels/{self.memberID}",'boolMessage',message)


@tasks.loop(minutes=1)
async def voicech():
	vcList = [channel.id for channel in client.get_all_channels() if channel.type==ChannelType.voice]
	for channelID in vcList:
		voicechannel = client.get_channel(channelID)
		members_ = [m for m in client.get_all_members()]
		for member in members_:
			if not member.bot:
				memberID = member.id
				user = User(memberID)
			

		members = voicechannel.members

		for member in members:
			if not member.bot:
				memberID = member.id
				user = User(memberID)
				user.updateXP(memberID)
				data = user.getData(memberID)
				XP = data['XP']
				maximumXP = data['maximumXP']
				index = data['nextLevelIndex']
				currentLevel = data['currentLevel']

				if XP >= maximumXP:
					index += 1
					await user.addRole(role=nextLevel[index],member=member)
					user.changeIndex(index)
					user.changeMaximumXP(index)
					channel = client.get_channel(id=914204255894765578)
					await channel.send(f"Tebrikler <@{memberID}>! **{currentLevel}**. seviyeye ulaştın!")
			

@voicech.before_loop
async def before_voicech():
	await client.wait_until_ready()
	print("Channel Update Loop OK!")
voicech.start()



@client.command()
async def emojiMessage(ctx):
	global embeds
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
	await ctx.channel.send(embed=embed)
	embeds = [embed]
	message2 = await ctx.channel.send("Aşağıdaki emojilere basarak rollerini seçebilirsin.")
	message3 = await ctx.channel.send("Devamı ↓ ")
	for emoji in emojis:
		await message2.add_reaction(emoji)
	for emoji in emojis2:
		await message3.add_reaction(emoji)

	return embeds

@client.command()
async def embedDüzenle(ctx):
	global embeds
	print(embeds)
	embed = embeds[0]


@client.event
async def on_raw_reaction_add(payload):
	channel = payload.channel_id
	member = payload.member
	reaction = payload.emoji
	guild = client.get_guild(payload.guild_id)

	if channel == 905888377071616090:
		if member.bot:
			pass
		else:

			if str(reaction) == "🎬":
				role = get(guild.roles,name="Game Director 🎬")

			if str(reaction) == "🎮":
				role = get(guild.roles,name="Game Designer 🎮")

			if str(reaction) == "🕹️":
				role = get(guild.roles,name="Level Designer 🕹️")

			if str(reaction) == "📕":
				role = get(guild.roles,name="Script Writer 📕")

			if str(reaction) == "🌍":
				role = get(guild.roles,name="Interpreter 🌍")

			if str(reaction) == "⚠️":
				role = get(guild.roles,name="UX Designer ⚠️")

			if str(reaction) == "👍":
				role = get(guild.roles,name="Social Media Expert 👍")

			if str(reaction) == "⌨️":
				role = get(guild.roles,name="Game Developer ⌨️")

			if str(reaction) == "🎨":
				role = get(guild.roles,name="Visual Artist 🎨")

			if str(reaction) == "👾":
				role = get(guild.roles,name="Pixel Artist 👾")

			if str(reaction) == "🧊":
				role = get(guild.roles,name="3D Artist 🧊")

			if str(reaction) == "🖼️":
				role = get(guild.roles,name="2D Artist 🖼️")

			if str(reaction) == "🏃‍♀️":
				role = get(guild.roles,name="Cell Animator 🏃‍♀️")

			if str(reaction) == "💥":
				role = get(guild.roles,name="VFX Artist 💥")

			if str(reaction) == "📺":
				role = get(guild.roles,name="UI Designer 📺")

			if str(reaction) == "🎵":
				role = get(guild.roles,name="Sound Designer 🎵")

			if str(reaction) == "📣":
				role = get(guild.roles,name="Folley Artist 📣")

			if str(reaction) == "🎤":
				role = get(guild.roles,name="Voice Actor 🎤")

			if str(reaction) == "👩‍🎤":
				role = get(guild.roles,name="Singer 👩‍🎤")

			if str(reaction) == "💃":
				role = get(guild.roles,name="Dancer 💃")

			if str(reaction) == "🕵️":
				role = get(guild.roles,name="Detective 🕵️")

			if str(reaction) == "🧛":
				role = get(guild.roles,name="Vampire 🧛")

			if str(reaction) == "⚔️":
				role = get(guild.roles,name="Fighter ⚔️")

			if str(reaction) == "🏹":
				role = get(guild.roles,name="Ranger 🏹")

			if str(reaction) == "🧙‍♂️":
				role = get(guild.roles,name="Wizard 🧙‍♂️")

			if str(reaction) == "🚀":
				role = get(guild.roles,name="Astronaut 🚀")

			if str(reaction) == "🌪️":
				role = get(guild.roles,name="Duhan 🌪️")

			await member.add_roles(role)



@client.event
async def on_raw_reaction_remove(payload):
	channel = payload.channel_id
	guild = client.get_guild(payload.guild_id)
	member = guild.get_member(payload.user_id)
	reaction = payload.emoji


	if channel == 905888377071616090:
		if str(reaction) == "🎬":
			role = get(guild.roles,name="Game Director 🎬")

		if str(reaction) == "🎮":
			role = get(guild.roles,name="Game Designer 🎮")

		if str(reaction) == "🕹️":
			role = get(guild.roles,name="Level Designer 🕹️")

		if str(reaction) == "📕":
			role = get(guild.roles,name="Script Writer 📕")

		if str(reaction) == "🌍":
			role = get(guild.roles,name="Interpreter 🌍")

		if str(reaction) == "⚠️":
			role = get(guild.roles,name="UX Designer ⚠️")

		if str(reaction) == "👍":
			role = get(guild.roles,name="Social Media Expert 👍")

		if str(reaction) == "⌨️":
			role = get(guild.roles,name="Game Developer ⌨️")

		if str(reaction) == "🎨":
			role = get(guild.roles,name="Visual Artist 🎨")

		if str(reaction) == "👾":
			role = get(guild.roles,name="Pixel Artist 👾")

		if str(reaction) == "🧊":
			role = get(guild.roles,name="3D Artist 🧊")

		if str(reaction) == "🖼️":
			role = get(guild.roles,name="2D Artist 🖼️")

		if str(reaction) == "🏃‍♀️":
			role = get(guild.roles,name="Cell Animator 🏃‍♀️")

		if str(reaction) == "💥":
			role = get(guild.roles,name="VFX Artist 💥")

		if str(reaction) == "📺":
			role = get(guild.roles,name="UI Designer 📺")

		if str(reaction) == "🎵":
			role = get(guild.roles,name="Sound Designer 🎵")

		if str(reaction) == "📣":
			role = get(guild.roles,name="Folley Artist 📣")

		if str(reaction) == "🎤":
			role = get(guild.roles,name="Voice Actor 🎤")

		if str(reaction) == "👩‍🎤":
			role = get(guild.roles,name="Singer 👩‍🎤")

		if str(reaction) == "💃":
			role = get(guild.roles,name="Dancer 💃")

		if str(reaction) == "🕵️":
			role = get(guild.roles,name="Detective 🕵️")

		if str(reaction) == "🧛":
			role = get(guild.roles,name="Vampire 🧛")

		if str(reaction) == "⚔️":
			role = get(guild.roles,name="Fighter ⚔️")

		if str(reaction) == "🏹":
			role = get(guild.roles,name="Ranger 🏹")

		if str(reaction) == "🧙‍♂️":
			role = get(guild.roles,name="Wizard 🧙‍♂️")

		if str(reaction) == "🚀":
			role = get(guild.roles,name="Astronaut 🚀")

		if str(reaction) == "🌪️":
			role = get(guild.roles,name="Duhan 🌪️")

		await member.remove_roles(role)
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






@client.command(aliases=["level"])
async def seviye(ctx,member:discord.Member=None):
	if member == None:
		member = ctx.author
		memberName = ctx.author.name
		memberID = ctx.author.id
	else:
		memberID = member.id
		memberName = member.name

	user = User(memberID)
	data = user.getData(memberID)
	XP = data['XP']
	currentLevel = data['currentLevel']
	maximumXP = data['maximumXP']
	nextXP = maximumXP-XP
	nextLevelIndex = data['nextLevelIndex']
	# with open(f"voiceLevels/{member.name}-{memberID}.txt") as dosya:
	# 	okuma = dosya.read().splitlines()
	# 	XP = int(okuma[0])
	# 	rütbe = okuma[2]
	# 	level = okuma[3]
	# 	nextInt = int(okuma[3])
	# 	_nextXP = nextXP[nextInt-1] - XP
	if nextLevelIndex == 9:
		embed = discord.Embed(title=f"{memberName}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
		embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = {}\n Puanı = **{}**\n Rütbesi = **{}**\n".format(nextLevelIndex,XP,currentLevel),inline=False)
		embed.add_field(name="Bir sonraki değerler - 🚀 ",value="Maksimum seviyeye ulaştınız!",inline=False)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=f"{memberName}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
		embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\nRütbesi = **{}**".format(nextLevelIndex,XP,currentLevel),inline=False)
		embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{nextLevel[nextLevelIndex+1]}** rütbesi için kalan puan = **{nextXP}**",inline=False)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)


@client.command()
async def emojiekle(ctx,emoji):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		channel = get(ctx.guild.channels,id=905888377071616090)
		emoji = str(emoji)
		message = await channel.fetch_message(911627238250782790)
		await message.add_reaction(emoji=emoji)
	else:
		pass
@client.command()
async def clear(ctx,amount=1):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		await ctx.channel.purge(limit=amount+1)
		await ctx.channel.send("{} mesaj silindi! ✅".format(amount))
		await asyncio.sleep(3)
		await ctx.channel.purge(limit=1)
	else:
		await ctx.channel.send("Bu komutu kullanmaya izniniz yok!")

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
		memberName = member.name
		user = User(memberID)
		memberName_ = f"{member.display_name} [ A.K.A : {member.name} ]"
		if not member.bot:
			data = user.getData(memberID)
			XP = data['XP']
			currentLevel = data['currentLevel']
			di[memberName_] = [XP,currentLevel]
			sözlük = dict(sorted(di.items(),key=lambda item:item[1],reverse=True))
		else:
			pass

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
					user = User(memberID)
					user.addXP(10000)
		
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
					user = User(memberID)
					user.addXP(5000)
					
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
					user = User(memberID)
					user.addXP(2000)

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
					user = User(memberID)
					user.addXP(1000)

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
async def _kişiselpuan(ctx:SlashContext,member:discord.Member,puan:int):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		memberID = member.id
		memberName = member.name
		user = User(memberID)
		user.addXP(puan)
		
		embed=discord.Embed(title="Puan ekleme işlemi",description=f"**{memberName}** adlı kullanıcıya **{puan}** puan eklendi!",color=member.top_role.color)
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
	message = message or "Bu mesaj DM yoluyla gönderildi"
	await user.send(message)
client.run(TOKEN)

