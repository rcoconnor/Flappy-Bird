import pygame 
import os

pygame.init()
pygame.font.init()

# colors 
white = (255, 255, 255)
blue = (0, 0, 200)

height = 640
width = 360

screen = pygame.display.set_mode((width, height))

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
	# 	- a sprite image and rect
	# 	- x and y poss

	def __init__(self): 
		
		# sprite properties 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("bird_sprite.jpg", -1)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.rect = self.image.get_rect()
		self.ypos = 300
		self.xpos = 120
		self.rect.topleft = (self.xpos, self.ypos)
		
		# physics properties
		self.gravity = 0.5
		self.lift = 20
		self.velocity = 0
		self.air_resistance = 0.95

	def jump(self): 
		self.velocity -= self.lift

	def update(self): 
		# this funciton upadates all the values of the player's bird
		# check to make sure the bird isn't too low
		
		"""if self.rect.bottom > height: 
			self.y = height
			self.velocity = 0

		# check to make sure the bird isn't too high
		if self.rect.top < 0: 
			self.y = 0
			self.velocity = 0 """

		# update the birds position
		self.velocity += self.gravity
		self.velocity *= self.air_resistance
		newpos = self.rect.move(0, self.velocity)
		self.rect = newpos

		if self.rect.bottom > height: 
			self.velocity *= -1

		if self.rect.top < 0: 
			newpos = self.rect.move(0, self.rect.top)
			self.velocity *= -0.85


class Background(pygame.sprite.Sprite): 
	# This class creates a background object and loads the image into the game
	# Image: Asian Mountain Forest BG by Crisisworks 
	# URL: https://opengameart.org/content/asian-mountain-forest-bg
	def __init__(self, imageFile, location): 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(imageFile)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location



def game_loop(): 

	

	screen.fill(blue)


	player = Player()
	BackGround = Background("imageBackground.png", [0,0])	

	game_exit = False
	allsprites = pygame.sprite.RenderPlain((player))


	clock = pygame.time.Clock()

	while not game_exit: 
		# lock the game to 50 fps
		clock.tick(50)

		#Event Handling
		for event in pygame.event.get(): 
			# if the player is trying to quit
			if event.type == pygame.QUIT: 
				game_exit = True
			# handle jumping 
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE: 
					player.jump()


		allsprites.update()
		screen.fill((255, 255, 255))
		screen.blit(BackGround.image, BackGround.rect)
		allsprites.draw(screen)
		pygame.display.update()

	pygame.quit()
	quit()

game_loop()