from setting import Setting

class Game_stats():
	def __init__(self,ai_setting):
		self.ai_setting = ai_setting
		self.game_active = False
		self.reset_stats()

		self.fileName = "datasource/high_score.txt"

		self.high_score = 0

		self.read_high_score()


	def reset_stats(self):

		self.ships_left = self.ai_setting.ship_limit
		self.score = 0
		self.level = 1

	def read_high_score(self):

		old_score = 0
		try :
			with open(self.fileName) as file_object:

				content = file_object.read()

				old_score = int(content)

		except FileNotFoundError:
			pass
		self.high_score = old_score

	def write_high_score(self):

		with open(self.fileName,'w') as file_object:
			file_object.write(str(self.high_score))