
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
	def __init__(self,tile_x,tile_y,source_rect,ASSETS,solid=False):
		self.texture=ASSETS.crop(source_rect)
		self.texture.set_colorkey(BLACK)
		self.tempRect=self.texture.get_rect()
		self.size=32
		self.x=tile_x*self.size
		self.y=tile_y*self.size
		self.solid=solid
		self.bounds=Rect(self.x,self.y,self.size,self.size)



	def render(self,display,off):
		x0=self.x
		y0=self.y
		x1=x0+self.size/2
		y1=y0+self.size/2

		display.blit(self.texture,(x0-off[0],y0-off[1]))
		display.blit(self.texture,(x1-off[0],y0-off[1]))
		display.blit(self.texture,(x1-off[0],y1-off[1]))
		display.blit(self.texture,(x0-off[0],y1-off[1]))



	

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

	# def check_collision_entities(self):
	# 	for i1,e1 in enumerate(self.entities):
	# 		for i2,e2 in enumerate(self.entities):
	# 			if e1==e2:
	# 				continue
	# 			e1.checkCollision(move_x,move_y,entity.bounds):


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
				tiles[y][x]=Tile(x,y,(16*4,16*2,16,16),self.tileManager)

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
