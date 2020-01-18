# -*- coding: utf-8 -*-

#Note: pyHook only support win32
#import pyHook  
import random, time, sys

class game2048():
	"""docstring for Game2048"""
	def __init__(self, row_col_num):
		self.row_num = row_col_num
		self.col_num = row_col_num
		self.score = 0
		self.alive = True

		self.rand_data = [2, 4]
		self.grid_data = [ [0 for i in range(0, row_col_num)] for i in range(0, row_col_num) ]

	def _transit_matrix_(self, matrix_list):
		self.grid_data = [ [row[x] for row in matrix_list] for x in range(len(matrix_list[0])) ]

	def _move_oneline_(self, grid_line):
		move_flag = False		
		#how many numbers > 0 in this line 
		if (len(grid_line)-grid_line.count(0)==0):
			return move_flag, grid_line
		y=0
		list_line = [0 for x in range(len(grid_line))] 		
		for x in range(0, len(grid_line)):
			if (grid_line[x]>0):
				list_line[y]=grid_line[x]  #get all the non-zero numbers	
				y=y+1

		for x in range(0, len(list_line)-1):
			if (list_line[x]==list_line[x+1]):
				list_line[x] = 2*list_line[x+1]	 #merge one grid to left				
				for y in range(x+1, len(list_line)-1):
					list_line[y]=list_line[y+1]  #move left grids to left
				list_line[len(list_line)-1] = 0  #update the last grid to blank

		if (list_line!=grid_line):  #list contents changed after moving
			move_flag = True

		return move_flag, list_line

	def reset_game(self):
		self.score = 0
		self.alive = True

		self.grid_data = [ [0 for i in range(0, self.row_num)] for i in range(0, self.col_num) ]

	def get_status(self):
		list_grid = sum(self.grid_data, [])
		list_grid.sort(reverse=True)
		self.score = list_grid[0]  #get the maximum value

		line_len=len(self.grid_data)
		list_grid.sort(reverse=False) 
		if list_grid[0] > 0: #grids are full, no empty grid to fill
			self.alive = False
			for x in range(0, line_len):
				for y in range(0, line_len-1):
					#compare grids next to each other on the same line
					if(self.grid_data[x][y]==self.grid_data[x][y+1]):
						self.alive=True
					#compare grids next to each other on the same coloum
					if(x<line_len-1):
						if (self.grid_data[x][y]==self.grid_data[x+1][y]):
							self.alive=True
						#compare grids on the last coloum
						if (y==line_len-2) and (self.grid_data[x][y+1]==self.grid_data[x+1][y+1]):
							self.alive=True
					if self.alive :
						break	

	def fill_onegrid(self):
		zero_grid_pos = []
		for x in range(0,self.row_num):
			for y in range(0,self.col_num):
				if (self.grid_data[x][y]==0):
					zero_grid_pos.append((x,y))

		self.fill_data = random.choice(self.rand_data)
		if len(zero_grid_pos)>0:
			self.fill_pos = random.choice(zero_grid_pos)
			self.grid_data[self.fill_pos[0]] [self.fill_pos[1]] = self.fill_data


	def move_left(self):
		move_flags=[True for i in range(0,self.row_num)]
		for x in range(0, self.row_num):
			move_flags[x], self.grid_data[x] = self._move_oneline_(self.grid_data[x])
			
		return (move_flags.count(True)>0)

	def move_right(self):
		move_flags=[True for i in range(0,self.row_num)]
		for x in range(0, self.row_num):
			self.grid_data[x].reverse()
			move_flags[x], self.grid_data[x] = self._move_oneline_(self.grid_data[x])
			self.grid_data[x].reverse()

		return (move_flags.count(True)>0)

	def move_up(self):
		self._transit_matrix_(self.grid_data)
		move_flag = self.move_left()
		self._transit_matrix_(self.grid_data)
		return move_flag

	def move_down(self):
		self._transit_matrix_(self.grid_data)
		move_flag = self.move_right()
		self._transit_matrix_(self.grid_data)
		return move_flag

	#for run in IDEL
	def _show_panel_(self):
		self.get_status()
		print ("========Game 2048========")
		print ("Today's ScoreBoard: ", self.score)
		print ("=========================")
		for x in range(0, self.row_num):
			for y in range(0, self.col_num):
				print(str(self.grid_data[x][y]), end="\t")
			print("")

		print ("========================")
		print ()

	#monitor keys with pyHook in IDLE
	def _monitor_func_(self, key_pressed):
		key_down = key_pressed.Key 

		if (key_down=="F6"):
			self.reset_game()

		elif (key_down=="Escape"):
			sys.exit()

		elif (key_down=="Left"):
			self.move_left()
			self.fill_onegrid()			
			self._show_panel_()
			
		elif (key_down=="Right"):
			self.move_right()
			self.fill_onegrid()
			self._show_panel_()			

		elif (key_down=="Up"):
			self.move_up()
			self.fill_onegrid()			
			self._show_panel_()

		elif (key_down=="Down"):
			self.move_down()
			self.fill_onegrid()
			self._show_panel_()

		return True
			
	#for run in IDLE
	def _start_game_(self):
		print ("Use Left, Right, Up, Down arrow keys to play.")

		self.fill_onegrid()
		self._show_panel_()

		hook=pyHook.HookManager()
		hook.KeyDown=self._monitor_func_
		hook.HookKeyboard()

# On windows:
# use pip to install pyhook for supporting key monitor in IDLE
# then uncomment the pyhook import line at the beginning
# Press "F5" to run it in IDLE without pygame
if __name__=="__main__":
	game = game2048(4)
	game._start_game_()

