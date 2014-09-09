from math import *
from model.ActionType import ActionType
from model.HockeyistType import HockeyistType


class Coach:
	def __init__(self):
		self.a = None

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

		if (closest_id == me.id):
			return True
		else:
			return False

coach = Coach()

class MyStrategy:
	def move(self, me, world, game, move):
		if (world.puck.owner_player_id != me.player_id):
			if (coach.need_I_take_puck(me, world)):
				move.speed_up = 1.0
				angle = me.get_angle_to_unit(world.puck)

				if (angle < pi):
					move.turn = angle
				else:
					move.turn = -(2*pi - angle)
				move.action = ActionType.TAKE_PUCK
		else:
			move.action = ActionType.PASS
			move.pass_power = 1.0
			move.pass_angle = pi / 4.0
