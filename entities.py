import pygame as pg
import sys
import os
from pygame import *
from random import randrange

import time
import math
import random

BLACK=(0,0,0)

class Entity:
	def __init__(self,tile_x,tile_y,source_rect,assetsManager):
		self.texture=assetsManager.crop(source_rect)
		self.texture.set_colorkey(BLACK)
		self.tempRect=self.texture.get_rect()
		self.size=32#shows grid based engine
		self.x=tile_x*self.size
		self.y=tile_y*self.size
		self.bounds=Rect(self.x,self.y,self.size,self.size)


	def checkCollision(self,move_x,move_y,target):
		rect=Rect(self.x+move_x,self.y+move_y,self.size,self.size)
		return rect.colliderect(target)

	def update(self,level):
		self.update_bounds()

	def update_bounds(self):
		self.bounds=Rect(self.x,self.y,self.size,self.size)

	def render(self,display,off):
		bounds=(self.x-off[0],self.y-off[1])
		display.blit(self.texture,bounds)

class Mob(Entity):
	def __init__(self,tile_x,tile_y,source_rect,assetsManager):
		super().__init__(tile_x,tile_y,source_rect,assetsManager)
		self.tickCount=0
		self.anim_counter=0
		self.anim_index=0
		self.max_value=4
		self.assetsManager=assetsManager
		self.textures=self.fill_textures()
		self.default_speed=0.5
		self.boost_speed=self.default_speed*2
		self.speed=self.default_speed
		self.boost=False

	def chase(self,x_target,y_target):
		x_dir=0
		y_dir=0
		xx=x_target-self.x
		yy=y_target-self.y
		if xx>0:
			x_dir=1
			y_dir=0
		elif xx<0:
			x_dir=-1
			y_dir=0
		if yy>0:
			y_dir=1
			x_dir=0

		elif yy<0:
			y_dir=-1
			x_dir=0

		return(x_dir,y_dir)
			



	def update(self,level):
		# x_dir=randrange(-1,2)
		# y_dir=randrange(-1,2)
		# if x_dir!=0 and y_dir!=0:
		# 	x_dir=0
		# if random.randint(0,10)>8:
		# 	dx,dy=x_dir,y_dir
			
		player=level.entities[0]
		dx,dy=self.chase(player.x,player.y)
		
		dx*=self.speed
		dy*=self.speed
		
		self.get_frame()
		self.texture=self.get_animated_texture(dx,dy,self.anim_index)
	

		# if random.randint(0,10)>5:
		self.x+=dx
		self.y+=dy

		self.update_bounds()



	def get_frame(self):
		time_lapse=0
		if self.boost:
			time_lapse=5
		else:
			time_lapse=10
		self.anim_counter+=1
		if self.anim_counter>time_lapse:
			self.anim_index+=1
			self.anim_counter=0
			if(self.anim_index>=self.max_value):
				self.anim_index=0

	def fill_textures(self):
		textures=[0]*4
		for y in range(4):
			textures[y]=[0]*4
		tile_size=64
		for y in range(4):
			for x in range(4):
				textures[y][x]=self.assetsManager.crop((x*tile_size,y*tile_size,tile_size,tile_size))
				textures[y][x].set_colorkey(BLACK)
		return textures		
		
	def get_animated_texture(self,x_dir,y_dir,index):
		if x_dir >0 and y_dir==0:
			return self.textures[2][index]
		if x_dir <0 and y_dir==0:
			return self.textures[1][index]
		if x_dir ==0 and y_dir>0:
			return self.textures[0][index]
		if x_dir ==0 and y_dir<0:
			return self.textures[3][index]
		else:
			return self.textures[0][0]




class Player(Mob):
	def __init__(self,tile_x,tile_y,source_rect,assetsManager):
		super().__init__(tile_x,tile_y,source_rect,assetsManager)
		self.default_speed=3
		self.boost_speed=self.default_speed*2
		self.speed=self.default_speed


	def move(self,direction,level):
		dx,dy=direction
		if key.get_pressed()[K_LSHIFT]:
			self.boost=True
		self.get_frame()
		self.texture=self.get_animated_texture(dx,dy,self.anim_index)
		


		if self.boost:
			self.speed=self.boost_speed
			self.boost=False
		else:
			self.speed=self.default_speed
		
		move_x=dx*self.speed
		move_y=dy*self.speed


		entities=level.entities
		for index,entity in enumerate(level.entities):
			if type(entity).__name__=="Player":
				continue
			# if entity ==self:
			# 	print('checked')
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
