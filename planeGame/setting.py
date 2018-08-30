class Setting():

	def __init__(self):

		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230.,230.,230.)

		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60.,60.,60.)
		
		self.fire_bullte = False # not use
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		# ship move speed
		self.ship_speed_factor = 6
		# ship limit 
		self.ship_limit = 3

		# bullet move speed
		self.bullet_speed_factor = 6
		#bullet allowed
		self.bullet_allowed = 300

		# alien move speed
		self.alien_speed_factor = 3
		# alien drop speed
		self.fleet_drop_speed = 10
		# shit one alien ,get score
		self.alien_points = 50


		# alien move direction,1 -> right ,-1 -> left
		self.fleet_direction = 1
		# speed up scale
		self.speedup_scale = 1.1

	def increase_speed(self):

		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.speedup_scale)