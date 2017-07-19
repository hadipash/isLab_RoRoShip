# -*- coding: utf-8 -*-

import sys
import math
import time

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from draw_lib import *
from global_Data import *
#from layout import *

class window:
	def __init__(self, width = 480, height = 320, caption = 'simulation'):
		pygame.init()
		self.width = width
		self.height = height


		self.dash_size = 10
		self.scr_H = height * self.dash_size
		self.scr_W = width * self.dash_size
		self.path = []
		self.isLoaded = []
		self.cnt = 0
		'''
		self.scr_H = space.height * dash_size
		self.scr_W = space.width * dash_size
		self.grid = np.ones(shape=(space.width, space.height))
		for x in range(space.width):
			for y in range(space.height):
				self.grid[x][y] = space.vertexArr[y][x].isOccupied()
		'''

		# 1) 화면 해상도를 480*320으로 초기화. 윈도우 모드, 더블 버퍼 모드로 초기화하는 경우
		self.screen = pygame.display.set_mode((self.scr_W, self.scr_H), DOUBLEBUF | OPENGL)
		pygame.display.set_caption(caption)  # 타이틀바의 텍스트를 설정

		self.TARGET_FPS = 60
		self.TIME_STEP = 1.0 / self.TARGET_FPS
 
		self.clock = pygame.time.Clock()
		self.running = True

		gl_set(self.scr_W, self.scr_H)

	def pathread(self,file_name):
		f = open(file_name, 'r')
		path = f.readlines()
		temp=[]
		for s in path:
			s = s.rstrip()
			s = s.split()
			s = [int(i) for i in s]
			if (len(s) == 4):
				self.path.append(temp)
				self.isLoaded.append(-1)
				temp = []
				self.cnt += 1
				continue
				#break
			temp.append(s)


	def display(self):
		screen = self.screen
		running = self.running
		dash_size = self.dash_size


		### gl veiw white clear ###
		glClearColor(1.0,1.0,1.0,1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


		### first setting ###
		f_cnt = 0
		cnt=0
		path = self.path[f_cnt]
		turn = -1
		straight = -1
		x = 0
		y = 0
		

		while running:
			for event in pygame.event.get():		
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					running = False #sys.exit()
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_a and ori == 0):
						x -= 1
					if (event.key == pygame.K_d and ori == 0):
						x += 1
					if (event.key == pygame.K_w and ori == 1):
						y -= 1
					if (event.key == pygame.K_s and ori == 1):
						y += 1
					if (event.key == pygame.K_e):
						y -= 1
					if (event.key == pygame.K_q):
						y += 1
			
			
			###  background white clear  ###
			glClearColor(1.0,1.0,1.0,1.0)
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			
			### enter ###
			glColor3ub(255,0,0)
			#draw(dash_size * 22, dash_size*0, 6*dash_size, 2*dash_size)
			#draw(dash_size * 0, dash_size*47, 2*dash_size, 6*dash_size)

			draw(dash_size * 10, dash_size * 12, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 12, 1*dash_size, 1*dash_size)
			draw(dash_size * 10, dash_size * 25, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 25, 1*dash_size, 1*dash_size)
			draw(dash_size * 10, dash_size * 37, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 37, 1*dash_size, 1*dash_size)

			draw(dash_size * 10, dash_size * 62, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 62, 1*dash_size, 1*dash_size)
			draw(dash_size * 10, dash_size * 75, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 75, 1*dash_size, 1*dash_size)
			draw(dash_size * 10, dash_size * 87, 1*dash_size, 1*dash_size)
			draw(dash_size * 39, dash_size * 87, 1*dash_size, 1*dash_size)

			glColor3ub(66,73,73)	#color set DEEP_GRAY
			
			###  draw grid   ###
			for _x in range(0,self.scr_W,dash_size):
				draw_line(_x,0,0, self.scr_H)

			for _y in range(0,self.scr_H,dash_size):
				draw_line(0,_y,self.scr_W,0)

				###  draw already loaded freight  ###

			for f in range(f_cnt):
				if (self.isLoaded[f]!= -1):
					_path = self.path[f]
					_width = _path[0][0]
					_height = _path[0][1]
					if(_path[1][2] == 0 or _path[1][2] == 2):
						draw(dash_size*_path[1][0],dash_size*_path[1][1],_width*dash_size,_height*dash_size)
						glColor3f(0,0,0)
						draw(dash_size*_path[1][0],dash_size*_path[1][1],_width*dash_size,1*dash_size)
					elif(_path[1][2] == 1):
						draw(dash_size*_path[1][0],dash_size*_path[1][1],_height*dash_size,_width*dash_size)
						glColor3f(0,0,0)
						draw(dash_size*(_path[1][0]+_height-1),dash_size*_path[1][1],1*dash_size,_width*dash_size)
					elif(_path[1][2] == 2):
						draw(dash_size*_path[1][0],dash_size*_path[1][1],_width*dash_size,_height*dash_size)
						glColor3f(0,0,0)
						draw(dash_size*_path[1][0],dash_size*(_path[1][1]+_height - 1),_width*dash_size,1*dash_size)
					elif(_path[1][2] == 3):
						draw(dash_size*_path[1][0],dash_size*_path[1][1],_height*dash_size,_width*dash_size)
						glColor3f(0,0,0)
						draw(dash_size*_path[1][0],dash_size*_path[1][1],1*dash_size,_width*dash_size)
					glColor3ub(66,73,73)

				###  draw already loaded freight  ###
			
			###  next freight width, height, path set  ###
			if(f_cnt < len(self.path) and cnt == 0):
				#if(f_cnt > 0):
				#	self.isLoaded[f_cnt-1] = 1
				path = self.path[f_cnt]
				width = path[0][0]
				height = path[0][1]
				bump = path[0][2]
				cnt = len(path)-1
				f_cnt += 1
			###  next freight width, height, path set  ###

			##	background save
			glPushMatrix() 	
			
			##	color set purple
			glColor3f(1.0,0.0,1.0)	
			
			if(cnt > 0):
				##	color set blue
				glColor3f(0.0,0.0,1.0)
				if (cnt != len(path)-1 and cnt != 0  and path[cnt][2] != path[cnt-1][2] and turn == -1 and straight == -1):
					## up
					if (path[cnt][2] == 0 and straight == -1):
						glColor3f(0.0,0.0,1.0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,1*dash_size)

					## right
					elif (path[cnt][2] == 1 and straight == -1):
						glColor3f(0.0,0.0,1.0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*(path[cnt][0]+height-1),dash_size*path[cnt][1],1*dash_size,width*dash_size)

					## down
					elif (path[cnt][2] == 2 and straight == -1):
						glColor3f(0.0,0.0,1.0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*(path[cnt][1]+height - 1),width*dash_size,1*dash_size)

					## left
					elif (path[cnt][2] == 3 and straight == -1):
						glColor3f(0.0,0.0,1.0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],1*dash_size,width*dash_size)
					
					#print "front turn ",path[cnt][2]," to ",path[cnt-1][2]
					glColor3f(1.0,0.0,1.0)
					turn = 1
					degree = 0
					#cnt += 1

				## do not need to turn
				if (turn == -1):
					## up
					if (path[cnt][2] == 0 and straight == -1):
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,1*dash_size)

					## right
					elif (path[cnt][2] == 1 and straight == -1):
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*(path[cnt][0]+height-1),dash_size*path[cnt][1],1*dash_size,width*dash_size)

					## down
					elif (path[cnt][2] == 2 and straight == -1):
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*(path[cnt][1]+height - 1),width*dash_size,1*dash_size)

					## left
					elif (path[cnt][2] == 3 and straight == -1):
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						glColor3f(1,0,0)
						draw(dash_size*path[cnt][0],dash_size*path[cnt][1],1*dash_size,width*dash_size)

					if (path[cnt][2] == path[cnt-1][2] and straight == -1):
						#glColor3ub(0, 255, 0)
						if(path[cnt][0] > path[cnt-1][0]):
							straight = 3 # right
							x = path[cnt][0]*dash_size
							y = path[cnt][1]*dash_size
						elif(path[cnt][0] < path[cnt-1][0]):
							straight = 1 # left
							x = path[cnt][0]*dash_size
							y = path[cnt][1]*dash_size
						elif(path[cnt][1] > path[cnt-1][1]):
							straight = 0 # up
							x = path[cnt][0]*dash_size
							y = path[cnt][1]*dash_size
						elif(path[cnt][1] < path[cnt-1][1]):
							straight =  2 # down
							x = path[cnt][0]*dash_size
							y = path[cnt][1]*dash_size


					glColor3ub(0, 255, 0)
					if (straight != -1):
						if (straight == 0):
							y -= dash_size
							draw(x,y,width*dash_size,height*dash_size)
						elif (straight == 1):
							x += dash_size
							draw(x,y,height*dash_size,width*dash_size)
						elif (straight == 2):
							y += dash_size
							draw(x,y,width*dash_size,height*dash_size)
						elif (straight == 3):
							x -= dash_size
							draw(x,y,height*dash_size,width*dash_size)
						#draw(x,y,height*dash_size,width*dash_size)
						#glColor3f(1,0,0)
						#draw(x,y,1*dash_size,width*dash_size)
						if (straight == 0 and y == path[cnt-1][1]*dash_size):
							straight = -1
							cnt -= 2
							x=0
							y=0
						elif (straight == 1 and x == path[cnt-1][0]*dash_size):
							straight = -1
							cnt -= 2
							x=0
							y=0
						elif (straight == 2 and y == path[cnt-1][1]*dash_size):
							straight = -1
							cnt -= 2
							x=0
							y=0
						elif (straight == 3 and x == path[cnt-1][0]*dash_size):
							straight = -1
							cnt -= 2
							x=0
							y=0
					

				##	need to turn
				if (cnt != len(path)-1 and cnt != 0  and path[cnt][2] != path[cnt+1][2] and turn == -1 and straight == -1):
					#print "turn ",path[cnt+1][2]," to ",path[cnt][2]
					glColor3f(1.0,0.0,1.0)
					turn = 1
					degree = 0
					cnt += 1
				
				if (turn == 1): ## from (cnt) to (cnt -1)
					time.sleep(0.05)
					##	color set deep gray
					glColor3ub(66,73,73)
					center_x = 0
					center_y = 0
					set_dgr = 90

					## up
					if (path[cnt][2] == 0):
						## up right
						if (path[cnt-1][2] == 1 and path[cnt][0] < path[cnt-1][0]):
							set_dgr = 90
							#print "UR"
							#glColor3ub(255,0,0)
							center_x = path[cnt-1][0] + bump;
							center_y = path[cnt][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## up left
						elif (path[cnt-1][2] == 3 and path[cnt][0] > path[cnt-1][0]):
							set_dgr = -90
							#print "UL"
							center_x = path[cnt-1][0] + height - bump;
							center_y = path[cnt][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## down left
						elif (path[cnt-1][2] == 1):
							set_dgr = 90
							#print "DL"
							center_x = path[cnt-1][0] + height - bump;
							center_y = path[cnt][1] + bump;
							#glColor3f(1.0,0.0,1.0)
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## down right
						elif (path[cnt-1][2] == 3):
							set_dgr = -90
							#print "DR"
							center_x = path[cnt-1][0] + bump;
							center_y = path[cnt][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)

					## right
					elif (path[cnt][2] == 1):

						## right up
						if (path[cnt-1][2] == 0 and path[cnt][1] > path[cnt-1][1]):
							set_dgr = -90
							#print "RU"
							center_x = path[cnt][0] + bump;
							center_y = path[cnt-1][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## right down
						elif (path[cnt-1][2] == 2 and path[cnt][0] < path[cnt-1][0]):
							set_dgr = 90
							#print "RD"
							center_x = path[cnt][0] + bump;
							center_y = path[cnt-1][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## left up
						elif (path[cnt-1][2] == 2):
							set_dgr = 90
							#print "LU"
							center_x = path[cnt][0] + height - bump;
							center_y = path[cnt-1][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## left down
						elif (path[cnt-1][2] == 0):
							set_dgr = -90
							#print "LD"
							center_x = path[cnt][0] + height - bump;
							center_y = path[cnt-1][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)

					## down
					elif (path[cnt][2] == 2):

						## up right
						if (path[cnt-1][2] == 3 and path[cnt][0] < path[cnt-1][0]):
							set_dgr = 90
							#print "UR"
							center_x = path[cnt-1][0] + bump;
							center_y = path[cnt][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## up left
						elif (path[cnt-1][2] == 1 and path[cnt][0] > path[cnt-1][0]):
							set_dgr = -90
							#print "UL"
							center_x = path[cnt-1][0] + height - bump;
							center_y = path[cnt][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## down left
						elif (path[cnt-1][2] == 3):
							set_dgr = 90
							#print "DL"
							center_x = path[cnt-1][0] + height - bump;
							center_y = path[cnt][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)
						## down right
						elif (path[cnt-1][2] == 1):
							#print "DR"
							set_dgr = -90
							center_x = path[cnt-1][0] + bump;
							center_y = path[cnt][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],width*dash_size,height*dash_size)

					## left
					elif (path[cnt][2] == 3):
						## right up
						if (path[cnt-1][2] == 2 and path[cnt][1] > path[cnt-1][1]):
							set_dgr = -90
							#print "RU"
							center_x = path[cnt][0] + bump;
							center_y = path[cnt-1][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## right down
						elif (path[cnt-1][2] == 0 and path[cnt][0] < path[cnt-1][0]):
							set_dgr = 90
							#print "RD"
							center_x = path[cnt][0] + bump;
							center_y = path[cnt-1][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## left up
						elif (path[cnt-1][2] == 0):
							set_dgr = 90
							#print "LU"
							center_x = path[cnt][0] + height - bump;
							center_y = path[cnt-1][1] + height - bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)
						## left down
						elif (path[cnt-1][2] == 2):
							set_dgr = -90
							#print "LD"
							center_x = path[cnt][0] + height - bump;
							center_y = path[cnt-1][1] + bump;
							degree = draw_rotate(dash_size*center_x,dash_size*center_y,degree,set_dgr,dash_size*path[cnt][0],dash_size*path[cnt][1],height*dash_size,width*dash_size)

					###   turning end	###
					if(degree == set_dgr):
						rotate(dash_size*center_x,dash_size*center_y, -degree)
						degree = 0
						set_dgr = 90
						turn = -1
						cnt -= 1
						if (cnt == 1):
							cnt-=1


			if (cnt == 0 and ( path[cnt+1][2] == 0 or path[cnt+1][2] == 2)):
				glColor3ub(66,73,73)
				draw(dash_size*path[cnt+1][0],dash_size*path[cnt+1][1],width*dash_size,height*dash_size)
				self.isLoaded[f_cnt-1] = 1

			elif(cnt == 0):
				glColor3ub(66,73,73)
				draw(dash_size*path[cnt+1][0],dash_size*path[cnt+1][1],height*dash_size,width*dash_size)
				self.isLoaded[f_cnt-1] = 1

			glPopMatrix()

			global enter_info
			
			self.clock.tick(self.TARGET_FPS)
			pygame.display.flip() 	##	screen update
			pygame.time.delay(leftInFrame())

			#running = False
			#event = pygame.event.wait()
			#break
		print('Done!')
		pygame.quit()
		
def main():
	py = window(50,100)
	py.pathread("path_list")
	py.display()
	

if __name__ == "__main__":
    main()
