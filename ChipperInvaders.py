from ProjectConstants import *
from Sprite import Sprite, remove_collisions, resize_image, remove_collisions_from_list_1
import random
import time
from pygame import mixer
from Button import Button


class ChipperInvaders:
	def __init__(self, centerX, centerY, cookieSpeed, armanSpeed):
		self.state = "Title Screen 1"  #Title Screen 1, Level 1, Level 2, Level 3, Level 4, Level 5, Boss Menu, Boss Level, Done, Fail
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)  #degrees
		self.cookieSpeed = cookieSpeed
		self.originalArmanSpeed = armanSpeed
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

		troll = pygame.image.load('images/TROLLER.png').convert_alpha()
		self.scaledTroll = resize_image(troll, 150).convert_alpha()

		self.trolls: list[Sprite] = []
		self.score = 0
		self.strikes = 0

		boss = pygame.image.load('images/boss.jpg').convert()
		self.scaledBoss = resize_image(boss, SCREEN_HEIGHT - 200)
		self.spriteBoss = Sprite(self.scaledBoss, SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2, -25, 0, "rectangle", 1)

		self.restartButton = Button(centerX=SCREEN_WIDTH - 75, centerY=SCREEN_HEIGHT - 50, width=100, height=50, textSize=30, borderSize=10,
									text="Reset")

	def draw_reset_button(self, screen):
		if self.restartButton.draw_and_check_click(screen):
			self.reset_all_objects()
			self.state = "Title Screen 1"

	def set_state(self, state):
		self.state = state

	def change_angle(self):
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)

	def reset_all_objects(self):
		self.cookies = []
		self.armans = []

		self.trolls = []

		self.spriteBoss.set_centerX_and_centerY(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2)

		try:
			for x in range(int(self.state[-1])):
				self.trolls.append(Sprite(self.scaledTroll, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 50, 0, "rectangle", 1))
		except:
			pass

		self.score = 0
		self.strikes = 0

	def draw_static(self, screen):
		if self.state == "Fail":
			screen.blit(resize_image(self.allArmanImages[2], SCREEN_WIDTH - 100), (50, 100))

			if len(self.trolls) < 10:
				self.trolls.append(
					Sprite(self.scaledTroll, random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
						   1))

			self.trolls = [troll for troll in self.trolls if 0 < troll.get_centerX() < SCREEN_WIDTH and 0 < troll.get_centerY() < SCREEN_HEIGHT]

			for troll in self.trolls:
				troll.randomly_move()
				troll.draw_static(screen)

			# if len(self.armans) < 10:
			# 	self.armans.append(
			# 		Sprite(self.allArmanImages[random.randint(0, 2)], random.randint(100, SCREEN_WIDTH - 100),
			# 			   random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
			# 			   1))
			#
			# self.armans = [arman for arman in self.armans if 0 < arman.get_centerX() < SCREEN_WIDTH and 0 < arman.get_centerY() < SCREEN_HEIGHT]
			#
			# for arman in self.armans:
			# 	arman.randomly_move()
			# 	arman.draw_static(screen)

			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70, 70, "WHY IS BRO TROLLIONING")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, 30, "start from lvl 1 again boi")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, 25, "Click to continue")

			if ifClicked():
				self.state = "Level 1"
				self.reset_all_objects()

		elif self.state == "Boss Menu":
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70, 70, "are u ready for boss?")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, 30, "lets go to boss, boss")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, 25, "Click to continue")

			if ifClicked():
				self.state = "Boss Level"
				self.reset_all_objects()

		elif self.state == "Boss Level":
			if len(self.trolls) < 5:
				self.trolls.append(
					Sprite(self.scaledTroll, random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
						   1))

			self.trolls = [troll for troll in self.trolls if 0 < troll.get_centerX() < SCREEN_WIDTH and 0 < troll.get_centerY() < SCREEN_HEIGHT]

			for troll in self.trolls:
				troll.randomly_move()
				troll.draw_static(screen)

			if len(self.armans) < 10:
				self.armans.append(
					Sprite(self.allArmanImages[random.randint(0, 2)], random.randint(100, SCREEN_WIDTH - 100),
						   random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
						   1))

			self.armans = [arman for arman in self.armans if 0 < arman.get_centerX() < SCREEN_WIDTH and 0 < arman.get_centerY() < SCREEN_HEIGHT]

			for arman in self.armans:
				arman.randomly_move()
				arman.draw_static(screen)

			self.spriteBoss.draw_static(screen)

			draw_text_center(screen, SCREEN_WIDTH / 2, 30, 30, f"Chipper Invaders: {self.state}")
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

			#if mouse is clicked, add a new cookie to cookie list
			if ifClicked():
				self.cookies.append(Sprite(self.scaled_cookie, self.currentCenterX, self.currentCenterY, self.cookieSpeed, self.angle, "circle", 0.8))
				cookieSound = mixer.Sound("sounds/gol.ogg")
				cookieSound.play()

			#draw all cookies
			for cookie in self.cookies:
				cookie.draw_static(screen)

			#remove cookies that are colliding
			self.score += remove_collisions_from_list_1(self.cookies, self.spriteBoss)

			if self.score == 69:
				self.state = "Done"

			self.spriteBoss.get_next_frame()

			#remove sprites that are past boundaries of screen
			self.cookies = [cookie for cookie in self.cookies if 0 < cookie.get_centerX() < SCREEN_WIDTH and 0 < cookie.get_centerY() < SCREEN_HEIGHT]

			if self.originalCenterX + 159 > self.spriteBoss.get_centerX():
				self.state = "Fail"
				self.reset_all_objects()

			draw_text_left(screen, SCREEN_WIDTH - 130, 100, 25, "Score: " + str(self.score))

		elif self.state == "Done":
			self.draw_reset_button(screen)

			if len(self.trolls) < 5:
				self.trolls.append(
					Sprite(self.scaledTroll, random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
						   1))

			self.trolls = [troll for troll in self.trolls if 0 < troll.get_centerX() < SCREEN_WIDTH and 0 < troll.get_centerY() < SCREEN_HEIGHT]

			for troll in self.trolls:
				troll.randomly_move()
				troll.draw_static(screen)

			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70, 70, "good job joller")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, 30, "get trolled")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, 25, "Click to continue")

		elif self.state == "Title Screen 1":
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70, 70, "Chipper Invaders")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30, 30, "Are you ready?... for the state of Joe")
			draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, 25, "Click to continue")

			if ifClicked():
				self.state = "Level 1"

		else:
			draw_text_center_alpha(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, self.state[-1], 50)

			self.armanSpeed = self.originalArmanSpeed * int(self.state[-1])

			draw_text_center(screen, SCREEN_WIDTH / 2, 30, 30, f"Chipper Invaders: {self.state}")
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

			#if mouse is clicked, add a new cookie to cookie list
			if ifClicked():
				self.cookies.append(Sprite(self.scaled_cookie, self.currentCenterX, self.currentCenterY, self.cookieSpeed, self.angle, "circle", 0.8))
				cookieSound = mixer.Sound("sounds/gol.ogg")
				cookieSound.play()

			#draw all cookies
			for cookie in self.cookies:
				cookie.draw_static(screen)

			#draw all trolls
			for troll in self.trolls:
				troll.draw_static(screen)
				troll.randomly_move()

			#remove cookies that are colliding
			self.score += remove_collisions(self.cookies, self.armans)

			if len(self.trolls) < int(self.state[-1]) + self.strikes:
				self.trolls.append(
					Sprite(self.scaledTroll, random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100), 50, 0, "rectangle",
						   1))

			#remove sprites that are past boundaries of screen
			self.cookies = [cookie for cookie in self.cookies if 0 < cookie.get_centerX() < SCREEN_WIDTH and 0 < cookie.get_centerY() < SCREEN_HEIGHT]
			self.trolls = [troll for troll in self.trolls if 0 < troll.get_centerX() < SCREEN_WIDTH and 0 < troll.get_centerY() < SCREEN_HEIGHT]

			amtArmans = len(self.armans)
			self.armans = [arman for arman in self.armans if 0 < arman.get_centerX() < SCREEN_WIDTH and 0 < arman.get_centerY() < SCREEN_HEIGHT]

			if amtArmans != len(self.armans):
				self.strikes += 1
				self.trolls.append(Sprite(self.scaledTroll, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 50, 0, "rectangle", 1))
			# self.strikes += amtArmans - len(self.armans)

			draw_text_left(screen, SCREEN_WIDTH - 130, 100, 25, "Score: " + str(self.score))
			draw_text_left(screen, SCREEN_WIDTH - 130, 135, 25, "Strikes: " + str(self.strikes))

			#if 3 strikes, game failed and restart
			if self.strikes >= 3:
				self.state = "Fail"
				self.reset_all_objects()
				self.armanSpeed = self.originalArmanSpeed

			if self.score == 10:
				if self.state[-1] == "1":
					self.state = "Level 2"
				elif self.state[-1] == "2":
					self.state = "Level 3"
				elif self.state[-1] == "3":
					self.state = "Level 4"
				elif self.state[-1] == "4":
					self.state = "Level 5"
				elif self.state[-1] == "5":
					self.state = "Boss Menu"

				self.reset_all_objects()
