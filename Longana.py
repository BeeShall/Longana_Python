from Tournament import Tournament
from Human import Human
from Computer import Computer

class Longana:
	def __init__(self):
		pass

	def start(self):
		print('-' * 44)
		print("Welcome to Longana!")
		print('-' * 44)
		print()

		score = ''
		while not score.isdigit():
			score = input("Please enter a tournament score: ")
		score = int(score)

		noOfPlayers = ''
		while not noOfPlayers.isdigit():
			noOfPlayers = input("How many players do you want to play? ")
		noOfPlayers = int(noOfPlayers)

		players = []
		print("Please enter the player type for all the players (h for human and c for computer): ")
		for i in range(0,noOfPlayers):
			playerType = ''
			while (not playerType == 'h') and (not playerType == 'c'):
				playerType = (input(i+1)).lower()

			name = input("Enter player name: ")

			if playerType is 'h':
				players.append(Human(name, 0, name))
			else:
				players.append(Computer(name, 0, name))

		t = Tournament(score,players)
		t.start()


l = Longana()
l.start()