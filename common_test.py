from common import *

class HandsChecker:
	@staticmethod
	def testRoyal():
		hand = [("♠", "10"), ("♠", "K")]
		deck = [("♠", "A"), ("♠", "J"), ("♠", "Q"), ("♠", "3"), ("♠", "2")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.RoyalFlush(hand + deck)

		hand = [("♠", "10"), ("♠", "K")]
		deck = [("♢", "A"), ("♠", "J"), ("♢", "6"), ("♢", "3"), ("♢", "2")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.RoyalFlush(hand + deck)

	@staticmethod
	def testStraightFlush():
		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♠", "3"), ("♠", "J"), ("♠", "Q"), ("♠", "4"), ("♠", "9")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.StraightFlush(hand + deck)

		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♠", "3"), ("♣", "J"), ("♠", "Q"), ("♠", "4"), ("♠", "9")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.StraightFlush(hand + deck)

	@staticmethod
	def testFour():
		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "8"), ("♠", "9")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Four(hand + deck)

		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "8"), ("♠", "8")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Four(hand + deck)

		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "6"), ("♠", "3")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Four(hand + deck)

	@staticmethod
	def testFull():
		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "10"), ("♠", "9")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Full(hand + deck)

		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "8"), ("♠", "8")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Full(hand + deck)

		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♡", "8"), ("♢", "10"), ("♢", "8"), ("♣", "8"), ("♠", "3")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Full(hand + deck)

	@staticmethod
	def testFlush():
		hand = [("♠", "10"), ("♠", "8")]
		deck = [("♠", "2"), ("♠", "J"), ("♢", "8"), ("♣", "7"), ("♠", "9")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Flush(hand + deck)

		hand = [("♠", "10"), ("♢", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "8"), ("♢", "8")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Flush(hand + deck)

	@staticmethod
	def testStraight():
		hand = [("♠", "A"), ("♢", "10")]
		deck = [("♢", "2"), ("♠", "J"), ("♢", "A"), ("♣", "K"), ("♠", "Q")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Straight(hand + deck)

		hand = [("♠", "A"), ("♢", "8")]
		deck = [("♢", "2"), ("♠", "3"), ("♢", "A"), ("♣", "5"), ("♠", "4")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Straight(hand + deck)

		hand = [("♠", "10"), ("♢", "8")]
		deck = [("♡", "8"), ("♠", "J"), ("♢", "8"), ("♣", "8"), ("♢", "8")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Straight(hand + deck)

	@staticmethod
	def testThree():
		hand = [("♠", "A"), ("♢", "10")]
		deck = [("♢", "5"), ("♠", "J"), ("♢", "A"), ("♣", "A"), ("♠", "Q")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Three(hand + deck)

		hand = [("♠", "A"), ("♢", "8")]
		deck = [("♢", "2"), ("♠", "3"), ("♢", "A"), ("♣", "5"), ("♠", "4")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Three(hand + deck)

	@staticmethod
	def testPairs():
		hand = [("♠", "A"), ("♢", "10")]
		deck = [("♢", "5"), ("♠", "5"), ("♢", "A"), ("♣", "10"), ("♠", "Q")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Pairs(hand + deck)

		hand = [("♠", "A"), ("♢", "10")]
		deck = [("♢", "5"), ("♠", "5"), ("♢", "A"), ("♣", "9"), ("♠", "Q")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Pairs(hand + deck)

		hand = [("♠", "A"), ("♢", "8")]
		deck = [("♢", "2"), ("♠", "3"), ("♢", "A"), ("♣", "5"), ("♠", "4")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Pairs(hand + deck)

	@staticmethod
	def testPair():
		hand = [("♠", "A"), ("♢", "8")]
		deck = [("♢", "2"), ("♠", "3"), ("♢", "A"), ("♣", "5"), ("♠", "4")]
		hand, deck = Deck(hand), Deck(deck)
		assert Hands.Pair(hand + deck)

		hand = [("♠", "A"), ("♢", "10")]
		deck = [("♢", "5"), ("♠", "5"), ("♢", "3"), ("♣", "9"), ("♡", "Q")]
		hand, deck = Deck(hand), Deck(deck)
		assert not Hands.Pairs(hand + deck)

	#[("♠","J"), ("♡", "Q"), ("♢", "K"), ("♣", "A")]
	@staticmethod
	def runAll():
		HandsChecker.testRoyal()
		HandsChecker.testStraightFlush()
		HandsChecker.testFour()
		HandsChecker.testFull()
		HandsChecker.testFlush()
		HandsChecker.testStraight()
		HandsChecker.testThree()
		HandsChecker.testPairs()
		HandsChecker.testPair()


class ScenarioCompare:
	@staticmethod
	def run():
		h0 = "|♣ A|♢ A|♠ 8|♢ 6|♢ 5|".split("|")[1:-1]
		h1 = "|♣ 5|♢ 5|♢ J|♠ 8|♢ 6|".split("|")[1:-1]
		h2 = "|♣10|♢10|♡ 9|♠ 8|♢ 5|".split("|")[1:-1]
		h3 = "|♢ 8|♠ 8|♡ 7|♢ 6|♢ 5|".split("|")[1:-1]
		raw = [h0, h1, h2, h3]

		hands = [Deck([(c[:1], c[1:].strip()) for c in h]) for h in raw]
		targets = [hands[0], hands[2], hands[3], hands[1]][::-1]

		hands = sorted(hands)

		for i, hand in enumerate(hands):
			assert targets[i] == hand

	@staticmethod
	def run2():
		h0 = "|♢10|♠10|♠ A|♣ K|♢ J|".split("|")[1:-1]
		h1 = "|♣10|♠10|♠ A|♣ K|♠ J|".split("|")[1:-1]
		h2 = "|♠ 6|♢ 6|♠ A|♣ K|♠ Q|".split("|")[1:-1]
		h3 = "|♢ A|♠ A|♣ K|♠10|♣ 2|".split("|")[1:-1]
		raw = [h0, h1, h2, h3]

		hands = [Deck([(c[:1], c[1:].strip()) for c in h]) for h in raw]
		targets = [hands[3], hands[0], hands[1], hands[2]][::-1]

		hands = sorted(hands)

		for i, hand in enumerate(hands):
			assert targets[i] == hand


	@staticmethod
	def run3():
		h0 = "|♠ 7|♡ 6|♢ 5|♡ 4|♡ 3|".split("|")[1:-1]
		h1 = "|♢10|♢ 9|♡ 8|♠ 7|♡ 6|".split("|")[1:-1]
		h2 = "|♠ 7|♡ 6|♢ 5|♡ 4|♠ 3|".split("|")[1:-1]
		h3 = "|♠ 7|♡ 6|♢ 5|♡ 4|♢ 3|".split("|")[1:-1]
		raw = [h0, h1, h2, h3]

		hands = [Deck([(c[:1], c[1:].strip()) for c in h]) for h in raw]
		targets = [hands[1], hands[0], hands[2], hands[3]][::-1]

		hands = sorted(hands)

		for i, hand in enumerate(hands):
			assert targets[i] == hand

	@staticmethod
	def run4():
		h0 = "|♠ Q|♠ 8|♠ 5|♠ 4|♠ 3|".split("|")[1:-1]
		h1 = "|♣ 8|♠ 8|♡ 8|♢ Q|♠ Q|".split("|")[1:-1]
		h2 = "|♠ 8|♡ 8|♢ K|♣ 5|♣ 2|".split("|")[1:-1]
		h3 = "|♠ 8|♡ 8|♢ K|♣ J|♢ 2|".split("|")[1:-1]
		h4 = "|♠ 8|♡ 8|♡ A|♢ K|♡ 6|".split("|")[1:-1]
		h5 = "|♠ 8|♡ 8|♣ 3|♠ 3|♣ 6|".split("|")[1:-1]

		raw = [h0, h1, h2, h3, h4, h5]

		hands = [Deck([(c[:1], c[1:].strip()) for c in h]) for h in raw]
		targets = [hands[2], hands[3], hands[4], hands[5], \
					hands[0], hands[1]]#[::-1]

		hands = sorted(hands)
		for i, hand in enumerate(hands):
			assert targets[i] == hand

	@staticmethod
	def runAll():
		ScenarioCompare.run()
		ScenarioCompare.run2()
		ScenarioCompare.run3()
		ScenarioCompare.run4()

# To start other tests
class Scenario:
	@staticmethod
	def run():
		#import pdb; pdb.set_trace()
		#[("♠","J"), ("♡", "Q"), ("♢", "K"), ("♣", "A")]

		players = [
			Player(name="Dan", cash=1000.0, hand=[("♡", "5"), ("♣", "9")], bet=0, playing=True),
			Player(name="Alex", cash=1000.0, hand=[("♡", "K"), ("♣", "7")], bet=0, playing=True),
			Player(name="Vera", cash=1000.0, hand=[("♡", "8"), ("♣", "J")], bet=0, playing=True),
			Player(name="Alin", cash=1000.0, hand=[("♡", "2"), ("♠", "9")], bet=0, playing=True),
			Player(name="George", cash=1000.0, hand=[("♢", "K"), ("♠", "3")], bet=0, playing=True),
			Player(name="Cosmin", cash=1000.0, hand=[("♡", "4"), ("♣", "A")], bet=0, playing=True),
		]
		deck = [("♡", "3"), ("♡", "3"),("♡", "A"), ("♣", "Q"),\
				("♡", "3"), ("♠", "6"),("♡", "3"), ("♣", "10")]
		play_once(deck, players, ALL, FLOP | TURN | RIVER)


if __name__ == "__main__":
	HandsChecker.runAll()
	ScenarioCompare.runAll()
