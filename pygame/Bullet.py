import pygame
import Global_var as gv
from Draw import Draw
from Actor import Monster


class Bullet_group:
    """This type of storage for bullets"""
    def __init__(self):
        self.blst=[] # Set empty bullet list
    def add_bullet(self,image,position,speed,direction):
        new_bullet=Bullet(image,position,speed,direction)
        self.blst.append(new_bullet)
    def check_bullet_list(self):
        for i in self.blst:
            if i.flag:
                i.check_position()
                i.move()
                
    def play_shoot(self):# When the player attacks
        player1=gv.get_dict('player') # Get the player object
        bullet_image='bullet.png'# Get bullet picture
        SPEED=5
        if player1.direction==0:# Player down
            b_position=(player1.position.center[0]-player1.image_x//3,player1.position.center[1])
            b_speed=[0,SPEED]
        elif player1.direction==1:# Player left
            b_position=(player1.position.center[0]-player1.image_x,player1.position.center[1]-player1.image_y//2)
            b_speed=[-SPEED,0]
        elif player1.direction==2:# Player  right
            b_position=(player1.position.center[0],player1.position.center[1]-player1.image_y//2)
            b_speed=[SPEED,0]
        elif player1.direction==3:# Player up
            b_position=(player1.position.center[0]-player1.image_x//3,player1.position.center[1]-player1.image_y)
            b_speed=[0,-SPEED]
        self.add_bullet(bullet_image,b_position,b_speed,player1.direction)# append new bullet object
        
    
class Bullet:
    """This class is used to define bullets"""
    def __init__(self,image,position,speed,direction):
        # iamge：Bullet pictures; postion：Bullet coordinates; speed：Bullet speed; direction: Bullet direction

        self.image=pygame.image.load('pic/'+image).convert_alpha()
        self.position=self.image.get_rect(center=position)
        self.speed=speed
        new_speed=[50*i for i in self.speed]# Functional programming is used here. The effective range of the bullet is 250 pixels.
        self.target_position=self.position.move(new_speed)# Set the effective range boundary
        self.direction=direction# Bullet direction
        self.flag=True # If the bullet exists, it is True
        self.pic_index=1
        self.image_x=34# Bullet size
        self.image_y=34
    
    def move(self): # Bullet move
        target_p=self.position.move(self.speed)
        if self.position!=self.target_position:# When the bullet does not exceed the effective range, showing the bullet
            self.pic_index =(self.pic_index+1)%3
            self.position=target_p
            self.show()
        else:# The bullet disappears after it exceeds the effective range
            self.flag=False
    def show(self):
        game_main=gv.get_dict('game_main')
        Draw.draw_image(game_main.screen, self.image, self.position, self.pic_index, self.direction,self.image_x,self.image_y)
        
    def check_position(self):
        BOOM_DISTANCE=30# Set the limited explosion range of the bullet
        monster_list1=gv.get_dict('monster_list1')
        for i in monster_list1.list:
            if i.show_flag and i.attack==-1:# When the monster is alive and wriggling, calculate the distance between the bullet and the monster
                s,x,y=Monster.cal_distance(self.position.center[0],i.position.center[0],self.position.center[1],i.position.center[1])
                if s<=BOOM_DISTANCE:# When the distance between the slime and the bullet is less than 30, the slime explodes and the bullet disappears
                    i.boom();
                    self.flag=False

                    
        