import os
import json
from main import client


experiences = [250,1987,6666,9999,30000,90000,300000,900000,10000001]
levelNames = ["Guest","Colony Member","Open Crew","Crew","Captain","Judge","Colony Manager","Mars Lover","Chief of the Colony","Partner"] 



class User():
	def __init__(self,memberID):
		self.id = memberID
		self.guild = client.get_guild(888759899226538025)
		self.path = f"userFiles/levels/{self.id}.json"

		if self.__userFile() == False:
			self.__create()
			self.__getVariables()
		else:
			self.__getVariables()


	def isMaxLevel(self):
		if self.level == len(experiences) +1:
			return True
		else:
			return False

	def getModifier(self,modifierType):
		with open(f"userFiles/modifiers.json") as file:
			data = json.load(file)
		
		return data[modifierType]

	def update(self,variable,value):
		self.data[variable] = value
		self.__writeUserFile()

	def updateXP(self):
		self.update('XP',self.XP + self.modifier)

	def addXP(self,XP):
		self.update('XP',self.XP + XP)

	def addLevel(self):
		with open(f"userFiles/levels/{self.id}") as file:
			data = json.load(file)
			data['level'] += 1

		with open(f"userFiles/levels/{self.id}","w") as file:
			json.dump(data,file,indent=4)
        

	def __userFile(self):
		if os.path.exists(self.path):
			return True
		else:
			return False

	def __writeUserFile(self):
		with open(self.path,"w") as file:
			json.dump(self.data,file,indent = 4)


	def __getVariables(self):
		with open(self.path) as file:
			self.data = json.load(file)
		
		self.XP = self.data['XP']
		self.level = self.data['level']
		self.modifier = self.data['modifier']
		# self.currentLevelMaximumXP = self.data['currentLevelMaximumXP']
		self.messageBool = self.data['messageBool'] 
		self.currentLevelMaximumXP = experiences[self.data['level']]
		self.levelName = levelNames[self.data['level']]
			
	def __create(self):
		self.data = {
                'XP' : 0,
                'level' : 0,
                'modifier' : 1,
                'maximumXP' : 250,
                'messageBool' : True,
            }
		with open(self.path,"w") as file:
			json.dump(self.data,file,indent = 4)
