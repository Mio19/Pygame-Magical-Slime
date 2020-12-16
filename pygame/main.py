import pygame
import os
import Global_var as gv
from Screen_map import Game_set,Game_map
from Actor import Player  
from Monsterlist import Monster_list  
from Dialog import Dialog
from Mouse import Mouse_click_screen
from Draw import Music
from Bullet import Bullet_group

'''
Source of Pictures
The player and map pictures (fight.png, floor0.png, floor1.png, floorb2a.png,
floob2b.png, icon.png, monster.png player.png room.png) are made by RPG Maker MV. 
(A game make application, be sold in Steam, images are allowed to used in buyer’s games.)
All the remaining pictures are made by Photoshop.

Source of Music
All music are purchased from this link:
https://item.taobao.com/item.htm?spm=a1z0k.6846577.0.0.6e8b6697EctbJq&id=625407827665&_u=t2dmg8j26111
Copyright allowed to be used

'''


# Initial values
SCREEN_SIZE=(1350, 810)
SCREEN_IMAGE='room.png'
TITLE='Magical Slime'
MAP_RELATE='1'# Initial room puzzle index
PLAYER_IMAGE=[['player.png','fight.png'],50,50]
MOUSE_MODE_INIT=['title.png','start']
MUSIC_INIT=['start.wav',1,1]
TIME=60 # Calling the pygame.time.clock.tick function TIME times per second
SPEED=5
MOVE_TIMES=3 # Movement of SPEED*MOVE_TIMES pixels for every time pressing keyboard

pygame.init()

# Import the Game_set class, create an instance object of the class Game_set, and store it in the game_main variable
game_main=Game_set(SCREEN_SIZE,SCREEN_IMAGE,TITLE)
# Putting the created instance object into the Global_var file so that classes in other files can be called at any time
gv.put_dict('game_main',game_main)

map1=Game_map(game_main,MAP_RELATE)
gv.put_dict('map',map1)
player1=Player(PLAYER_IMAGE[0],PLAYER_IMAGE[1],PLAYER_IMAGE[2])
gv.put_dict('player',player1)
monster_list1=Monster_list()
gv.put_dict('monster_list1',monster_list1)
bullet_group1=Bullet_group()
gv.put_dict('bullet_group1',bullet_group1)
dialog1=Dialog()
gv.put_dict('dialog1',dialog1)
mouse_click_screen1=Mouse_click_screen(MOUSE_MODE_INIT)
gv.put_dict('mouse_click_screen1',mouse_click_screen1)

clock=pygame.time.Clock()# Track running events
Music.play_music(MUSIC_INIT)#Initializing music playback


while(True):
    clock.tick(TIME)# Refresh setting
    # Monitor keyboard and mouse events
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    # keyboard
    ''' key_pressed = pygame.key.get_pressed()
        Inspiration code: (Chinese) https://www.matools.com/blog/190696937 In the end of website
        If we press the keyboard once to move forward a little, the game becomes difficult to play. 
        To get the key that was pressed, we used the code which comes from the url above.'''
        
    if not mouse_click_screen1.show_flag and not dialog1.flag:
        if e.type==pygame.KEYDOWN:
            if e.key == pygame.K_e:# Shooting
                player1.big_attack()
                bullet_group1.play_shoot()
            elif e.key == pygame.K_f: 
                map1.check_task(player1.position)# Interactive function (check item,switch map)
                
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:# Turn left
            player1.speed=[-SPEED,0] # Obtain -SPEED value in left direction
            player1.direction=1# Set the character turn to the left
            player1.big_move(MOVE_TIMES) # Moving MOVE_TIMES*SPEED pixel
        elif key_pressed[pygame.K_d]:# Turn right
            player1.speed=[SPEED,0]
            player1.direction=2
            player1.big_move(MOVE_TIMES)
        elif key_pressed[pygame.K_w]:# Turn up
            player1.speed=[0,-SPEED]
            player1.direction=3
            player1.big_move(MOVE_TIMES)
        elif key_pressed[pygame.K_s]:# Turn down
            player1.speed=[0,SPEED]
            player1.direction=0
            player1.big_move(MOVE_TIMES)
 
    ''' Monitor mouse events module
        If dialog box is Showed, every time you click the mouse, the next one will be shown.
        If mouse_click_screen is showed, perform event according to click position '''
    if e.type==pygame.MOUSEBUTTONDOWN:
        if dialog1.flag:
            dialog1.show_next()  
        elif mouse_click_screen1.show_flag:
            mouse_click_screen1.do_event(e.pos)
    
    # Running all objects displayed on the screen and refreshing
    game_main.show_screen()
    player1.actor_check()
    monster_list1.check_monster_list()
    bullet_group1.check_bullet_list()
    mouse_click_screen1.mouse_check()
    dialog1.dialog_check()
    pygame.display.flip()

# Quiting the game
pygame.quit()
os._exit(0) # for Mac users