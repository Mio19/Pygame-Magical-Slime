import pygame
from Screen_map import Game_map
import Global_var as gv
from Draw import Draw,Music

class Mouse_click_screen:
    """This Class is used for the interaction between the mouse and the game interface"""
    def __init__(self,info_lst):
        map_dict=gv.get_dict('map_dict')
        self.show_flag=True
        self.image=pygame.image.load('pic/'+info_lst[0]).convert_alpha()
        self.text=[]
        self.key=''
        self.event_map=map_dict[info_lst[1]] # Get event list
        self.game_main=gv.get_dict('game_main')
        
    def show(self):
        Draw.draw_mouse_screen(self.game_main.screen,self.image)
        
    def tshow(self):
        T_POSITION=(140,160)
        Draw.draw_str(self.game_main.screen,''.join(self.text),T_POSITION) 
        
    def mouse_check(self):
        if self.show_flag:
            self.show()
            if self.text !=[]: # When the text is not empty, display it
                self.tshow()
            
    def set_mouse_screen(self,info_lst):# Set the mouse interface
        map_dict=gv.get_dict('map_dict')
        
        self.image=pygame.image.load('pic/'+info_lst[0]).convert_alpha()
        self.show_flag=True
        self.event_map=map_dict[info_lst[1]]
        self.key=info_lst[2]
        self.commend=info_lst[3]
        
    def check_event(self,position):# Check the task number of the current click position
        event='none'
        if self.event_map!=[]:
            new_position=Game_map.check_grid(position,0)
            event=self.event_map[new_position[0]][new_position[1]]
        return event    
    
    def do_event(self,position):# Perform different mouse click tasks according to the event number
        map1=gv.get_dict('map')
        task_door_dict=gv.get_dict('task_door_dict')
        door_open_dict=gv.get_dict('door_open_dict')
        dialog1=gv.get_dict('dialog1')
        task_dict=gv.get_dict('task_dict')
        player1=gv.get_dict('player')
        
        
        event=self.check_event(position) # Get the number of the current click position event
        
        if event !='none' and event != 0:
            if event ==-1: #close the interface
                self.show_flag=False
                self.text=[]
                      
            elif type(event)==int and event>=61 and event<=64:# Switch interface
                self.set_mouse_screen(task_dict[str(event)])
                Music.play_music(['click.wav',0,1])
                
            elif event==60:
                # Start the game
                gv.fresh_dict() 
                self.show_flag=False
                self.event_map=[]
                self.game_main.fresh_sreen(task_dict[str(event)][0])
                map1.fresh_map(self.game_main,task_dict[str(event)][2])
                player1.fresh_player(task_dict[str(event)][1]) 
                dialog1.set_dialog(task_dict[task_dict[str(event)][3]])
                player1.heart=3
                Music.bgm.stop()
                Music.play_music(['click.wav',0,1])
                Music.play_music(task_dict[str(event)][4])
                
            elif event==11:# Password lock interface-delete
                if len(self.text)>=1:
                    self.text.pop()# pop delete the last input number
                Music.play_music(['key.wav',0,1])   
                
            elif event==12: # Password lock interface-submit answer
                if ''.join(self.text)==self.key:# Use .join to connect the input answers
                    self.show_flag=False
                    self.text=[]
                    self.game_main.fresh_sreen(self.commend)
                    map1.fresh_map(self.game_main,'1')                 
                    open_index=task_door_dict[self.commend]
                    door_open_dict[open_index]=1
                    Music.play_music(['unlock.wav',0,1])
                else:
                    self.text=[]
                    Music.play_music(['error.wav',0,1])
                
            elif (type(event)==int and (event>=1 and event<=10) )or (event>='A' and event<='Z'):
                # Password lock interface-typing
                if (type(event)==int and event==10):
                    event=0
                if len(self.text)<=10:
                    self.text.append(str(event))
                Music.play_music(['key.wav',0,1])
            
                
                    
                    
                