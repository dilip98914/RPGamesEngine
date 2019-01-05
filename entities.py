import pygame as pg
import sys
import os
from pygame import *
from random import randrange

import time
import math


class Entity:
	def __init__(self,tile_x,tile_y,color):
		self.size=32
		self.x=tile_x*self.size
		self.y=tile_y*self.size
		self.color=color
		#bounds at pixel coordinates
		self.bounds=Rect(self.x,self.y,self.size,self.size)


	def checkCollision(self,move_x,move_y,target):
		rect=Rect(self.x+move_x,self.y+move_y,self.size,self.size)
		# if (rect.x>target.x and rect.x<target.x+target.w and 
		# 	rect.y>target.y and rect.y<target.y+target.h):
		# 	return True
		# return False

		""" target must give current position rect"""
		return rect.colliderect(target)

	def update(self,level):
		self.update_bounds()

	def update_bounds(self):
		self.bounds=Rect(self.x,self.y,self.size,self.size)

	def render(self,display,off):
		bounds=Rect(self.x-off[0],self.y-off[1],self.size,self.size)
		draw.rect(display,self.color,bounds)

class Mob(Entity):
	def __init__(self,tile_x,tile_y,color):
		super().__init__(tile_x,tile_y,color)
		self.tickCount=0
		self.speed=1

	def move(self,direction):
		dx,dy=direction
		self.x+=dx*self.speed
		self.y+=dy*self.speed

	def update(self,level):
		x_dir=randrange(-1,2)
		y_dir=randrange(-1,2)
		if self.tickCount%100==0:
			# if self.checkCollision(x_dir*self.speed,0):
			self.move((x_dir,0))
			# if self.checkCollision(0,y_dir*self.speed):
			self.move((0,y_dir))
				
			self.tickCount=0
		self.tickCount+=1
		self.update_bounds()


class Player(Mob):
	def __init__(self,tile_x,tile_y,color):
		super().__init__(tile_x,tile_y,color)
		self.speed=6

	def move(self,direction,level):
		dx,dy=direction
		move_x=dx*self.speed
		move_y=dy*self.speed


		entities=level.entities
		for index,entity in enumerate(level.entities):
			# if type(entity).__name__=="Player":
			# 	continue
			if not self.checkCollision(move_x,0,entity.bounds):
				move_x=dx*self.speed
			if not self.checkCollision(0,move_y,entity.bounds):
				move_y=dy*self.speed

			if  self.checkCollision(move_x,move_y,entity.bounds):
				move_x=0
				move_y=0
						

		self.x+=move_x
		self.y+=move_y

	


	""" returns tuple with value dir_x,dir_y"""		
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


	def update(self,level):
		self.update_bounds()
		self.move(self.getInput(),level)

