import pygame 
import os
import random 

pygame.init()
pygame.font.init()

# colors 
white = (255, 255, 255)
blue = (0, 0, 200)
black = (0, 0, 0)

height = 640
width = 360

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Pickin Sticks")

small_font = pygame.font.SysFont('Comic Sans MS', 15)
med_font = pygame.font.SysFont('Comic Sans MS', 30)
large_font = pygame.font.SysFont('Comic Sans MS', 50)

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



class Pipes(pygame.sprite.Sprite): 
	# This class will create a pipe object with:  
	# 	- a sprite image and rect for each pipe
	#	- an x and y position for the pipes
	#	- functions to handle the movement of pipes and the score

	def __init__(self, the_player): 
		# load the images
		self.player = the_player
		self.bottom_image = load_image("Pipe_Long_bottom.png")
		self.top_image = load_image("Pipe_Long.png")
		self.space_between = 300
		self.did_collide = False
		self.did_player_pass = False
		
		# Positions
		self.xpos = 360
		self.ypos = round(random.randint(1, 33)* 20)

		#check to make sure the y position is within bounds
		while self.ypos > height or self.ypos < self.space_between: 
			self.ypos = round(random.randint(1, 33) * 20)
		

		# create rects
		self.bottom_rect = self.bottom_image.get_rect()
		self.bottom_rect.topleft = (self.xpos, self.ypos)
		self.top_rect = self.top_image.get_rect()
		self.top_rect.bottomleft = (self.xpos, self.ypos - self.space_between)

	
	# this function will move the pipes until the player hits the pipe
	def move_pipes(self): 
		if self.did_collide != True: 
			newpos = self.bottom_rect.move(-2, 0)
			self.bottom_rect = newpos

			newpos = self.top_rect.move(-2, 0)
			self.top_rect = newpos

			self.xpos -= 2


	def does_collide(self): 
		# function to check if the player and pipe collide
		# will set did_collide to true or false
		if self.bottom_rect.colliderect(self.player): 
			if self.did_collide != True: 
				self.did_collide = True

		if self.top_rect.colliderect(self.player): 
			if self.did_collide != True: 
				self.did_collide = True
			
	# Function to increment the score for the player
	def check_score(self): 
		if self.top_rect.right < self.player.rect.right: 
			if self.did_player_pass == False: 
				self.did_player_pass = True
				self.player.score += 1


	def update(self): 
		self.does_collide()		
		self.move_pipes()
		self.check_score()

	# checks whether the pipe is offscreen
	def offscren(self): 
		if self.top_rect.right < 0: 
			return True
		return False



 



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
		self.is_dead = False
		self.score = 0
		
		# physics properties
		self.gravity = 0.5
		self.lift = 20
		self.velocity = 0
		self.air_resistance = 0.95

	def jump(self): 
		self.velocity -= self.lift		

	
	def display_score(self): 
		score_string = "Score: " + str(self.score)
		screen_text = med_font.render(score_string, True, black)
		text_rect = screen_text.get_rect()
		text_rect.center = (275, 30)
		screen.blit(screen_text, text_rect)

	def update(self): 
		# this funciton upadates all the values of the player's bird

		# update the birds position
		self.velocity += self.gravity
		self.velocity *= self.air_resistance
		newpos = self.rect.move(0, self.velocity)
		self.rect = newpos

		# check to make sure the bird isn't too low or too high
	
		if self.rect.top <= 0: 
			newpos = self.rect.move(0, self.rect.top)
			self.velocity *= -0.85
		if self.rect.top > 690: 
			self.is_dead = True

		#check to make sure the player is alive
		if self.is_dead == True: 
			self.gravity = 0
			self.velocity = 0

		#display the score
		self.display_score()




class Background(pygame.sprite.Sprite): 
	# This class creates a background object and loads the image into the game
	# Image: Asian Mountain Forest BG by Crisisworks 
	# URL: https://opengameart.org/content/asian-mountain-forest-bg
	def __init__(self, imageFile, location): 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(imageFile)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location


def message_to_screen(msg, color, y_displacement = 0, size = "small"): 
	# Blits a message to the screen
	if size == "small": 
		screen_text = small_font.render(msg, True, color)
	if size == "medium": 
		screen_text = med_font.render(msg, True, color)
	if size == "large": 
		screen_text = large_font.render(msg, True, color)

	text_rect = screen_text.get_rect()
	text_rect.center = (width / 2), (height / 2) + y_displacement
	screen.blit(screen_text, text_rect)

def create_menu(): 
	message_to_screen("Flap", black, -100, "large")
	message_to_screen("By: Rory O'Connor", black, 0, "small")
	message_to_screen("Press Space to Play", black, 100, "medium")
	#message_to_screen("Press C for credits", black, 150, "small")


def display_game_over(user_score): 
	game_over_str = "Game Over"
	play_again_str = "Press space to play again"
	quit_string = "or Q to quit"
	score_string = "Score: " + str(user_score)

	message_to_screen(game_over_str, black, -20, "large")
	message_to_screen(score_string, black, 25, "medium")
	message_to_screen(play_again_str, black, 65, "small")
	message_to_screen(quit_string, black, 85, "small")


def main_menu(): 
	intro = True
	pygame.display.update()
	while intro: 
		screen.fill(white)
		create_menu()
		pygame.display.update()

		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				intro = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE: 
					intro = False



def game_loop(): 


 
	player = Player()
	BackGround = Background("imageBackground.png", [0,0])	

	game_exit = False
	is_game_over = False

	bird_sprite = pygame.sprite.RenderPlain((player))

	pipe_list = []
	pipe_list.append(Pipes(player))

	clock = pygame.time.Clock()

	while not game_exit: 
		# lock the game to 50 fps
		clock.tick(50)

		while is_game_over == True:
			screen.fill(white)
			display_game_over(player.score)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN: 
					if event.key == pygame.K_SPACE: 
						game_loop()
					if event.key == pygame.K_q: 
						game_exit = True
						is_game_over = False
				if event.type == pygame.QUIT: 
					is_game_over = False
					game_exit = True

		#Event Handling
		for event in pygame.event.get(): 
			# if the player is trying to quit
			if event.type == pygame.QUIT: 
				game_exit = True
			# exit if the player has died
			if player.is_dead == True: 
				game_exit = True
			# handle jumping 
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE:
					if pipe_list[0].did_collide == False:  
						player.jump()

		 
		 # space out the last element correctcly
		if pipe_list[-1].xpos < 20: 
			pipe_list.append(Pipes(player))
		if pipe_list[0].offscren(): 
			pipe_list.pop(0) 


		screen.blit(BackGround.image, BackGround.rect)

		

		for each_pipe in pipe_list: 
			each_pipe.update()
			screen.blit(each_pipe.bottom_image, each_pipe.bottom_rect)
			screen.blit(each_pipe.top_image, each_pipe.top_rect)

		# check if the player is under the screen
		if player.rect.top > 660: 
			is_game_over = True

		bird_sprite.update()
		
		bird_sprite.draw(screen)
		pygame.display.update()

	pygame.quit()
	quit()

main_menu()
game_loop()