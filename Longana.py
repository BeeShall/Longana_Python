from Tournament import Tournament
from Human import Human
from Computer import Computer
import json


class Longana:
	def __init__(self):
		pass

	def start(self):
		print('-' * 44)
		print("Welcome to Longana!")
		print('-' * 44)
		print()
		choice = ''
		while (choice != 'y') and (choice != 'n'):
			choice = input("Would you like to load a game? (y/n): ").lower()

		if choice == 'y':
			self.load()
		else:
			self.newGame()


	def load(self):
		fileOK = False
		while not fileOK:
			fileName = input("Please enter the file name to load: ")
			try:
				data = json.load(open('./serial/'+fileName+'.json'))
				t = Tournament()
				t.load(data)
				fileOK = True
			except OSError:
				print("File not found! Please try again!")

	def newGame(self):
		score = ''
		while not score.isdigit():
			score = input("Please enter a tournament score: ")
		score = int(score)

		noOfPlayers = 0
		while noOfPlayers <1 or noOfPlayers >4  :
			noOfPlayers = input("How many players do you want to play? ")
			if (noOfPlayers.isdigit()):
				noOfPlayers = int(noOfPlayers)
			else:
				noOfPlayers = 0
		

		players = []
		sides = ['l','r','t','b']
		humanPlayerEnough = False
		computerPlayerEnough = False

		while (not humanPlayerEnough) or (not computerPlayerEnough):
			print("Please enter the player type for all the players (h for human and c for computer): ")
			players.clear()
			for i in range(0, noOfPlayers):
				playerType = ''
				while (playerType != 'h') and (playerType != 'c'):
					playerType = (input(i + 1)).lower()

				name = input("Enter player name: ")

				if playerType == 'h':
					humanPlayerEnough = True
					players.append(Human(name, 0, sides[i]))
				else:
					computerPlayerEnough = True
					players.append(Computer(name, 0, sides[i]))
			
			if not humanPlayerEnough:
				print("Not enough human players!!!")
				computerPlayerEnough = False
			elif not computerPlayerEnough:
				humanPlayerEnough = False
				print("Not enough computer players!!")

		t = Tournament(score, players)
		t.start()


l = Longana()
l.start()
