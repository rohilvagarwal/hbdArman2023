import asyncio

from ProjectConstants import *
import sys
from Button import Button
from ChipperInvaders import ChipperInvaders
import time

#pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#image imports
d4 = pygame.image.load('images/d4Logo.svg').convert_alpha()
scaled_d4 = pygame.transform.scale(d4, (50, 50)).convert_alpha()

#game variables
chipperInvaders = ChipperInvaders(100, SCREEN_HEIGHT / 2, 500, 200)

#game states: menu, kinematics, circularMotion, aboutMe
gameState = "menu"

#background sound
mixer.music.load("sounds/trollion.mp3")
mixer.music.play(-1)


def return_to_menu_button():
	global gameState

	menuButton = Button(centerX=SCREEN_WIDTH - 75, centerY=50, width=100, height=50, textSize=30, borderSize=10, text="Menu")

	if menuButton.draw_and_check_click(screen):
		gameState = "menu"


def draw_d4():
	screen.blit(scaled_d4, (0, 10))


def draw_menu():
	global gameState
	#global GAME_OVER
	screen.fill(backgroundColor)
	draw_d4()

	#draw title
	draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10, 70, "Arman Gaming")

	chippers = Button(centerX=SCREEN_WIDTH / 2, centerY=SCREEN_HEIGHT / 2, width=350, height=100, textSize=70, borderSize=30, text="Start Boi")
	#exit = Button(centerX=SCREEN_WIDTH / 2, centerY=SCREEN_HEIGHT - 30, width=100, height=40, textSize=25, borderSize=10, text="Exit")

	#draw button and check if clicked
	if chippers.draw_and_check_click(screen):
		gameState = "Chipper Invaders"


# if exit.draw_and_check_click(screen):
# 	GAME_OVER = True


def draw_chipper_invaders():
	screen.fill(backgroundColor)
	draw_d4()
	return_to_menu_button()

	chipperInvaders.draw_static(screen)


async def main():
	#game start
	GAME_OVER = False
	draw_menu()
	pygame.display.update()

	frame_count = 0
	frame_rate = 0
	start_time = time.time()

	while not GAME_OVER:
		if gameState == "menu":
			draw_menu()
		if gameState == "Chipper Invaders":
			draw_chipper_invaders()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GAME_OVER = True

		frame_count += 1
		if time.time() - start_time > 1:
			frame_rate = frame_count
			frame_count = 0
			start_time = time.time()

		draw_text_left(screen, 5, 10, 10, "FPS: " + str(frame_rate))

		pygame.display.update()
		clock.tick(FPS)
		await asyncio.sleep(0)

	pygame.quit()
	sys.exit()


asyncio.run(main())
