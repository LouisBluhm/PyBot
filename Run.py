import string
import re
import time

from Read import getUser, getMessage, uptime, get_points, localtime, roulette, followage, raffle, mod_check
from TheSocket import openSocket, sendMessage, sendWhisper
from Initialize import joinRoom
from Commands import commands

s = openSocket()
joinRoom(s)
readbuffer = ""

while True:
		readbuffer = readbuffer + s.recv(1024).decode('UTF-8')
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)

			if "PING :tmi.twitch.tv" in line:
				#s.send(bytes(line.replace("PING", "PONG"), 'UTF-8'))
				response = "PONG :tmi.twitch.tv\r\n"
				print(response)
				#print(response)
				bytes_response = str.encode(response)
				#print(bytes_response)
				s.send(bytes_response)
				break
			user = getUser(line)
			message = getMessage(line)
			print(user + " typed :" + message)

			# advanced commands
			if "!uptime" in message:
				#uptime()
				sendMessage(s, uptime())
			if "!localtime" in message:
				sendMessage(s, localtime())
			if "!points" in message:
				sendMessage(s, get_points(user))
			if "!followage" in message:
				sendMessage(s, followage(user))

			# raffle
			raffle_amount = re.findall('\d+', message)
			y = str(raffle_amount)
			if ("!raffle") in message:
				if(mod_check(user)):
					new_y = int(re.search(r'\-?\d+', y).group())
					output = "Raffle for " + str(new_y) + " points has begun. Type Kappa to enter!"
					sendMessage(s, str(output))
					time.sleep(15)
					sendMessage(s, "The raffle ends in 15 seconds!")
					time.sleep(15)
					sendMessage(s, raffle(user, new_y))
				else:
					sendMessage(s, "Only mods can set raffles FailFish")


			# roulette
			amount = re.findall('\d+', message)
			x = str(amount)

			# print("check this to see if int: ", x)
			# print(type(x))

			if ("!roulette") in message:
				if(roulette(user, x) == False):
					roulette_error = user + ", you can only enter integer values."
					sendMessage(s, roulette_error)
					#sendWhisper(s, user, roulette_error)
				else:
					sendMessage(s, roulette(user, x))


			# basic commands
			if "!admin" in message:
				sendMessage(s, commands.get('admin'))
			if "!commands" in message or "!help" in message:
				sendMessage(s, user + commands.get('commands'))
			if "!twitter" in message:
				sendMessage(s, commands.get('twitter'))
			if "!discord" in message:
				sendMessage(s, commands.get('discord'))
			if "!spooky" in message:
				sendMessage(s, commands.get('spooky'))
			if "!coloring" in message:
				sendMessage(s, commands.get('coloring'))