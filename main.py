from collections import defaultdict, OrderedDict
from pprint import pprint
from tqdm import tqdm

import random
import sys
import itertools

from table import Table, Options

from common import *
from typing import *

def play_once(deck:Deck, players:Players, show:int = ALL, stgs:int = ALL) -> Dict[str, int]:
	stats = defaultdict(lambda:0)
	for player in players:
		stats[Hands.BestHand(player.hand + table)[0]] += 1
	return stats


def probabilify(stats:Dict[str, int]) -> Dict[str, float]:
	totl = sum(stats.values())
	for k in stats:
		stats[k] /= totl
	sortd = sorted(stats.items(), key=lambda kv: kv[1], reverse=True)
	stats = OrderedDict(sortd)
	return stats

def my_pprint(d):
	nl = 15
	vl = 6
	vl2 = vl // 2

	for key in d:
		val = d[key]
		print(f"%{nl}s: %{vl2}.{vl2}f%%" % (key, val * 100))

if __name__ == "__main__":
	DELTA = 10000
	names = sorted(['Alex', 'Vera', 'George', 'Alin', 'Dan', 'Cosmin'], key=len)
	players = [Player(name=name, cash=1000, hand=[], bet=0, playing=True) \
				for name in names]
	stats = defaultdict(lambda:0)

	confg = Options(seats=10, stages=ALL, show=RIVER, logger=print)
	table = Table(confg=confg)
	for player in players:
		table.join(player)

	#for i in tqdm(range(1)):
	for i in range(1):
		table.play()
		if i % DELTA == DELTA - 1:
			print()

	"""
	for i in tqdm(range(1)):
		stat = play_once(deck, players, ALL)
			for key, value in stat.items():
				stats[key] += value

		if i % DELTA == DELTA - 1:
			print()
			my_pprint(probabilify(stats))
	print()
	my_pprint(probabilify(stats))
	"""
