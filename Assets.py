import pygame as pg


class AssetsManager:
	def __init__(self,path):
		self.image=pg.image.load(path);
		self.image.set_colorkey((0,0,0))

	def show(self,screen):
		screen.blit(self.image,(100,100))
	
	""" returns cropped image as surface"""
	def crop(self,rect):
		x=rect[0]
		y=rect[1]
		w=rect[2]
		h=rect[3]
		return self.image.subsurface(pg.Rect(x,y,w,h))
