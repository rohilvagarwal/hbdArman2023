from ProjectConstants import *


def remove_collisions(list1: list["Sprite"], list2: list["Sprite"]):
	num_collisions = 0

	for item1 in list1:
		for item2 in list2:
			if item1.collides_with(item2):
				# Remove colliding items from list1 and list2
				list1.remove(item1)
				list2.remove(item2)
				num_collisions += 1

	return num_collisions


def resize_image(pic, maxDimension):
	maxNum = max(pic.get_width(), pic.get_height())

	return pygame.transform.scale(pic, (pic.get_width() * maxDimension // maxNum, pic.get_height() * maxDimension // maxNum)).convert()


class Sprite:
	def __init__(self, image, centerX, centerY, velocity, angle, hitboxShape: str, hitboxScale):
		self.image = image
		self.centerX = centerX
		self.centerY = centerY
		self.velocity = velocity
		self.angle = angle
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

		#define hitbox dimensions
		self.hitboxShape = hitboxShape
		if self.hitboxShape == 'rectangle':
			self.width = self.image.get_width() * hitboxScale
			self.height = self.image.get_height() * hitboxScale
		elif self.hitboxShape == 'circle':
			self.radius = max(self.image.get_width(), self.image.get_height()) / 2 * hitboxScale

	def get_centerX(self):
		return self.centerX

	def get_centerY(self):
		return self.centerY

	def get_hitbox_shape(self):
		return self.hitboxShape

	def set_velocity_and_angle(self, velocity, angle):
		self.velocity = velocity
		self.angle = angle
		self.xVelocity = math.cos(math.radians(self.angle)) * self.velocity
		self.yVelocity = -math.sin(math.radians(self.angle)) * self.velocity

	def get_next_frame(self):
		self.centerX += self.xVelocity / FPS
		self.centerY += self.yVelocity / FPS

	def draw_static(self, screen):
		self.get_next_frame()
		blit_center(screen, self.image, (self.centerX, self.centerY))

	def get_hitbox(self):
		if self.hitboxShape == 'rectangle':
			# Calculate hitbox coordinates for a rectangle
			left = self.centerX - self.width / 2
			top = self.centerY - self.height / 2
			right = self.centerX + self.width / 2
			bottom = self.centerY + self.height / 2
			return left, top, right, bottom
		elif self.hitboxShape == 'circle':
			# Return hitbox coordinates for a circle
			return self.centerX, self.centerY, self.radius

	def collides_with(self, other_sprite: "Sprite"):
		self_hitbox = self.get_hitbox()
		other_hitbox = other_sprite.get_hitbox()

		if self.hitboxShape == 'rectangle' and other_sprite.get_hitbox_shape() == 'rectangle':
			# Check for collision between two rectangles
			if self_hitbox[2] >= other_hitbox[0] and self_hitbox[0] <= other_hitbox[2] and \
					self_hitbox[3] >= other_hitbox[1] and self_hitbox[1] <= other_hitbox[3]:
				return True
		elif self.hitboxShape == 'circle' and other_sprite.get_hitbox_shape() == 'circle':
			# Check for collision between two circles
			distance_squared = (self_hitbox[0] - other_hitbox[0]) ** 2 + (self_hitbox[1] - other_hitbox[1]) ** 2
			if distance_squared <= (self_hitbox[2] + other_hitbox[2]) ** 2:
				return True
		else:
			# Check for collision between a circle and a rectangle
			if self.hitboxShape == 'circle':
				circle_hitbox = self_hitbox
				rect_hitbox = other_hitbox
			else:
				circle_hitbox = other_hitbox
				rect_hitbox = self_hitbox

			closest_x = max(rect_hitbox[0], min(circle_hitbox[0], rect_hitbox[2]))
			closest_y = max(rect_hitbox[1], min(circle_hitbox[1], rect_hitbox[3]))

			distance_squared = (circle_hitbox[0] - closest_x) ** 2 + (circle_hitbox[1] - closest_y) ** 2
			if distance_squared <= circle_hitbox[2] ** 2:
				return True

		return False

	def draw_hitbox(self, screen):
		hitbox = self.get_hitbox()
		if self.hitboxShape == 'rectangle':
			left, top, right, bottom = hitbox
			pygame.draw.rect(screen, (255, 0, 0), (left, top, right - left, bottom - top), 2)
		elif self.hitboxShape == 'circle':
			pygame.draw.circle(screen, RED, (int(hitbox[0]), int(hitbox[1])), int(hitbox[2]), 2)
