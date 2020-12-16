import pygame
import Global_var as gv
from Draw import Music

class Game_set:
    #This class is used to display background images
    def __init__(self,screen_size,roomname,gamecaption):
        self.screen_size=screen_size
        self.screen=pygame.display.set_mode(screen_size)
        pygame.display.set_caption(gamecaption)
        self.fresh_sreen(roomname)# Refresh the game background
    
    def show_screen(self):
        SCREEN_POSITION=(0,0)
        self.screen.blit(self.background,SCREEN_POSITION)
        
    def fresh_sreen(self,roomname):# Refresh the game background
        self.roomname=roomname
        self.background = pygame.image.load('pic/'+self.roomname).convert()
        

class Game_map:
    """ The class is used to obtain the active area and obstacle area in the map, 
        and to obtain the number of the task area in the map;
        And divide each picture into 25*15 grids, each grid has corresponding attributes
        This idea is borrowed from link: class GameMap(Array2D) Line 51 code.
        https://github.com/zxf20180725/pygame-jxzj/blob/master/04_1_%E4%BA%BA%E7%89%A9%E8%A1%8C%E8%B5%B0_%E5%9C%B0%E5%9B%BE%E8%AE%BE%E8%AE%A1/jxzj/core.py
        
        We only learned about the idea of class Array2D, but did not copy any code.
    """
    GRID_PIXEL=25
    #the offset value between topleft and center coordinates of the rectangle because the rectangle is drawn in the center place but shown in topleft position
    GRID_SIZE=[25,15]# The grid numbers of width and heigth of the 2D grid
    
    def __init__(self,game_main,relate_key,door_open=0):
        self.fresh_map(game_main,relate_key)# relate_key: Define whether the door of the current map is opened
        
    def check_grid(position,pixel):# Returns the coordinate value of the grid according to the original coordinate value
        Game_map.game_main=gv.get_dict('game_main')

        new_position=[0,0]
        # change pixel coordinates to grid coordinates
        new_position[1]=int((position[0]+pixel)//(Game_map.game_main.screen_size[0]/Game_map.GRID_SIZE[0]))
        new_position[0]=int((position[1]+pixel)//(Game_map.game_main.screen_size[1]/Game_map.GRID_SIZE[1]))
        return new_position
           
    def check_position(self,position):# check whether the current position can continue to walk or not
        
        new_position=Game_map.check_grid(position,Game_map.GRID_PIXEL)
        # If the character is outside the boundary, they cannot walk
        if new_position[0]<0 or new_position[0]>Game_map.GRID_SIZE[1]-1 or new_position[1]<0 or new_position[1]> Game_map.GRID_SIZE[0]-1:
            return 0
        # Inside the boundary, the corresponding grid coordinates are returned
        return self.map[new_position[0]][new_position[1]]
    
    def fresh_map(self,game_main,key):
        map_dict=gv.get_dict('map_dict')
        self.map_name=game_main.roomname
        self.map=map_dict[self.map_name]
        self.tmap=map_dict[self.map_name+'t']
        self.relate_key=key

        
    def check_task(self,position):# Execute task by task coordinates
        new_position=Game_map.check_grid(position,Game_map.GRID_PIXEL)
        task=self.tmap[new_position[0]][new_position[1]]# Get the grid task number of the current grid position
        # Obtain various dictionary values
        task_dict=gv.get_dict('task_dict')
        door_open_dict=gv.get_dict('door_open_dict')# Judgment this map lead to the next map
        task_door_dict=gv.get_dict('task_door_dict')
        dialog1=gv.get_dict('dialog1')
        monster_list1=gv.get_dict('monster_list1')
        mouse_click_screen1=gv.get_dict('mouse_click_screen1') 
        player1=gv.get_dict('player')
        
        if task>=1 and task<=10:# Switch map
            if door_open_dict[str(task)] and not monster_list1.check_alive():
                # Check whether the current map task is completed and whether the map is created by the remaining slimes
                relate_key=task_dict[str(task)][3] # The index of the door that would be opened in the current room puzzle
                if task==5 or task==8:
                    ''' According to whether the puzzle of the room to be entered has been solved,
                        switch to different open room '''
                    if door_open_dict[relate_key]==1: 
                        task +=1
                # Refresh objects
                Game_map.game_main.fresh_sreen(task_dict[str(task)][0])
                self.fresh_map(Game_map.game_main,relate_key)
                player1.fresh_player(task_dict[str(task)][1])
                Music.bgm.stop()
                Music.play_music(task_dict[str(task)][5])
                
                if door_open_dict[relate_key]==0:
                    # check whether the puzzle is solved or not to determine to generate monsters or not.
                    monster_list1.fresh_monster(task_dict[str(task)][2])
                    if task_dict[str(task)][4]!='none':
                        dialog1.set_dialog(task_dict[task_dict[str(task)][4]])
                                    
            else:# Prompt when the map cannot be switched
                dialog1.set_dialog(task_dict['door'])
            
        elif task>=11 and task <35:# Show the dialogue when check items
            if str(task) in task_door_dict.keys():
                open_index=task_door_dict[str(task)]
                door_open_dict[open_index]=1
        
            if not dialog1.flag:# Determine if the dialogue has been displayed
                dialog1.set_dialog(task_dict[str(task)])
            else:# Close the dialog 
                dialog1.text=''
                dialog1.index=0
                dialog1.flag= not dialog1.flag
            if task==19:# Eat fish to reset health
                player1.heart=3
                
        elif task>=35 and task<50:# Show notes
            mouse_click_screen1.set_mouse_screen(task_dict[str(task)])  
            Music.play_music(['paper.wav',0,1])
        
        elif task==50:# Win
            mouse_click_screen1.set_mouse_screen(task_dict[str(task)][0]) 
            dialog1.set_dialog(task_dict[str(task)][1])
            Music.bgm.stop()
            Music.play_music(['win.wav',0,1])