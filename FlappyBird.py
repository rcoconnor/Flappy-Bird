import pygame 
import os

pygame.init()
pygame.font.init()

white = (255, 255, 255)

screen = pygame.display.set_mode((360, 640))

pygame.display.set_caption("Pickin Sticks")

def load_image(name, colorkey = None): 
	try: 
		image = pygame.image.load(name)
	except pygame.error as error: 
		print("Cannot load image: ", name)
		raise systemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1: 
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image

class Player(pygame.sprite.Sprite): 
	# This class will create a player class with
	# 	-a sprite
	# 	-height

	def __init__(self): 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("bird_sprite.jpg", -1)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.rect = self.image.get_rect()
		self.ypos = 300
		self.xpos = 200
		self.rect.topleft = (self.xpos, self.ypos)


def game_loop(): 

	screen.fill(white)

	player = Player()

	game_exit = False

	allsprites = pygame.sprite.RenderPlain((player))


	while not game_exit: 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				game_exit = True

		allsprites.update()
		allsprites.draw(screen)
		pygame.display.update()

	pygame.quit()
	quit()

game_loop()