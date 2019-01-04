import pygame as pg
import sys
import os
from pygame import *

import time



class Level:
	def __init__(self,tileWidth,tileHeight):
		self.w=tileWidth
		self.h=tileHeight
		self.tiles=[0]*self.h
		for y in range(self.h):
			self.tiles[y]=[0]*self.w
		self.fillArray()

	def fillArray(self):
		for y in range(self.h):
			for x in range(self.w):
				self.tiles[y][x]=Tile(x,y,(255,0,255))

	def render(self,display):
		for y in range(self.h):
			for x in range(self.w):
				self.tiles[y][x].render(display)



class Tile:
	def __init__(self,tile_x,tile_y,color):
		self.x=tile_x
		self.y=tile_y
		self.color=color
		self.w=32
		self.h=32

	def render(self,display):
		bounds=Rect(self.x*self.w,self.y*self.h,self.w,self.h)
		draw.rect(display,self.color,bounds)
		draw.rect(display,(0,0,0),bounds,1)

class Player:
	def __init__(self,tile_x,tile_y):
		self.x=tile_x
		self.y=tile_y
		self.color=(255,255,0)
		self.w=32
		self.h=32
		self.bounds=Rect(0,0,self.w,self.h)

		self.speed=1

	def move(self,direction):
		dx,dy=direction
		self.x+=dx*self.speed
		self.y+=dy*self.speed
	
	def getInput(self):
		if key.get_pressed()[K_UP]:
			return (0,-1)
		if key.get_pressed()[K_DOWN]:
			return (0,1)
		if key.get_pressed()[K_RIGHT]:
			return (1,0)
		if key.get_pressed()[K_LEFT]:
			return (-1,0)

		else:
			return(0,0)


	def update(self):
		self.move(self.getInput())


	def render(self,display):
		self.bounds[0]=self.x*self.w
		self.bounds[1]=self.y*self.h
		draw.rect(display,self.color,self.bounds)

class Game:
	def __init__(self):
		os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" %(250,60)
		pg.init()
		# 1000/650 good resolution
		self.size=(600,525)
		self.screen=pg.display.set_mode(self.size)
		pg.display.set_caption('pokemon maybe')
		self.running=True

		self.keys=[False]*500
		self.player=Player(0,0)
		self.lastTime=0
		self.delta=0
		self.frameTime=1/30
		self.level=Level(20,50)


	def render(self):
		draw.rect(self.screen,(0,0,0),Rect(0,0,self.size[0],self.size[1]))
		self.level.render(self.screen)
		self.player.render(self.screen)
		pg.display.update()

	def tick(self):
		self.player.update()
			

		
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
				self.tick()
				self.render()
			else:
				self.render()

		pg.quit()
		sys.exit()


game=Game()
game.loop()