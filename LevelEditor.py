import pygame as pg
from pygame import *


class LevelEditor:
	def __init__(self,tileManager):
		self.x=0
		self.y=0
		self.tileManager=tileManager
		self.tile_x=0
		self.tile_y=0
		self.scale_factor=16
		self.unit_rect=(self.scale_factor*self.tile_x,self.scale_factor*self.tile_y,self.scale_factor,self.scale_factor)
		self.already_pressed=False
		self.tick_count=0

	def get_next_tile(self):
		if key.get_pressed()[K_LCTRL] and not self.already_pressed:
			self.tile_x+=1
			if self.tile_x>=self.tileManager.image.get_width()/16:
				self.tile_x=0
			self.already_pressed=True
		if key.get_pressed()[K_RCTRL] and not self.already_pressed:
			self.tile_y+=1
			if self.tile_y>=self.tileManager.image.get_height()/16:
				self.tile_y=0
			self.already_pressed=True
		
		if not key.get_pressed()[K_LCTRL]:
			self.already_pressed=False
		if not key.get_pressed()[K_RCTRL]:
			self.already_pressed=False

		self.unit_rect=(self.scale_factor*self.tile_x,self.scale_factor*self.tile_y,self.scale_factor,self.scale_factor)
		texture=self.tileManager.crop(self.unit_rect)
		texture=pg.transform.scale(texture,(32,32))
		return texture


	def change_map_tile(self,level):
		tiles=level.tiles
		if mouse.get_pressed()[0]:
			xx=int(self.x/32)
			yy=int(self.y/32)
			tiles[yy][xx].texture=self.get_next_tile()

	def save(self,file_name,level_data):
		file=open("%s.txt" % file_name,'w')
		str1 = ''.join(str(e) for e in level_data)
		file.write(str1)
		file.close()

	def update(self,level):
		self.x,self.y=mouse.get_pos()
		self.change_map_tile(level)

	def render(self,display):
		texture=pg.transform.scale(self.get_next_tile(),(32,32))
		display.blit(texture,(self.x,self.y))
		# draw.rect(display,(100,100,100),(self.x,self.y,32,32))