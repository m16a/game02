from math import *
from model.ActionType import ActionType
from model.HockeyistType import HockeyistType
from fsm import FSM
from coach import *

import vector




#Segment(Vector(), Vector())

coach = None
predictor = None

initedOnce = False
def initSystems():
	if initedOnce:
		return

	global coach = Coach()
	global predictor = Predictor()

	
	global initedOnce = True




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
	def moveToPoint(self,me,x,y,move):
		dist = me.get_distance_to(x,y)

		angle = me.get_angle_to(x,y)
		k = 1
		if (angle < pi/2 and angle > -pi/2) or dist > 150:
			move.turn = angle
		else:
			k = -1
			move.turn = -angle

		move.speed_up = (1.0 if dist > 75 else  dist / 75.0) * k


	def getHockeyistByID(self, world,id):
		return [x for x in world.hockeyists if x.id == id][0]

	def canStrikeUnit(self, me, unit):
		return me.get_distance_to_unit(unit) <= 120 and abs(me.get_angle_to_unit(unit)) <= pi / 12.0

	#sheme [(my_id1, target_id1),...]
	def defend(self, def_type, sheme, value, me, world, game, move):
		if def_type == DefenceStrategy.PERSONAL:
			target_id = [x[1] for x in sheme if x[0] == me.id][0]

			u = self.getHockeyistByID(world, target_id)
			
			my_player = world.get_my_player()

			net_X = my_player.net_front
			net_Y = 0.5 * (my_player.net_top + my_player.net_bottom)

			koef = 0.9
			dist_X = (koef * u.x + (1 - koef) * net_X)
			dist_Y = (koef * u.y + (1 - koef) * net_Y)	
			# self.moveToPoint(me, u.x, u.y, move)
			
			self.moveToPoint(me, dist_X, dist_Y, move)
			
			if world.puck.owner_hockeyist_id == target_id:
				if (self.canStrikeUnit(me, world.puck) or self.canStrikeUnit(me, u)):
					move.action = ActionType.STRIKE
				else:
					move.action = ActionType.TAKE_PUCK
			else:
				move.action = ActionType.TAKE_PUCK

		return move

	def move(self, me, world, game, move):

		fsm.event(world)
		#print fsm.currentState

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

			enemy = world.get_opponent_player()

			net_X = enemy.net_front
			net_Y = 0.5 * (enemy.net_top + enemy.net_bottom)

			a = me.get_angle_to(net_X, net_Y)
			move.turn = a
			if (abs(a) < pi / 180.0):
				move.action = ActionType.STRIKE
			