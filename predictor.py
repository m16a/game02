from vector import Vector
from model.Unit import Unit

class Predictor:
	def __init__(self, top, left, right, bot):
		self.top_side_col = top
		self.left_side_col = left
		self.right_side_col = right
		self.bot_side_col = bot


	def predict_unit_move(self, unit, segment):
		#	p + t * r = q + u * s
		#	t [0, +inf)
		#	u [0, 1]  

		p = Vector(unit.x, unit.y)
		r = Vector(unit.speed_x, unit.speed_y)
		q = Vector(segment.start.x, segment.start.y)
		s = Vector(segment.end.x - segment.start.x, segment.end.y - segment.start.y)

		# x - cross point
        # r - dirrection
        # symetry reflect r respect to s vector
