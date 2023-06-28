from ProjectConstants import *
from Sprite import Sprite


class ChipperInvaders:
	def __init__(self, centerX, centerY, velocity):
		self.state = "default"  #default, animating, paused, doneAnimating
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)  #degrees
		self.velocity = velocity
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity
		self.arrowLength = 50

		self.cookieRadius = 25
		self.cookie = pygame.image.load('images/cookie.png').convert_alpha()
		self.scaled_cookie = pygame.transform.scale(self.cookie, (2 * self.cookieRadius, 2 * self.cookieRadius)).convert_alpha()

		self.cookies: list[Sprite] = []

	def change_angle(self):
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

	def draw_static(self, screen):
		self.change_angle()

		blit_center(screen, self.scaled_cookie, (self.originalCenterX, self.originalCenterY))

		arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
		arrowLayer.fill((0, 0, 0, 0))

		pygame.draw.rect(arrowLayer, objectsColor, (100 + self.cookieRadius + 10, 97, self.arrowLength, 6))
		pygame.draw.polygon(arrowLayer, objectsColor, ((100 + self.cookieRadius + 10 + self.arrowLength, 90),
													   (100 + self.cookieRadius + 10 + self.arrowLength + 10, 100),
													   (100 + self.cookieRadius + 10 + self.arrowLength, 110)))

		rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

		screen.blit(rotatedSurface, center)

		if ifClicked():
			self.cookies.append(Sprite(self.scaled_cookie, self.currentCenterX, self.currentCenterY, self.velocity, self.angle, "circle", 0.8))

		for cookie in self.cookies:
			cookie.draw_static(screen)
			cookie.draw_hitbox(screen)

		self.cookies = [cookie for cookie in self.cookies if 0 < cookie.get_centerX() < SCREEN_WIDTH and 0 < cookie.get_centerY() < SCREEN_HEIGHT]
