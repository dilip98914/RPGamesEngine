
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
from entities import *

class Camera:
	def __init__(self):
		self.offset_x=0
		self.offset_y=0
		
	def update(self,player):
		x=player.x
		y=player.y
		delta_x=x-ORIGIN[0]
		delta_y=y-ORIGIN[1]
		self.offset_x=delta_x
		self.offset_y=delta_y



class Tile:
	def __init__(self,tile_x,tile_y,color,solid=False):
		self.size=32
		self.x=tile_x*self.size
		self.y=tile_y*self.size
		self.color=color
		self.solid=solid

	def render(self,display,off):
		bounds=Rect(self.x-off[0],self.y-off[1],self.size,self.size)
		draw.rect(display,self.color,bounds)
		draw.rect(display,(0,0,0),bounds,1)

	

class Level:
	def __init__(self,tileWidth,tileHeight):
		self.w=tileWidth
		self.h=tileHeight
		self.tiles=self.createTiles()
		self.camera=Camera()
		self.entities=self.createEntities(15)

	def createEntities(self,len):
		entities=[0]*len
		entities[0]=Player(9,8,LIGHT_YELLOW)
		entities[1]=Mob(10,10,WHITE)
		for x in range(2,len):
			xx=randrange(int(WIDTH/32))
			yy=randrange(int(HEIGHT/32))
			entities[x]=Entity(xx,yy,PINK)
		return entities


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
				tiles[y][x]=Tile(x,y,LIGHT_GREEN)

		return tiles

	def update(self):
		self.camera.update(self.entities[0])
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
