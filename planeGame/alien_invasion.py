
import sys

import pygame

from pygame.sprite import Group

import game_functions as gf

from setting import Setting
from alien import Alien
from game_stats import Game_stats
from play_button import Play_button
from scoreboard import Scoreboard
from ship import Ship




def run_game():

	pygame.init()

	pygame.display.set_caption("Alien Invasion")

	ai_setting = Setting()

	screen =  pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height))

	stats = Game_stats(ai_setting)

	play_button = Play_button(ai_setting,screen,"Play")

	sb = Scoreboard(ai_setting,screen,stats)

	ship = Ship(screen,ai_setting)

	aliens = Group()
	bullets = Group()

	gf.creat_fleet(ai_setting,screen,aliens,ship)

	while True:
		
		gf.check_events(ai_setting,screen,ship,bullets,play_button,aliens,stats,sb)

		if stats.game_active:

			ship.update()

			bullets.update()

			gf.update_bullets(bullets,aliens,ai_setting,screen,ship,sb,stats)

			gf.update_aliens(ai_setting,aliens,ship,stats,screen,bullets,sb)
		
		gf.update_screen(ai_setting,screen,ship,bullets,aliens,play_button,sb,stats)
		

run_game()