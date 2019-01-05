import pygame as pg
import sys
import os
from pygame import *
from random import randrange

import time
import math

WIDTH=600
HEIGHT=525
# player origin-> //center//9,8






from level import *




class Game:
	def __init__(self):
		os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" %(250,60)
		pg.init()
		# 1000/650 good resolution
		self.size=(WIDTH,HEIGHT)
		self.screen=pg.display.set_mode(self.size)
		pg.display.set_caption('pokemon maybe')
		self.running=True

		self.keys=[False]*500
		self.lastTime=0
		self.delta=0
		self.fps=60
		self.frameTime=1/self.fps
		self.level=Level(20,50)


	def render(self):
		draw.rect(self.screen,(0,0,0),Rect(0,0,self.size[0],self.size[1]))
		self.level.render(self.screen)
		pg.display.update()

	def update(self):
		self.level.update()
			

		
	def timer(self):
		self.delta+=time.clock()-self.lastTime
		if self.delta>=self.frameTime:
			self.delta=0
			self.lastTime=time.clock()
			return True
		return False


	def loop(self):
		while self.running:
			for event in pg.event.get():
				if event.type==pg.QUIT:
					self.running=False
				if event.type==pg.KEYDOWN:
					self.keys[event.key]=True
				if event.type==pg.KEYUP:
					self.keys[event.key]=False
				
			
			if self.timer():			
				self.update()
				self.render()
			else:
				self.render()

		pg.quit()
		sys.exit()


game=Game()
game.loop()