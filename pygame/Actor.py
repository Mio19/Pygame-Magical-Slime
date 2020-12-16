import pygame
import Global_var as gv
from Draw import Draw,Music

class Actor:
    """
    Actor class is the parent class to the Player and Monster
    It contains basic functions of show and move.
    """
    
    def show(self): 
        game_main = gv.get_dict('game_main') # Get the game_main object that stored in Global_var
        
        ''' Call draw_image in the Draw class to draw the specific area of self.image
            (defined by the last four parameters) at the position of self.position
        '''
        Draw.draw_image(game_main.screen, self.image, self.position, self.pic_index, self.direction,self.image_x,self.image_y)

    def move(self):
        dialog1=gv.get_dict('dialog1')
        mouse_click_screen1=gv.get_dict('mouse_click_screen1')
        map1=gv.get_dict('map')

        ''' check whether the dialog box exists or not, and whether to interact with the mouse, or not
            if neither, move the character
        '''
        if dialog1.flag==False and mouse_click_screen1.show_flag==False:
            target_p1=self.position.move([5*i for i in self.speed]) # Functional Programming taught in lessons
            target_p2=self.position.move(self.speed) 
    
            if not map1.check_position(list(target_p1)):# can not walk forward
                self.target_position=self.position
                          
            else:# can go ahead
                self.position=target_p2
                self.pic_index = (self.pic_index+1)%3#use % operation to choose 3 different images of the character to realize the dynamic effect.
        self.show()  
            
   
class Player(Actor):

    def __init__(self,namelist,image_x,image_y,x=0,y=0):
        self.namelist=namelist # namelist = ['player.png','fight.png']
        self.image=pygame.image.load('pic/'+self.namelist[0]).convert_alpha()
        self.position=self.image.get_rect(center=(x,y))
        self.speed=[0,0] # speed[0]:pixel length in x axis for every step speed[1]:pixel length in y axis for every step
        self.direction=0 # set the front face of the character in the play.png picture
        self.pic_index=1 # Get the character in the second column of the play.png picture
        self.target_position=self.position # Used to determine whether the player needs to stop
        self.attack_index=0 # Value:0-6; 0:not acttck; 1-6: acttck
        self.image_x=image_x # 50, the width of the character
        self.image_y=image_y # 50,the height of the character
        self.show_flag=True # check whether the player is alive or not
        self.heart=3# Set the player's health to 3
        
    def fresh_player(self,position):
        self.show_flag=True
        self.position=self.image.get_rect(center=position)
        self.speed=[0,0]
        self.target_position=self.position
        
        
    def big_move(self,speed_number):#Move speed_number*speed
        new_speed=[speed_number*i for i in self.speed]
        self.target_position=self.position.move(new_speed)
    
    def actor_check(self):#Check player status at any time
        mouse_click_screen1=gv.get_dict('mouse_click_screen1')
        task_dict=gv.get_dict('task_dict')
        
        if self.show_flag and self.heart>0:# when player alive, moving
            if self.target_position!=self.position:
                self.move()
            else:
                if self.attack_index==0: # when not attack, showing player.png
                    self.image=pygame.image.load('pic/'+self.namelist[0]).convert_alpha()
                    self.pic_index=1
                    
                else:
                    self.attack()
                self.show()
                
        elif self.heart<=0:# player died
            self.show_flag=False # stop showing player
            self.heart=3 #reset life value
            mouse_click_screen1.set_mouse_screen(task_dict['51']) #change to end page
            Music.bgm.stop()
            Music.play_music(['gameover.wav',0,1])
        
        self.draw_heart()
     
    def draw_heart(self):# drawing life bar
        game_main=gv.get_dict('game_main')
        HEART_IMAGE='heart_bar.png'
        HEART_POSITION=(54,0)# setting life bar postion
        HEART_SIZE=50# setting heart image size
        image=pygame.image.load('pic/'+HEART_IMAGE).convert_alpha()
        Draw.draw_image(game_main.screen, image, HEART_POSITION, 0, 1, HEART_SIZE*3, HEART_SIZE)# drawing black hearts
        Draw.draw_image(game_main.screen, image, HEART_POSITION, 0, 0, HEART_SIZE*self.heart, HEART_SIZE)# drawing red hearts according life value
        
    def attack(self):
        self.image=pygame.image.load('pic/'+self.namelist[1]).convert_alpha()
        self.pic_index = (self.attack_index-1)//2 #setting the image_index in fight.png to change frame
        self.attack_index -=1
        
    def big_attack(self):# 6 frames are played for each attack
        self.attack_index=6
        Music.play_music(["shoot.wav",0,0.5])
     
class Monster(Actor):

    def __init__(self,x,y,target,namelist,image_x,image_y):
        self.namelist=namelist
        self.image=pygame.image.load('pic/'+self.namelist[0]).convert_alpha()
        self.position=self.image.get_rect(center=(x,y))
        self.speed=[0,0]
        self.direction=0
        self.pic_index=1# Get image index
        self.target=target
        self.target_position=target.position
        self.show_flag=True
        self.attack=-1 # The monster is wriggling
        self.image_x=image_y
        self.image_y=image_x
        
    def actor_check(self):
        monster_list1=gv.get_dict('monster_list1')
        map1=gv.get_dict('map')
        door_open_dict=gv.get_dict('door_open_dict')# Get the status of whether the door is open or not
        
        if self.show_flag :# check if the slime is still alive
            if self.attack==-1 and self.target.show_flag:#Determine whether it self-boom state vaule= -1 did not boom.
                self.target_position=self.target.position # Obtain the player's coordinates as the destination
                # Calculate the distance between the monster and the player
                s,x,y=Monster.cal_distance(self.position.left,self.target.position.left,self.position.top,self.target.position.top)
                self.self_target_distance=s  
                if s>=30:   
                    #Determine whether the position is the same as the player's position, if different, move towards the player's direction
                    self.get_speed(s,x,y)
                    self.move()
                else:
                    #Same as the player's position, became self-destruction
                    self.boom()
                    self.show()
               
            else:
                # self-destruction
                self.pic_index = (self.attack)//10
                self.attack +=1 # Run the image of each frame
                self.show()
                if self.attack==50:#finished self-destruction
                    self.show_flag=False# slime is died
                    if not monster_list1.check_alive() and map1.relate_key!='last':# when all mosters are died, and dont in the last map.
                        door_open_dict[map1.relate_key]=1 # open the door

    def boom(self):
        BOOM_DISTANCE=80 #The explosion has a range of 80
        if self.self_target_distance<=BOOM_DISTANCE:# if palyer are within the exploded shot, lose one life
            self.target.heart -= 1
            Music.play_music(["hurt.wav",0,1])
        self.image=pygame.image.load('pic/'+self.namelist[1]).convert_alpha()
        self.image_x=60
        self.image_y=64
        self.attack=0
        self.direction=0
        self.pic_index=0
        Music.play_music(["boom.wav",0,0.5])
        
    def get_speed(self,s,x,y):#Set the speed of up and down and left and right
        # according to the cosine and sine values of the angle of the player and the monster
        if s>=1:
            new_speed_x=-x/s*1.5 
            new_speed_y=-y/s*1.5
        else:
            new_speed_x=-x
            new_speed_y=-y
        self.speed=[new_speed_x,new_speed_y]
        
    def cal_distance(p1,p2,p3,p4): # Use the Pythagorean Theorem to calculate the distance between player and a monster
        x=p1-p2
        y=p3-p4
        s=(x**2+y**2)**(0.5)
        return s,x,y
        





