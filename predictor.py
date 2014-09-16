from vector import Vector


class Predictor:
	def __init__(self, top, left, right, bot):
		self.top_side_col = top
		self.left_side_col = left
		self.right_side_col = right
		self.bot_side_col = bot