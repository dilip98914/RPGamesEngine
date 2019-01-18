
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
LIGHT_BLUE=(128, 255, 255)
BROWN=(179, 60, 0)
GRAY=(184, 184, 148)
PINK=(255, 0, 102)
LIGHT_YELLOW=(255, 255, 77)
LIGHT_GREEN=(0, 255, 85)


WIDTH=600
HEIGHT=525

tile_colors=[LIGHT_BLUE,GREEN,LIGHT_GREEN,GRAY]
ORIGIN=(300,250)#center
from Assets import *
from entities import *

import pygame as pg

class Camera:
	def __init__(self):
		self.offset_x=0
		self.offset_y=0
		
	def update(self,player,level):
		x=player.x
		y=player.y
		self.offset_x=x-ORIGIN[0]
		self.offset_y=y-ORIGIN[1]
		self.check_corners(player,level)

	def check_corners(self,player,level):
		if player.x<=WIDTH/2:
			self.offset_x=0
		elif player.x>=level.w*32-WIDTH/2:
			self.offset_x=level.w*32-WIDTH
		if player.y<=HEIGHT/2:
			self.offset_y=0
		elif player.y>=level.h*32-HEIGHT/2:
			self.offset_y=level.h*32-HEIGHT



class Tile:
	def __init__(self,tile_x,tile_y,source_rect,ASSETS,solid=False,id=0):
		self.id=id
		self.texture=ASSETS.crop(source_rect)
		self.texture=pg.transform.scale(self.texture,(32,32))
		self.texture.set_colorkey(BLACK)
		self.tempRect=self.texture.get_rect()
		self.size=32
		self.x=tile_x*self.size
		self.y=tile_y*self.size
		self.solid=solid
		self.bounds=Rect(self.x,self.y,self.size,self.size)



	def render(self,display,off):
		display.blit(self.texture,(self.x-off[0],self.y-off[1]))



	

class Level:
	def __init__(self,tileWidth,tileHeight):
		self.w=tileWidth
		self.h=tileHeight
		self.camera=Camera()
		self.assetsManager=AssetsManager('playersheet.png')
		self.tileManager=AssetsManager('tileset.png')
		self.tiles=self.createTiles()
		self.entity_count=20
		self.entities=self.createEntities(self.entity_count)
		self.tile_id_map=self.create2DArray(self.w,self.h)
		self.fill_tile_map()

	def createEntities(self,len):
		entities=[0]*len
		entities[0]=Player(9,8,(0,0,64,64),self.assetsManager)
		# entities[1]=Mob(10,10,(0,0,64,64),self.assetsManager)
		for x in range(1,len):
			xx=randrange(int(WIDTH/32))
			yy=randrange(int(HEIGHT/32))
			entities[x]=Mob(xx,yy,(0,0,64,64),self.assetsManager)
		return entities

		if  self.checkCollision(move_x,move_y,entity.bounds):
				move_x=0
				move_y=0

	
	def fill_tile_map(self):
		for y in range(len(self.tiles)):
			for x in range(len(self.tiles[0])):
				self.tile_id_map[y][x]=self.tiles[y][x].id
			


	def add_to_entities(self,entity,index):
		self.entities[index]=entity

	def create2DArray(self,w,h):
		tiles=[0]*h
		for y in range(h):
			tiles[y]=[0]*w 
		return tiles

	def createTiles(self):
		tiles=self.create2DArray(self.w,self.h)
		for y in range(self.h):
			for x in range(self.w):
				tiles[y][x]=Tile(x,y,(16*3,16*2,16,16),self.tileManager,id=1)

		return tiles




	def update(self):
		self.camera.update(self.entities[0],self)
		for i in range(len(self.entities)):
			self.entities[i].update(self)

	def render(self,display):
		offset_x=self.camera.offset_x
		offset_y=self.camera.offset_y
		
		for y in range(self.h):
			for x in range(self.w):
				self.tiles[y][x].render(display,(offset_x,offset_y))


		for i in range(len(self.entities)):
			self.entities[i].render(display,(offset_x,offset_y))
