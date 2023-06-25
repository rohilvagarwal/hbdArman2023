from ProjectConstants import *


class Button:
	def __init__(self, centerX, centerY, width, height, textSize, borderSize, text="empty"):
		#self.ifMouseDownEarlier = False

		#font
		self.menuFont = pygame.font.SysFont("jost700", textSize)

		#text
		self.buttonText = self.menuFont.render(text, True, textColor)
		self.textWidth = self.buttonText.get_width()
		self.textHeight = self.buttonText.get_height()
		self.buttonPosition = self.buttonText.get_rect(center=(centerX, centerY))

		#background
		self.buttonBackground = pygame.Rect(0, 0, width, height)
		self.buttonBackground.center = (centerX, centerY)
		self.borderSize = borderSize

	def draw_and_check_click(self, surface):
		pressed = False
		mousePos = pygame.mouse.get_pos()

		#if mouse is on button
		if self.buttonBackground.collidepoint(mousePos):
			pygame.draw.rect(surface, textColor, self.buttonBackground, width=self.borderSize)
			pygame.draw.rect(surface, hoverColor, self.buttonBackground.inflate(-self.borderSize, -self.borderSize))

			if ifClicked():
				pressed = True

		#if mouse is not on button
		else:
			pygame.draw.rect(surface, textColor, self.buttonBackground, width=self.borderSize)
			pygame.draw.rect(surface, backgroundColor, self.buttonBackground.inflate(-self.borderSize, -self.borderSize))

		surface.blit(self.buttonText, self.buttonPosition)

		return pressed
