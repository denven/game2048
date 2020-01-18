# -*- coding: utf-8 -*-

import pygame, sys, os, time
from pygame.locals import *

import cls2048

SCORE_CLR  = (255,0,0)
GNAME_CLR  = (0,0,255)
BACKGRD_CLR  = (255,190,100)

NUMBER_064_CLR = (0,0,0)
NUMBER_128_CLR = (128,0,0)
NUMBER_256_CLR = (128,128,0)
NUMBER_512_CLR = (255,128,0)
NUMBER_1024_CLR = (255,255,0)
NUMBER_2048_CLR = (255,0,0)


def show_gamestatus(game_alive, game_score):
	font=pygame.font.SysFont("Lato", 30, bold=True)
	screen.blit(font.render("Game 2048", True, GNAME_CLR), (175,10))  #game name

	font=pygame.font.SysFont("Lato", 12, bold=True)
	screen.blit(font.render("Reset: F2", True, GNAME_CLR), (50,15))  #game instruction
	screen.blit(font.render("Exit: Esc", True, GNAME_CLR), (50,35))  #game instruction
	font=pygame.font.SysFont("Lato", 12, bold=True)
	screen.blit(font.render("Move: ← ↑ ↓ →", True, GNAME_CLR), (365,20)) #game instruction

	#game score
	if not game_alive:
		font=pygame.font.SysFont("Lato", 28, bold=True)
		screen.blit(font.render("Game Over!!!", True, SCORE_CLR), (48, 50))
	else:
		font=pygame.font.SysFont("Lato", 15, bold=True)
		screen.blit(font.render("You have scored: "+str(game_score), True, SCORE_CLR), (50, 60))

def print_passedtime(start_time):
	secondspassed=int(time.clock()-start_time)
	hours=secondspassed//3600
	minutes=(secondspassed%3600)//60
	seconds=(secondspassed%3600)%60
	time_text="Time: "+"{0:0=2}:{1:0=2}:{2:0=2}".format(hours,minutes,seconds)

	font=pygame.font.SysFont("Calibri", 22)
	screen.fill(BACKGRD_CLR,[320,50,150,30],0)
	screen.blit(font.render(time_text, True, SCORE_CLR), (350, 60))

'''create background'''
def show_background():
	pygame.draw.rect(screen, BACKGRD_CLR, [0,0,500,500], 0)  #no border
	screen.blit(screen, (0,0))


def draw_gamepanel(row_col_num):
	for x in range(0,row_col_num):
		for y in range(0,row_col_num):
			start_x=50+100*x
			start_y=80+100*y
			width=100
			height=100
			pygame.draw.rect(screen, (128,128,128), [start_x,start_y,width,height], 2)


def show_gamedata(listdata):
	font=pygame.font.SysFont("Calibri", 40, bold=True)
	draw_gamepanel(len(listdata))
	for x in range(0,len(listdata)):
		for y in range(0,len(listdata)):
			gamedata_text=str(listdata[x][y])
			width,height = font.size(gamedata_text)
			start_x=50+(100-width)//2+100*x
			start_y=85+(100-height)//2+100*y
			if listdata[x][y]==0:
				pass
			elif listdata[x][y]<=64:
				screen.blit(font.render(gamedata_text, True, NUMBER_064_CLR), (start_x,start_y))
			elif listdata[x][y]==128:
				screen.blit(font.render(gamedata_text, True, NUMBER_128_CLR), (start_x,start_y))
			elif listdata[x][y]==256:
				screen.blit(font.render(gamedata_text, True, NUMBER_256_CLR), (start_x,start_y))
			elif listdata[x][y]==512:
				screen.blit(font.render(gamedata_text, True, NUMBER_512_CLR), (start_x,start_y))
			elif listdata[x][y]==1024:
				screen.blit(font.render(gamedata_text, True, NUMBER_1024_CLR), (start_x,start_y))
			elif listdata[x][y]>=2048:
				screen.blit(font.render(gamedata_text, True, NUMBER_2048_CLR), (start_x,start_y))

pygame.init()

screen=pygame.display.set_mode((500,500))
pygame.display.set_caption("2048")

show_background()

game_instance=cls2048.game2048(4)
game_instance.fill_onegrid()

start_time=time.clock()
show_gamedata(game_instance.grid_data)  #initial status
show_gamestatus(game_instance.alive, game_instance.score)
#print_passedtime(start_time)

pygame.display.update()

while True:
	print_passedtime(start_time)

	press_flag = False
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			press_flag = True
		elif event.type == KEYUP:
			press_flag = False

	if press_flag:
		key_pressed = pygame.key.get_pressed()
		move_flag = False
		#if event.key>=273 and event.key<=276:
		if key_pressed[K_ESCAPE]:
			pygame.quit()
			sys.exit()  #call these two function together

		if key_pressed[K_F2]:
			start_time=time.clock()
			game_instance.reset_game()

		if key_pressed[K_UP]:
			move_flag = game_instance.move_left()

		elif key_pressed[K_DOWN]:
			move_flag = game_instance.move_right()

		elif key_pressed[K_RIGHT]:
			move_flag = game_instance.move_down()

		elif key_pressed[K_LEFT]:
			move_flag = game_instance.move_up()

		if move_flag or key_pressed[K_F2]:
			screen.fill((0,0,0))
			show_background()
			game_instance.fill_onegrid()
			show_gamedata(game_instance.grid_data)
			if move_flag:
				game_instance.get_status()
			show_gamestatus(game_instance.alive, game_instance.score)

	pygame.display.update()
