import logging, coloredlogs
from threading import Thread
from time import sleep

from modules.config import *
from modules.database import Database
from modules.commandmanager import CommandManager
from modules.commandtext import commands, advanced_commands

from modules.api import API
# from modules.modules.time import Time
from modules.modules.playsound import PlaySound
from modules.modules.followalert import FollowAlert

# Working in V3
from modules.modules.Points import Points
from modules.modules.Roulette import Roulette
from modules.modules.raffle import Raffle
from modules.modules.giveaway import Giveaway
from modules.modules.duel import Duel
from modules.modules.uptime import Uptime
from modules.modules.localtime import LocalTime
from modules.modules.adminpoints import AdminPoints
from modules.modules.AdminCommands import AdminCommands
from modules.modules.zoltar import Zoltar
from modules.modules.Twitter import Twitter
from modules.modules.FollowAge import FollowAge

# from modules.Sockets.SongRequest import SongRequest

from modules.modules.showemote import ShowEmote

database = Database(db_host, db_user, db_pass, db_name, db_autocommit)
database.database_connection()

class Command:

	def __init__(self, line, user):
		self.line = line
		self.user = user
		self.command = self.line.split(" ")[0].strip()
		self.commands = commands
		self.advanced_commands = advanced_commands
		# self.time = Time()
		# self.playsound = PlaySound(self.user, PLAYSOUND_COST)
		# self.followalert = FollowAlert('FollowAlert')
		self.api = API(1)

	def return_command(self):
		from modules.bot import bot_msg, bot_msg_raw
		try:
			command_check = CommandManager(self.line)
			parameter_2 = command_check.get_message_word(1).strip()
		except IndexError or NameError:
			parameter_2 = None
		try:
			command_check = CommandManager(self.line)
			parameter_3 = command_check.get_message_word(2).strip()
		except:
			parameter_3 = None

		# Text commands from database
		try:
		 	output = database.db_get_command(self.command, self.user)
		 	response = self.response_parse(output, parameter_2, parameter_3)

		 	print(str(response))

		 	bot_msg(response)
		 	return ""
		except:
		 	pass

		# Create advanced command objects
		command_objects = [Duel(self.user, parameter_2, parameter_3),
						   Points(self.user, parameter_2),
						   Raffle(self.user, parameter_2, 10),
						   Uptime(),
						   LocalTime(),
						   AdminPoints(self.user, parameter_2, parameter_3),
						   AdminCommands(self.user, parameter_2, self.line.replace(parameter_2, '', 1).replace(self.command, '', 1) if parameter_2 is not None else 'error'),
						   Zoltar(self.user, self.line),
						   Roulette(self.user, parameter_2),
						   Twitter(self.user),
						   FollowAge(self.user, parameter_2)
						   # SongRequest(self.user, parameter_2),
						  ]

		print('command:', self.command)

		# Advanced commands
		for command_object in command_objects:
			try:
				if self.command == command_object.CommandMain or self.command in command_object.CommandMainOptions:
					print("{} command found - {}".format(command_object.CommandMain, self.command))
					command_object.execute_command(self.command)
					break
				if self.command in command_object.CommandResponses:
					print("{} command response found".format(self.command))
					command_object.execute_command_response(self.command)
					break
			except Exception as e:
				print(e)
				pass
		return ""

	def response_parse(self, response, variable_2, variable_3):
		try:
			output = response.replace('{x}', variable_2)
			if variable_3 is None:
				return output
			else:
				output = output.replace('{y}', variable_3)
				return output
		except:
			return response

		# if cmd == 'enter' and Giveaway.GiveawayActive and self.user not in Giveaway.GiveawayEntries:
		# 	Giveaway.GiveawayEntries.append(self.user)
		# 	return ""
		# if cmd == 'enter':
		# 	return ""
			
			# if cmd == 'giveaway':
			# 	command_text = self.line.replace(var2, '').replace(cmd, '')
			# 	giveaway = Giveaway(int(var2), command_text)
			# 	giveaway.start_giveaway()
			# 	return ""