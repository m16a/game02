import sys
#import and init pygame
import pygame

BLUE =  (  0,   0, 255)

class Circle(object):
	def __init__(self):
		self.x = 50
		self.y = 50
		self.r = 20


pygame.init() 

#create the screen
window = pygame.display.set_mode((640, 480)) 

#draw a line - see http://www.pygame.org/docs/ref/draw.html for more 
pygame.draw.line(window, (255, 255, 255), (0, 0), (30, 50))

#draw it to the screen
 

c = Circle()

#input handling (somewhat boilerplate code):
while True:
	window.fill((0,0,0))
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			sys.exit(0) 
		# elif event.type == pygame.KEYUP:
		# 	  c.y = c.y - 10
		elif event.type == pygame.KEYDOWN:
			print event.key
			if event.key == 273:
				c.y = c.y - 10
			elif event.key == 274:
				c.y = c.y + 10
			elif event.key == 276:
				c.x = c.x - 10
			elif event.key == 275:
		  		c.x = c.x + 10	   
		else: 
	  		print event
	pygame.draw.circle(window, BLUE, [c.x, c.y], c.r)
	pygame.display.flip() 