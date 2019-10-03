from termcolor import colored

from collections import *
from typing import *

import numpy as np
import random
import logging

__cardlogr = logging.getLogger("Card")
__decklogr = logging.getLogger("Deck")
__handlogr = logging.getLogger("Hand")

# SUITS are the possible suits for the cards in a regular poker game.
SUITS = "♠ ♡ ♢ ♣".split()

# RANKS are the possible suits for the cards in a regular poker game.
RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()

# Stages of the poker game.
SILENT, PREFLOP, FLOP, TURN, RIVER, ALL = 0, 1, 2, 4, 8, 15

# Type alias to represent a basic poker card.
Card = Tuple[str, str]

class ESUITS:
	"""
	Enum like class, with readable members for card suits.

	Attributes
	----------
	CLUBS:   '♣'
	HEARTS:  '♡'
	SPADES:  '♠'
	DIAMOND: '♢'
	ALL: a list of all the possible suits as string
	"""
	CLUBS = '♣'
	HEARTS = '♡'
	SPADES = '♠'
	DIAMOND= '♢'
	ALL = SUITS

class ERANKS:
	"""
	Enum like class, with readable members for card suits.

	Attributes
	----------
	ALL: a list of all the possible ranks: 2, 3, 4, 5, ..., J, Q, K, A

	Methods:
	fromIdx(rank):
	fromRnk(rank):
	"""
	ALL = RANKS
	@staticmethod
	def fromIdx(rank:int) -> str:
		if rank <= 0 or rank >= len(ERANKS.ALL):
			return ERANKS.ALL[-1]
		return ERANKS.ALL[rank - 1]

	@staticmethod
	def asIndex(rank:str) -> int:
		if rank not in RANKS:
			return -1
		if rank == 'A':
			return [1 + ERANKS.ALL.index(rank), 0]
		return [1 + ERANKS.ALL.index(rank)]

class PokerCard:
	def __init__(self, tpl):
		self.suit = tpl[0]
		self.rank = tpl[1]

	def __hash__(self):
		return hash(self[0]) ^ hash(self[1])

	def __eq__(self, other):
		return self[0] == other[0] and self[1] == other[1]

	def __getitem__(self, index):
		if index < 0 or index >= 2:
			__cardlogr.warn("%d is invalid index for card", index)

		if index == 0:
			return self.suit
		return self.rank

	def __repr__(self):
		suit2Color = {
			"♠": None, # for black
			"♣": "green",
			"♡": "red",
			"♢": "blue",
		}
		if self[0] not in suit2Color:
			return "   "
		return colored(self[0] + "%2s" % self[1], suit2Color[self[0]])

	@staticmethod
	def OfSuit(suit:str) -> Callable[["Card"], bool]:
		return lambda card: card[0] == suit

	@staticmethod
	def OfRank(rank:str) -> Callable[["Card"], bool]:
		return lambda card: card[1] == rank

class Deck(list):
	def __init__(self, cards):
		for card in cards:
			self.append(PokerCard(card))
			#self.append(card)

	def __repr__(self):
		scard = "|".join(str(PokerCard(card)) for card in self)
		return f"|{scard}|"

	def __eq__(self, that:"Deck"):
		print("__eq__")
		selfHandPowr = Hands.Powr(Hands.BestHand(self)[0])
		thatHandPowr = Hands.Powr(Hands.BestHand(that)[0])
		if selfHandPowr != thatHandPowr:
			return False
		for c1, c2 in zip(self, that):
			c1, c2 = ERANKS.asIndex(c1.rank)[0], ERANKS.asIndex(c2.rank)[0]
			if c1 != c2:
				return False
		return True

	def __lt__(self, that:"Deck"):
		selfHandPowr = Hands.Powr(Hands.BestHand(self)[0])
		thatHandPowr = Hands.Powr(Hands.BestHand(that)[0])
		if selfHandPowr != thatHandPowr:
			return selfHandPowr < thatHandPowr
		for c1, c2 in zip(self, that):
			c1, c2 = ERANKS.asIndex(c1.rank)[0], ERANKS.asIndex(c2.rank)[0]
			if c1 > c2:
				return False
			if c1 < c2:
				return True
		return False

	def __gt__(self, that:"Deck"):
		selfHandPowr = Hands.Powr(Hands.BestHand(self)[0])
		thatHandPowr = Hands.Powr(Hands.BestHand(that)[0])
		if selfHandPowr != thatHandPowr:
			return selfHandPowr > thatHandPowr
		for c1, c2 in zip(self, that):
			c1, c2 = ERANKS.asIndex(c1.rank)[0], ERANKS.asIndex(c2.rank)[0]
			if c1 > c2:
				return True
			if c1 < c2:
				return False
		return False

	def __add__(self, that):
		temp = self[:]
		temp.extend(that)
		return Deck(temp)

	def Draw(self, count):
		drawn = self[:count]
		for i in range(count):
			self.pop(0)
		return Deck(drawn)

	def Freq(self) -> Dict[str, int]:
		freq = defaultdict(lambda: 0)
		for card in self:
			freq[card.suit] += 1
			freq[card.rank] += 1
		sortd = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
		freq = OrderedDict(sortd)
		return freq

	def MostFreq(self, what:str="rank") -> str:
		domain = RANKS if what == "rank" else SUITS
		freqList = list(self.Freq().keys())
		for i in range(len(freqList) - 1, -1, -1):
			if freqList[i] in domain:
				return freqList[i]
		return freqList[-1]

	def TopN(self, numb:int, used:Set[Card]) -> "Deck":
		bign = Deck([])
		for card in self:
			if len(bign) == numb:
				break
			if card not in used:
				bign.append(card)
		return bign.Sort()

	def Sort(self) -> "Deck":
		rankComp = lambda card: ERANKS.asIndex(card.rank)
		return Deck(sorted(self[:], key=rankComp, reverse=True))

	def Only(self, ofSuit=None, ofRank=None) -> "Deck":
		if not ofSuit and not ofRank:
			return self
		if ofSuit:
			predicate = PokerCard.OfSuit(ofSuit)
		if ofRank:
			predicate = PokerCard.OfRank(ofRank)
		return Deck(card for card in self if predicate(card))

	def ACard(self, ofSuit=None, ofRank=None) -> "Deck":
		return self.Only(ofSuit, ofRank)[:1]

	@staticmethod
	def Generate(shuffle=False) -> "Deck":
		deck = Deck([(s, r) for r in RANKS for s in SUITS])
		if shuffle:
			random.shuffle(deck)
		return deck

Hand = Deck
Player = namedtuple('Player', 'name cash hand bet playing')

def playerRepr(this) -> str:
	assert isinstance(this, Player)
	player = this
	stat2colr = {
		True: "blue",
		False: "magenta",
	}
	colr = stat2colr[player.playing]
	name = "%15s" % colored(player.name, colr)
	cash = " %5d" % player.cash
	bett = " %5d" % player.bet
	hand = str(player.hand)

	return f"{name}[{cash}][{bett}] {hand}"

Player.__repr__ = playerRepr
Players = List[Player]
PokerTable = Tuple[Players, Deck]

class Hands:
	__cache = {}

	@staticmethod
	def __cached(deck:Deck):
		return str(deck) in Hands.__cache

	@staticmethod
	def __from_cache(deck:Deck):
		return Hands.__cache[str(deck)]

	@staticmethod
	def __into_cache(deck:Deck, value):
		# Since most of the time we need the key stored for the current game
		# and there is a limited number of What/BestHand calls we can assume
		# that the hands for this game are less than 20, so in order to not keep
		# hands stored in previous game we reset the cache from time to time
		# the threshold is arbitrary
		if len(Hands.__cache) >= 4096:
			Hands.__cache.clear()
		Hands.__cache[str(deck)] = value

	@staticmethod
	def InOrder():
		return [Hands.Noth, Hands.Pair, Hands.Pairs,
			Hands.Three, Hands.Straight, Hands.Flush, \
			Hands.Full, Hands.Four, Hands.StraightFlush, \
			Hands.RoyalFlush]

	@staticmethod
	def Powr(stat:str) -> int:
		return [h.__name__ for h in Hands.InOrder()].index(stat)

	@staticmethod
	def BestHand(deck:Deck) -> Tuple[str, Deck]:
		if Hands.__cached(deck):
			return Hands.__from_cache(deck)

		deck = Deck(deck)
		combs = Hands.InOrder()
		for comb in combs[::-1]:
			hand = comb(deck)
			if hand:
				Hands.__into_cache(deck, (comb.__name__, hand))
				break

		return Hands.__from_cache(deck)

	@staticmethod
	def Noth(deck:Deck) -> Deck:
		freq = deck.Freq()
		for s in freq:
			if s in ERANKS.ALL and freq[s] > 1:
				return []
		return deck.TopN(5, set())

	@staticmethod
	def Pair(deck:Deck) -> Deck:
		freq = deck.Freq()
		for s in freq:
			if s in ERANKS.ALL and freq[s] == 2:
				two = deck.Only(ofRank = s)
				return two + deck.TopN(3, set(two))
		return []

	@staticmethod
	def Pairs(deck:Deck) -> Deck:
		freq = deck.Freq()
		pairs = 0
		hand = Deck([])
		for s in freq:
			if s in ERANKS.ALL and freq[s] == 2:
				pairs += 1
				hand += deck.Only(ofRank = s)
			if pairs == 2:
				return hand.Sort() + deck.TopN(1, set(hand))
		return []

	@staticmethod
	def Three(deck:Deck) -> Deck:
		freq = deck.Freq()
		pairs = 0
		for s in freq:
			if s in ERANKS.ALL and freq[s] == 3:
				three = deck.Only(ofRank = s)
				topTw = deck.TopN(2, set(three))
				return three + topTw
		return []

	@staticmethod
	def Straight(deck:Deck) -> Deck:
		one_hot = np.zeros(len(ERANKS.ALL) + 1) #one hot encoding of the hand
		for card in deck:
			for i in ERANKS.asIndex(card[1]):
				one_hot[i] = 1
		for i in range(len(ERANKS.ALL) - 1, -1, -1):
			one_hot[i] += one_hot[i + 1] if one_hot[i] > 0 else 0
			if one_hot[i] >= 5:
				break
		else:
			return []
		hand = []
		for j in range(i, i + 5):
			hand.extend(deck.ACard(ofRank = ERANKS.fromIdx(j)))
		return Deck(hand[::-1])

	@staticmethod
	def Flush(deck:Deck) -> Deck:
		freq = deck.Freq()
		pairs = 0
		for s in freq:
			if s in ESUITS.ALL and freq[s] == 5:
				return deck.Only(ofSuit = s).Sort()
		return []

	@staticmethod
	def Full(deck:Deck) -> Deck:
		freq = deck.Freq()
		pair, three = False, False
		rank2, rank3 = "A", "A"
		for s in freq:
			if s in ERANKS.ALL:
				if freq[s] == 2:
					pair = True
					rank2 = s
				elif freq[s] == 3:
					three = True
					rank3 = s
		if not (three and pair):
			return []
		return deck.Only(ofRank = rank3) + deck.Only(ofRank = rank2)

	@staticmethod
	def Four(deck:Deck) -> Deck:
		freq = deck.Freq()
		rank = deck[0]
		for s in freq:
			if s in ERANKS.ALL and freq[s] == 4:
				four = deck.Only(ofRank = s)
				last = deck.TopN(1, set(four))
				return four + last
		return []

	@staticmethod
	def StraightFlush(deck:Deck, last:str=None) -> Deck:
		mostFreqSuit = deck.MostFreq(what="suit")
		sameSuitCrds = deck.Only(ofSuit=mostFreqSuit)
		if len(sameSuitCrds) < 5:
			return []
		return Hands.Straight(sameSuitCrds)

	@staticmethod
	def RoyalFlush(deck:Deck) -> Deck:
		hand = Hands.StraightFlush(deck)
		if hand and hand[0].rank == 'A':
			return hand
		return []
