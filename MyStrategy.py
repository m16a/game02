from math import *
from model.ActionType import ActionType
from model.HockeyistType import HockeyistType
from fsm import FSM
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

		enemy_permutation = list(itertools.permutations(enemys))

		# best = min(enemy_permutation, key = lambda x: for i in x )
		min_d = 1000
		best = None
		for e in enemy_permutation:
			d = 0
			for i in range(0, len(enemys)):
				d = d + my_h[i].get_distance_to_unit(e[i])

			if d < min_d:
				best = e
				min_d = d

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

coach = Coach()

fsm = FSM([(TacticType.START,   TacticType.OFFENCE, lambda x: Coach().isAttack(x)),
	       (TacticType.START,   TacticType.DEFENCE, lambda x: not Coach().isAttack(x)),
	       (TacticType.OFFENCE, TacticType.DEFENCE, lambda x: not Coach().isAttack(x)),
	       (TacticType.DEFENCE, TacticType.OFFENCE, lambda x: Coach().isAttack(x)),
	       (TacticType.DEFENCE, TacticType.DEFENCE, lambda x: not Coach().isAttack(x)),
	       (TacticType.OFFENCE, TacticType.OFFENCE, lambda x: Coach().isAttack(x)),
	       ])

fsm.start(TacticType.START)

#----------------------------------------------------------

class MyStrategy:

	def getHockeyistByID(self, world,id):
		return [x for x in world.hockeyists if x.id == id][0]

	#sheme [(my_id1, target_id1),...]
	def defend(self, def_type, sheme, value, me, world, game, move):
		print sheme
		if def_type == DefenceStrategy.PERSONAL:
			target_id = [x[1] for x in sheme if x[0] == me.id][0]

			move.speed_up = 1.0
			angle = me.get_angle_to_unit(self.getHockeyistByID(world, target_id))

			if (angle < pi):
				move.turn = angle
			else:
				move.turn = -(2*pi - angle)
			move.action = ActionType.TAKE_PUCK

		return move

	def move(self, me, world, game, move):

		fsm.event(world)
		print fsm.currentState

		if (fsm.currentState == TacticType.DEFENCE):
			# if (coach.need_I_take_puck(me, world)):
			# 	move.speed_up = 1.0
			# 	angle = me.get_angle_to_unit(world.puck)

			# 	if (angle < pi):
			# 		move.turn = angle
			# 	else:
			# 		move.turn = -(2*pi - angle)
			# 	move.action = ActionType.TAKE_PUCK
			strata = coach.getStrategy(world)
			self.defend(strata[0], strata[1], None, me, world, game, move)
		else:
			move.action = ActionType.PASS
			move.pass_power = 1.0
			move.pass_angle = pi / 4.0