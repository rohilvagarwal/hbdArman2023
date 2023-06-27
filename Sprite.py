from ProjectConstants import *


class Sprite:
	def __init__(self, image, centerX, centerY, velocity, angle):
		self.image = image
		self.centerX = centerX
		self.centerY = centerY
		self.velocity = velocity
		self.angle = angle
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

	def get_centerX(self):
		return int(self.centerX)

	def get_centerY(self):
		return int(self.centerY)

	def set_velocity_and_angle(self, velocity, angle):
		self.velocity = velocity
		self.angle = angle
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

	def draw_static(self, screen):
		self.centerX += self.xVelocity / FPS
		self.centerY += self.yVelocity / FPS

		blit_center(screen, self.image, (self.centerX, self.centerY))
