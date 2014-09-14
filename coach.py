from model.HockeyistType import HockeyistType
import itertools

class TacticType:
	START   = "start"
	OFFENCE = "offence"
	DEFENCE = "defence"
	TIMEOUT = "timeout" 

class DefenceStrategy:
	PERSONAL = "personal"

class Coach:
	def __init__(self):
		self.a = None

	def getStrategy(self,world):
		my_h = [x for x in world.hockeyists if x.teammate and x.type != HockeyistType.GOALIE]
		enemys = [x for x in world.hockeyists if not x.teammate and x.type != HockeyistType.GOALIE]

		if len(my_h) != len(enemys): 
			raise ValueError("bad teams size {0} - {1}".format(len(my_h), len(enemys)))

		enemy_permutation = list(itertools.permutations(enemys))

		# best = min(enemy_permutation, key = lambda x: for i in x )
		min_d = 100000
		best = None
		for e in enemy_permutation:
			d = 0
			for i in range(0, len(enemys)):
				d = d + my_h[i].get_distance_to_unit(e[i])
			if d < min_d:
				best = e
				min_d = d

		if best == None:
			raise ValueError("personal defense computation failed bad best")

		if len(best) != len(my_h):
			raise ValueError("personal defense computation failed bad size {0} - {1}".format(len(my_h), len(best)))

		sheme = []

		for i in range(0, len(enemys)):
			sheme.append((my_h[i].id , best[i].id))

		return (DefenceStrategy.PERSONAL, sheme, None)

	def need_I_take_puck(self, me, world):
		closest_id = -1
		min_dist = 1000

		for h in world.hockeyists:
			if not h.teammate or h.type == HockeyistType.GOALIE:
				continue
			d = h.get_distance_to_unit(world.puck)
			if (d <= min_dist):
				min_dist = d
				closest_id = h.id

		return closest_id == me.id

	def isAttack(self, world):
		return world.puck.owner_player_id == world.get_my_player().id and True #controlled pass must be here
