import logging

from common import *
from typing import *

tableLogger = logging.Logger("Table")

class Options:
	"""
	Options is an abstraction over poker table options.

	Attributes
	----------
	seats:
		the maximum number of players that can play at any given moment
	stags: int
		the mask containing the phases of the poker game to be played
		can be: PREFLOP, FLOP, TURN, RIVER, ALL
	showm:
		the mask containing the phases of the poker game to be displayed via
		print method; can be: PREFLOP, FLOP, TURN, RIVER, ALL
	print:
		print function to be used

	Methods
	-------
	Default()
		returns a default configuration:
	"""

	def __init__(self, seats:int, stages:int, show:int, logger):
		self.seats = seats
		self.stags = stages
		self.showm = show
		self.print = logger

	@staticmethod
	def Default():
		return Options(seats=10, stages=ALL, show=ALL, logger=print)

	@property
	def SeatNo(self):
		return self.seats

	@property
	def Stages(self):
		return self.stags

	@property
	def ShwMsk(self):
		return self.showm

	@property
	def Printf(self):
		return self.print


class Table:
	"""
	Table is an abstraction over a poker table.

	Attributes
	----------
	ID: int
		a global ID to increment so every table has a unique id.
	ON: Set[Table]
		a set of tables that are online (active)

	id: int
		id of the table
	plyrs: List[Player]
		the players enrolled at the table, that are currenly playing
	print: Callable
		the print function to use when printing
	confg: Options
		encloses poker table options such as: verbose, seats number, game stages

	Methods
	-------
	playOnce()
		runs one game of poker
	"""

	__ID:int = 0
	ON:Set["Table"] = set()

	def __init__(self, confg:Options=Options.Default()):
		self.id: int = self.__ID
		self.__ID += 1

		self.confg: Options = confg
		self.plyrs: Players = []
		self.cards: Deck = []

		self.ON.add(self)

	def __repr__(self):
		# Winner color, winner attributes, used only to pretty print them
		wclr, watr = 'on_yellow', ['bold', 'blink']
		pcmp = lambda p: Hands.BestHand(p.hand + self.cards)[1]
		srtd = sorted(self.plyrs, key = pcmp)
		winr = srtd[-1]
		repr = ""

		for player in srtd:
			status, hand = Hands.BestHand(player.hand + self.cards)
			stat = "%15s" % status
			hand = str(hand)

			agRepr = str(player) + f"{stat} {hand}"
			if hand == Hands.BestHand(winr.hand + self.cards):
				agRepr = colored(agRepr, on_color=wclr, attrs=watr)
			repr += agRepr + "\n"
		repr += "\nTable:" + str(Deck(self.cards)) + "\n"
		return repr

	def join(self, player:Player) -> bool:
		if len(self.plyrs) >= self.confg.SeatNo:
			tableLogger.warn("table full")
			return False
		self.plyrs.append(player)
		return True

	def left(self, player:Player) -> bool:
		if player in self.plyrs:
			self.plyrs.remove(player)
			return True
		return False

	def play(self):
		deck = Deck.Generate(shuffle=True)

		def playStage(deck, stage):
			_ = deck.Draw(1) # burn 1
			if stage & PREFLOP:
				self.plyrs = [p._replace(hand=deck.Draw(2)) for p in self.plyrs]
				return deck.Draw(0)
			elif stage & FLOP:
				return deck.Draw(3)
			elif stage & TURN:
				return deck.Draw(1)
			elif stage & RIVER:
				return deck.Draw(1)

			tableLogger.warn("invalid stage :%d" % stage)
			return []

		def prettySep(keyword, length=80):
			sepLength = len(keyword)
			hashtgLen = length // 2 - sepLength // 2
			separator = ("#" * hashtgLen) + keyword + ("#" * hashtgLen)
			separator += "#" * (length - len(separator))
			return separator

		stages = [PREFLOP,    FLOP,   TURN,   RIVER]
		titles = ["PREFLOP", "FLOP", "TURN", "RIVER"]
		for stage, title in zip(stages, titles):
			if self.confg.Stages & stage:
				self.cards.extend(playStage(deck, stage))
			if self.confg.ShwMsk & stage:
				self.confg.Printf(prettySep(" " + title + " "))
				self.confg.Printf(self)

		self.cards.clear()
