from ProjectConstants import *

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

		self.cookieWidth = 50
		self.cookie = pygame.image.load('images/cookie.png')
		self.scaled_cookie = pygame.transform.scale(self.cookie, (50, 50))

	def change_angle(self):
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

	def draw_static(self, screen):
		self.change_angle()

		arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
		arrowLayer.fill((0, 0, 0, 0))

		pygame.draw.rect(arrowLayer, objectsColor, (100 + self.cookieWidth + 10, 97, self.arrowLength, 6))
		pygame.draw.polygon(arrowLayer, objectsColor, ((100 + self.cookieWidth + 10 + self.arrowLength, 90),
													   (100 + self.cookieWidth + 10 + self.arrowLength + 10, 100),
													   (100 + self.cookieWidth + 10 + self.arrowLength, 110)))

		rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

		screen.blit(rotatedSurface, center)