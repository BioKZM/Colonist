import discord
import os
# import sys
import asyncio
import random
from discord.ext import commands,tasks
from discord.utils import get
from keep_alive import keep_alive
# from discord_ui import * 
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
# from Files.levels import nextXP, nextLevel
from discord import ChannelType
from firebase import firebase
from functions.embed import botEmbed
from functions.classes import User,experiences,levelNames

global message2
global message3
embeds = []


TOKEN = os.environ["TOKEN"]
serverURL = os.environ["serverURL"]

keep_alive()
firebase = firebase.FirebaseApplication(serverURL,None)
client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
intents = discord.Intents.all()
intents.members = True
# ui = UI(client)
slash = SlashCommand(client,sync_commands=True)
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
	User(member.id)

@client.event
async def on_message(message):
	channel = str(message.channel)
	memberID = message.author.id
	if not message.author.bot:
		user = User(memberID)
		if channel == "kendini-tanıt":
			if user.boolMessage == "True":
				user.addXP(250)
				user.update('boolMessage','False')
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
		# liste = ["Game Director 🎬","Game Designer 🎮","Level Designer 🕹️","Script Writer 📕","Interpreter 🌍","UX Designer ⚠️","Social Media Expert 👍","Game Developer ⌨️","Visual Artist 🎨","Pixel Artist 👾","3D Artist 🧊","2D Artist 🖼️","Cell Animator️ 🏃‍♀️","VFX Artist 💥","UI Designer 📺","Sound Designer 🎵","Folley Artist 📣","Voice Actor 🎤","Singer 👩‍🎤","Dancer 💃","Detective 🕵️","Vampire 🧛","Fighter ⚔️","Ranger 🏹","Wizard 🧙‍♂️","Astronaut 🚀","Duhan 🌪️"]

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
	if prev.channel and cur.channel:
		if not member.bot:
			user = User(member.id)
			
			if memberSituation(prev,cur) == "stream":
				modifier = user.getModifier(location="Yayın Çarpanı")
				user.update("modifier",modifier)

			elif memberSituation(prev,cur) == "cam":
				modifier = user.getModifier(location="Kamera Çarpanı")
				user.update("modifier",modifier)

			elif memberSituation(prev,cur) == "stream + cam":
				camModifier = user.getModifier(location="Kamera Çarpanı")
				streamModifier = user.getModifier(location="Yayın Çarpanı")
				modifier = camModifier + streamModifier
				user.update("modifier",modifier)
		
			elif memberSituation(prev,cur) == "":
					modifier = user.getModifier(location="Dakika Çarpanı")
					user.update("modifier",modifier)
					


@tasks.loop(minutes=1)
async def voicech():
	guild = client.guilds[0]
	vcList = [channel.id for channel in client.get_all_channels() if channel.type==ChannelType.voice]
	for channelID in vcList:
		voicechannel = client.get_channel(channelID)
		members = voicechannel.members
		
		# Level değerleri yerine XP değerleri yerleştirilip
		# o şekilde değerlendirilecek.


		for member in members:
			if not member.bot:
				user = User(member.id)
				user.updateXP()
				# kullanıcının puan şuanki levelinin puanından yüksekse
				# levelNames[user.level-1]
				
				if not user.haveMaxLevel():
					if user.XP >= user.currentLevelMaxXP:
						user.level = user.getLevel(user.XP)
						user.putLevel(user.level)
						user.levelName = levelNames[user.level-1]
						role = get(guild.roles, name=user.levelName)
						await member.add_roles(role)
						print(role)
						
						# send notification
						channel = client.get_channel(id=910547555245494322)
						await channel.send(f"Tebrikler <@{member.id}>! **{user.level}**. seviyeye ulaştın!")
						await asyncio.sleep(3)
		

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


@client.command(aliases=["level"])
async def seviye(ctx,member:discord.Member=None):
	# levelNames[(user.level)-1])
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
		async with ctx.typing():
			await asyncio.sleep(1)
			embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
			embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\n Rütbesi = **{}**\n".format(user.level,user.XP,user.levelName,inline=False))
			if user.haveMaxLevel():
				embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-1])-user.XP}**" if not user.haveMaxLevel() else "Maksimum seviyeye ulaştınız!",inline=False)
			elif not user.haveMaxLevel():
				if experiences[user.level-1] - user.XP <= 0:
					embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.getLevel(user.XP)-1]}** rütbesine ulaştın! Seviye atlamak için ses kanalına girebilirsin.",inline=False)
				else:
					embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-1])-user.XP}**",inline=False)


		# embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level])-user.XP}**" if not user.haveMaxLevel() else "Maksimum seviyeye ulaştınız!",inline=False)
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

def changeModifier(location,modifier):
	# firebase = firebase.FirebaseApplication(serverURL,None)
	firebase.put(f"modifiers/{location} Çarpanı",'modifier',modifier)

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
		# Change Multiplier
		changeModifier(görüntü,çarpan)
		# with open(f"Files/{görüntü} Çarpanı.txt","w") as dosya:
		# 	dosya.write(str(çarpan))
		# 	dosya.close()
		await ctx.send(embed=botEmbed(ctx.guild,client,f"{görüntü} çarpanı şu değere değiştirildi! = **{çarpan}**",f"{görüntü} çarpanı değişimi!"))
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")

def getSortedMembers(ctx):
	di = {}
	for member in ctx.guild.members:
		user = User(member.id)
		memberName_ = f"{member.display_name} [ A.K.A : {member.name} ]"
		if not member.bot:
			di[memberName_] = [user.XP,user.levelName]
			sortedMembers = dict(sorted(di.items(),key=lambda item:item[1],reverse=True))
		else:
			pass
	return sortedMembers

@client.command(aliases=["rank"])
async def sıralama(ctx):
	async with ctx.typing():
		sortedMembers = getSortedMembers(ctx)
	
		embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		# Add fields
		count = 1
		
		await asyncio.sleep(1)
		for key,value in sortedMembers.items():
			embed.add_field(name="{} - {}".format(count,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
			count += 1
			if count == 11:break

		await ctx.send(embed=embed)


def __addPointToSpaceShip(members, platform, shipRole):
	for member in members:
		if shipRole in member.roles:
			user = User(member.id)
			user.addXP(platformXPs[platform])
platformXPs = {
		"PC":10000,
		"Mobil":5000,
		"Hypercasual":2000,
		"GameJam":1000
	}
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
async def _gemipuan(ctx:SlashContext,platform:str,gemi:str):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		shipRole = get(ctx.guild.roles,name=str(gemi))
		embed = discord.Embed(title="Puan Artışı",description=f"**{shipRole.mention}** adlı geminin mürettebatına **{platformXPs[platform]}** puan eklendi!")
		await ctx.send(embed=embed)
		# await ctx.send(embed=botEmbed(ctx.guild,client,description=f"**{shipRole.mention}** adlı geminin mürettebatına **{platformXPs[platform]}** puan eklendi", title="Puan Artışı"))
		__addPointToSpaceShip(ctx.guild.members, platform, shipRole)



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
		user = User(kullanıcı.id)
		user.addXP(puan)
		
		embed=discord.Embed(title="Puan ekleme işlemi",description=f"**{kullanıcı.name}** adlı kullanıcıya **{puan}** puan eklendi!",color=kullanıcı.top_role.color)
		await ctx.send(embed=embed)
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")


""" 
	TEST COMMANDS
"""

# @client.command() x	xxx
# async def sustur(ctx):
# 	if isinstance(ctx.channel,discord.channel.DMChannel):
# 		member = get(client.get_all_members(), id=275971871047024640)
# 		await member.edit(mute = True)
		# channel = client.get_channel(id=860636538701611050)
		# await channel.send("İşlem tamam")

# @client.command()
# async def DM(ctx,user:discord.Member,*,message=None):
# 	await ctx.message.delete()
# 	message = message or "Bu mesaj DM yoluyla gönderildi"
# 	await user.send(message)


client.run(TOKEN)

