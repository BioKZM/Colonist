import discord
from discord.ext import commands
import os
from firebase import firebase
from discord.utils import get

client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
 
serverURL = "https://colonist-test-default-rtdb.firebaseio.com/"

experiences = [99,699,1987,6666,9999,30000,90000,300000,900000,10000001]
levelNames = ["Unit","Guest","Colony Member","Open Crew","Crew","Captain","Judge","Colony Manager","Mars Lover","Chief of the Colony","Partner"] 
		





# class Modifier():


class User():
	def __init__(self,id_):
		self.id = id_
		self.serverURL = serverURL
		self.guild = client.get_guild(888759899226538025)
		self.firebase_ = firebase.FirebaseApplication(serverURL,None)
		# self.XP, self.boolMessage,self.level,self.modifier = self.getData(self.id)
		# print(self.XP) 
		# self.level = self.getLevel(self.XP)
		# print(self.level)
		# self.levelName = levelNames[self.level]
		# self.level, self.levelName 

		try:
			self.__setVariables()
			# self.XP, self.boolMessage,self.modifier = self.getData(self.id_)
			# self.getLevel(self.XP)
			
			# self.levelName = levelNames[self.level]
		except AttributeError:
			if self.__userNotExists() == None:
				self.__create(self.id)
				# self.XP, self.boolMessage,self.modifier = self.getData(self.id)
				self.__setVariables()
				# self.level = self.getLevel(self.XP)
				# self.levelName = levelNames[self.level]
			else:
				print("Veriler hatalı")

	
		
	# async def addRole(self,role,member):
	# 	await member.add_roles(role)
		


	# 	self.firebase_.put(self.serverURL,f"/voiceLevels/{self.id}",data)
	
	def haveMaxLevel(self):
		return True if self.level == len(experiences)+1 else False



	def getModifier(self,location):
		modifier = self.firebase_.get(f"modifiers/{location}",'')
		return modifier

	def getLevel(self,XP):
		for level in range(0,len(experiences)+1):
			if XP < 99:
				level = 1
				return level
			if level < 3:
				if experiences[level-1] <= XP and experiences[level] >= XP:	
					level = level+1
					return level
			if level > 2:
				if experiences[level-2] <= XP and experiences[level-1] >= XP:	
					level = level
					return level
			if XP >= experiences[-1]:
				level = len(experiences)+1
				return level																		

	def putLevel(self,level):
		# 99 699 1987 6666 9999

		# for level in range(0,len(experiences)-1):
		# 	if XP < 99:
		# 		self.level = 1
		# 	if experiences[level-2] <= XP and experiences[level-1] > XP:	
		# 		self.level = level
		# 	if XP >= experiences[-1]:
		# 		self.level = len(experiences)+1
		
		self.firebase_.put(f"voiceLevels/{self.id}",'level',level)

	def updateXP(self):
		"""
			Kullanıcıların puanlarını o anki durumlarına göre çarparak ekler
		"""
		self.addXP(self.modifier)

	def addXP(self,XP):
		self.update("XP",self.XP+XP)
		# print(f"BF : {self.beforeLevel} , XP : {self.XP} , level : {self.level}")
		# print(f"Before level : {self.beforeLevel}")
		
		# self.beforeLevel = self.getLevel(self.XP)
		# self.XP += XP

		# print(f"Level : {self.level}")
		# if self.beforeLevel != self.level:
		# 	print("Seviye atlandı!")
		# print(f"NE: {self.beforeLevel} , XP : {self.XP} , level : {self.level}")
		
	
	def update(self,variable,value):
		self.firebase_.put(f"voiceLevels/{self.id}",variable,value)

	def __getData(self,id):
		result = self.firebase_.get(f"/voiceLevels/{id}",'')
		return result.values()
	
	def __setVariables(self):
		self.XP, self.boolMessage,self.level,self.modifier = self.__getData(self.id)
		# self.level = self.getLevel(self.XP)
		self.levelName = levelNames[self.level-1]
		if not self.level == 11:
			self.currentLevelMaxXP = experiences[self.level-1]
		# self.level = self.getLevel(self.XP)
		# self.beforeLevel = self.level
		# self.levelName = levelNames[self.level]

	def __userNotExists(self): 
		self.file_there = self.firebase_.get(self.serverURL,f"/voiceLevels/{self.id}")
		return self.file_there
	
	def __create(self,id):
		data = {
				'XP' : 0,
				'level' : 1,
				'modifier' : 1,	
				'boolMessage' : 'True',
				}
		self.firebase_.put(self.serverURL,f"voiceLevels/{id}",data)