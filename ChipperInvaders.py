from ProjectConstants import *
from Sprite import Sprite, remove_collisions, resize_image
import random
import time


class ChipperInvaders:
	def __init__(self, centerX, centerY, cookieSpeed, armanSpeed):
		self.state = "Title Screen 1"  #Title Screen 1, Level 1
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)  #degrees
		self.cookieSpeed = cookieSpeed
		self.armanSpeed = armanSpeed
		self.arrowLength = 50

		self.cookieRadius = 25
		self.cookie = pygame.image.load('images/cookie.png').convert_alpha()
		self.scaled_cookie = pygame.transform.scale(self.cookie, (2 * self.cookieRadius, 2 * self.cookieRadius)).convert_alpha()

		self.last_spawn_time = time.time()  # Track the last spawn time
		self.spawn_interval = random.uniform(1, 2)  # Random spawn interval

		arman1 = pygame.image.load('images/arman_hanate.jpeg').convert()
		scaledArman1 = resize_image(arman1, 75)
		arman2 = pygame.image.load('images/arman_stroke.jpeg').convert()
		scaledArman2 = resize_image(arman2, 75)
		arman3 = pygame.image.load('images/arman_wide.jpeg').convert()
		scaledArman3 = resize_image(arman3, 75)

		self.allArmanImages: pygame.image = [scaledArman1, scaledArman2, scaledArman3]

		self.cookies: list[Sprite] = []
		self.armans: list[Sprite] = []
		self.score = 0
		self.strikes = 0

	def set_state(self, state):
		self.state = state

	def change_angle(self):
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)

	def draw_static(self, screen):
		if self.state == "Title Screen 1":
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70, 70, "Chipper Invaders")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, 30, "Are you ready?... for the state of Joe")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, 25, "Click to continue")

			if ifClicked():
				self.state = "Level 1"

		if self.state == "Level 1":
			draw_text_center(screen, SCREEN_WIDTH / 2, 30, 30, "Chipper Invaders: Level 1")
			self.change_angle()

			blit_center(screen, self.scaled_cookie, (self.originalCenterX, self.originalCenterY))

			#draw arrow
			arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
			arrowLayer.fill((0, 0, 0, 0))

			pygame.draw.rect(arrowLayer, objectsColor, (100 + self.cookieRadius + 10, 97, self.arrowLength, 6))
			pygame.draw.polygon(arrowLayer, objectsColor, ((100 + self.cookieRadius + 10 + self.arrowLength, 90),
														   (100 + self.cookieRadius + 10 + self.arrowLength + 10, 100),
														   (100 + self.cookieRadius + 10 + self.arrowLength, 110)))

			rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

			screen.blit(rotatedSurface, center)

			current_time = time.time()  # Get the current time

			#Check if it's time to create new arman
			if current_time - self.last_spawn_time >= self.spawn_interval:
				self.armans.append(
					Sprite(self.allArmanImages[random.randint(0, 2)], SCREEN_WIDTH, random.randint(100, SCREEN_HEIGHT - 100), self.armanSpeed, -180,
						   "rectangle", 1))
				self.last_spawn_time = current_time
				self.spawn_interval = random.uniform(0.5, 2)  # Randomize the spawn interval again

			#draw all armans
			for arman in self.armans:
				arman.draw_static(screen)
				arman.draw_hitbox(screen)

			#if mouse is clicked, add a new cookie to cookie list
			if ifClicked():
				self.cookies.append(Sprite(self.scaled_cookie, self.currentCenterX, self.currentCenterY, self.cookieSpeed, self.angle, "circle", 0.8))

			#draw all cookies
			for cookie in self.cookies:
				cookie.draw_static(screen)
				cookie.draw_hitbox(screen)

			#remove cookies that are colliding
			self.score += remove_collisions(self.cookies, self.armans)

			#remove sprites that are past boundaries of screen
			self.cookies = [cookie for cookie in self.cookies if 0 < cookie.get_centerX() < SCREEN_WIDTH and 0 < cookie.get_centerY() < SCREEN_HEIGHT]

			amtArmans = len(self.armans)
			self.armans = [arman for arman in self.armans if 0 < arman.get_centerX() < SCREEN_WIDTH and 0 < arman.get_centerY() < SCREEN_HEIGHT]

			self.strikes += amtArmans - len(self.armans)

			draw_text_left(screen, SCREEN_WIDTH - 130, 100, 25, "Score: " + str(self.score))
			draw_text_left(screen, SCREEN_WIDTH - 130, 135, 25, "Strikes: " + str(self.strikes))
