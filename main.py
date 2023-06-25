import math

from ProjectConstants import *
import sys
from Button import Button
import time

#pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#image imports
d4 = pygame.image.load('images/d4Logo.svg')
scaled_d4 = pygame.transform.scale(d4, (50, 50))

#game variables
GAME_OVER = False

#game states: menu, kinematics, circularMotion, aboutMe
gameState = "menu"


def menu_button(centerX, centerY, text):
	return Button(centerX=centerX, centerY=centerY, width=230, height=50, textSize=30, borderSize=10, text=text)


def return_to_menu_button():
	global gameState

	menuButton = Button(centerX=SCREEN_WIDTH - 75, centerY=50, width=100, height=50, textSize=30, borderSize=10, text="Menu")

	if menuButton.draw_and_check_click(screen):
		gameState = "menu"


def draw_d4():
	screen.blit(scaled_d4, (0, 10))


def draw_menu():
	global gameState
	global GAME_OVER
	screen.fill(backgroundColor)
	draw_d4()

	#draw title
	draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10, 70, "Arman Gaming")

	chippers = menu_button(200, 2 * SCREEN_HEIGHT / 6, "Chippers")
	exit = menu_button(200, 5 * SCREEN_HEIGHT / 6, "Exit")

	#draw button and check if clicked
	if chippers.draw_and_check_click(screen):
		gameState = "chippers"

	if exit.draw_and_check_click(screen):
		GAME_OVER = True

#game start
draw_menu()
pygame.display.update()

frame_count = 0
frame_rate = 0
start_time = time.time()

while not GAME_OVER:
	if gameState == "menu":
		draw_menu()


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

pygame.quit()
sys.exit()
