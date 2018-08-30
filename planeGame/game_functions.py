import sys

import pygame

from bullet import Bullet

from alien import Alien

from game_stats import Game_stats

from time import sleep

from ship import Ship

def fire_bullet(ai_setting,screen,ship,bullets):
	if len(bullets) < ai_setting.bullet_allowed:
		new_buulte = Bullet(ai_setting,screen,ship)
		bullets.add(new_buulte)

def check_down_events(event,ai_setting,screen,ship,bullets):

	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_setting,screen,ship,bullets)
		# ai_setting.fire_bullte = True
	elif event.key == pygame.K_q:
		sys.exit()

def check_up_events(event,ship,ai_setting):

	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_SPACE:		
		ai_setting.fire_bullte = False


def check_events(ai_setting,screen,ship,bullets,play_button,aliens,stats,sb):

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_down_events(event,ai_setting,screen,ship,bullets)
			elif event.type == pygame.KEYUP:
				check_up_events(event,ship,ai_setting)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_setting,screen,stats,play_button,mouse_x,mouse_y,aliens,bullets,ship,sb)

def check_play_button(ai_setting,screen,stats,play_button,mouse_x,mouse_y,aliens,bullets,ship,sb):

	button_click = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_click and not stats.game_active:

		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True

		aliens.empty()
		bullets.empty()

		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		creat_fleet(ai_setting, screen, aliens, ship)
		ship.center_ship()

def check_bullet_alien_collide(bullets,aliens,ai_setting,screen,ship,sb,stats):

	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

	if collisions:
		for alines in collisions.values():
			stats.score += ai_setting.alien_points * len(alines)
			sb.prep_score()

	check_high_score(stats, sb)

	if len(aliens) == 0:
		stats.level += 1
		sb.prep_level()
		bullets.empty()
		ai_setting.increase_speed()
		creat_fleet(ai_setting,screen,aliens,ship)
def update_bullets(bullets,aliens,ai_setting,screen,ship,sb,stats):
	for bullet in bullets.copy():
			if bullet.rect.bottom <= 0 :
				bullets.remove(bullet)

	check_bullet_alien_collide(bullets,aliens,ai_setting,screen,ship,sb,stats)

def update_screen(ai_setting, screen , ship,bullets,aliens,play_button,sb,stats):

	screen.fill(ai_setting.bg_color)

	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()

	aliens.draw(screen)

	sb.show_score()

	if not stats.game_active:
		play_button.draw_button()

	pygame.display.flip()



def creat_fleet(ai_setting,screen,aliens,ship):

	alien = Alien(ai_setting,screen)
	alien_width = alien.rect.width
	
	numer_aliens_x = number_aliens(ai_setting,alien_width)
	numer_aliens_row = numer_rows(ai_setting, ship.rect.height, alien.rect.height)

	for row_number in range(numer_aliens_row):
		for aline_number in range(numer_aliens_x):
			creat_alien(ai_setting, screen, aliens, aline_number,row_number)

def number_aliens(ai_setting,alien_width):
	# 可用空间，总宽度 - 两边的空隙（两边的空隙为 外星人的宽度）
	available_space_x = ai_setting.screen_width - 2 * alien_width
	# 外星人个数 
	numer_aliens_x = int(available_space_x/(2*alien_width))

	return numer_aliens_x

def numer_rows(ai_setting,ship_height,alien_height):
	available_space_y = ai_setting.screen_height - 3 * alien_height - ship_height
	numer_rows = int(available_space_y/(2 * alien_height))
	return numer_rows

def creat_alien(ai_setting,screen,aliens,alien_number,row_number):

	alien = Alien(ai_setting,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)

def change_fleet_direction(ai_setting,aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_setting.fleet_drop_speed
	ai_setting.fleet_direction *= -1

def check_fleet_edges(ai_setting,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_setting,aliens)
			break

def ship_hit(ai_setting,stats,screen,ship,aliens,bullets,sb):

	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
		aliens.empty()
		bullets.empty()

		creat_fleet(ai_setting, screen, aliens, ship)

		ship.center_ship()

		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting,stats,screen,ship,aliens,bullets,sb):

	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_setting, stats, screen, ship, aliens, bullets,sb)
			break

def update_aliens(ai_setting,aliens,ship,stats,screen,bullets,sb):

	check_aliens_bottom(ai_setting,stats,screen,ship,aliens,bullets,sb)

	check_fleet_edges(ai_setting,aliens)
	aliens.update()

	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_setting, stats, screen, ship, aliens, bullets,sb)
		sleep(0.5)

def fire(ai_setting,screen,ship,bullets):

	if ai_setting.fire_bullte:
		fire_bullet(ai_setting,screen,ship,bullets)

def check_high_score(stats,sb):

	if stats.score > stats.high_score:
		stats.high_score = stats.score
		stats.write_high_score()
		sb.prep_high_score()





