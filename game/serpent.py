import pygame,sys,random
from pygame.locals import*
import time
import numpy
from numpy import linalg as LA 
import cv2
import pylab
import math
winx = 64*5
winy = 64*5
cellsize = 4*5
 
assert (winx%cellsize == 0 and winy%cellsize == 0),'cell number needs to be interger'
cellx = int(winx/cellsize)
celly = int(winy/cellsize)
 
red = (0,155,155)
green = (0,155,0)
darkgreen = (0,155,0)
white = (255,255,255)
black = (0,0,0)
 
left = 'left'
right = 'right'
down = 'down'
up = 'up'
 
head = 0

fpsclock = pygame.time.Clock()
disp = pygame.display.set_mode((winx,winy))
distance_diag = LA.norm([cellx,celly])
distance_record = 1

class GameState:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('serpent new')
		disp.fill(black)
		drawborder()
	    
		self.len_pre = 3
		self.direction = random.choice([left,right,up,down])
		startx = random.randint(5,cellx - 6)
		starty = random.randint(5,celly - 6)
		self.wormy = [{'x': startx, 'y': starty},
				 {'x': startx-1, 'y': starty},
				 {'x': startx-2, 'y': starty}]
		self.FPS = 10
		self.apple = randomapple()
		global distance_record
		distance_record = 1

	def frame_step(self, input_actions):
		pygame.event.pump()
		global distance_record

		terminal = False
		reward = 0
		if sum(input_actions) != 1:
			raise ValueError('Multiple input actions!')
		if input_actions[1] == 1 and self.direction!=right:
			self.direction = left
		elif input_actions[2] == 1 and self.direction!=left:
			self.direction = right
		elif input_actions[3] == 1 and self.direction!=down:
			self.direction = up
		elif input_actions[4] == 1:
			self.direction = down

		score = len(self.wormy) - 3

		if self.wormy[head]['x'] == cellx -1 or self.wormy[head]['x'] == 0 or self.wormy[head]['y'] == celly-1 or self.wormy[head]['y'] == 0:
			self.__init__()
			reward = -1
			terminal = True
		for wormybody in self.wormy[1:]:
			if wormybody['x'] == self.wormy[head]['x'] and wormybody['y'] == self.wormy[head]['y']:
				self.__init__()
				reward = -1
				terminal = True
		if self.wormy[head]['x'] == self.apple['x']  and  self.wormy[head]['y'] == self.apple['y']:
			self.apple = randomapple()
			reward = 1
		else:
			del self.wormy[-1]

		if self.direction == up:
			newhead = {'x':self.wormy[head]['x'],'y':self.wormy[head]['y']-1}
		if self.direction == down:
			newhead = {'x':self.wormy[head]['x'],'y':self.wormy[head]['y']+1}
		if self.direction == left:
			newhead = {'x':self.wormy[head]['x']-1,'y':self.wormy[head]['y']}
		if self.direction == right:
			newhead = {'x':self.wormy[head]['x']+1,'y':self.wormy[head]['y']}

		self.wormy.insert(0,newhead)
		disp.fill(black)
		drawborder()
		drawwormy(self.wormy)
		drawapple(self.apple)
		# drawscore
		if self.len_pre != len(self.wormy):
			print 'Score: '+str(score + 1) # wormy - 3 is the score
			self.len_pre = len(self.wormy)
		image_data = pygame.surfarray.array3d(pygame.display.get_surface())

		pygame.display.update()
		fpsclock.tick(self.FPS)
		return image_data, reward, terminal, score

def drawapple(coords):
 
	pygame.draw.circle(disp,red,(coords['x']*cellsize+cellsize/2,coords['y']*cellsize+cellsize/2),cellsize/2,0)
 
def randomapple():
	applex = random.randint(1,cellx-2)
	appley = random.randint(1,celly-2)
	return {'x':applex,'y':appley}
 
def drawwormy(wormy):
	for board in wormy:
		x = board['x']*cellsize
		y = board['y']*cellsize
		pygame.draw.rect(disp,darkgreen,(x,y,cellsize,cellsize))

def drawborder():
	pygame.draw.rect(disp,white,(0,0,winy,cellsize))
	pygame.draw.rect(disp,white,(0,winy - cellsize,winx,winy))
	pygame.draw.rect(disp,white,(0,0,cellsize,winy))
	pygame.draw.rect(disp,white,(winx-cellsize,0,winx,winy))     

if __name__ =='__main__':
	serpent = GameState()
	actions = [0,0,0,0,0]
	while True:
		action = raw_input().strip()
		action = int(action)
		actions[action] = 1
		image_data, reward, terminal = serpent.frame_step(actions)
		observation = cv2.cvtColor(cv2.resize(image_data, (80,80)), cv2.COLOR_BGR2GRAY)
		# ret, observation = cv2.threshold(observation,0,1,cv2.THRESH_BINARY)
		observation = observation/255.
		# print numpy.linalg.norm(observation)
		# print observation
		# print 'reward is'
		# print reward
		# pylab.imshow(observation)
		# pylab.show()
		time.sleep(1)
		actions = [0,0,0,0,0]


		
