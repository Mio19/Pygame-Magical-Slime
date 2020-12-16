import pygame

class Draw:
    # This class is used to draw pictures, mouse, and character strings
    """ The draw_image function is borrowed from this link:
        https://github.com/zxf20180725/pygame-jxzj/blob/master/04_1_%E4%BA%BA%E7%89%A9%E8%A1%8C%E8%B5%B0_%E5%9C%B0%E5%9B%BE%E8%AE%BE%E8%AE%A1/jxzj/core.py
        draw function 10-24 lines
        We almost reference the function draw in class Sprite of this website.
        By using this function, we could choose a small area of a big picture which contains a lot of small pictures. 
        Of course, we understand how to use this function and the meaning of each parameter.
    """
    def draw_image(screen, player, position, image_x, image_y, image_w, image_h):#Show pic in screen
        screen.blit(player, position, (image_x*image_w, image_y*image_h, image_w, image_h))
        
    def draw_mouse_screen(screen,image):#Show mousesreen in screen
        MOUSE_POSITION=(0,0)
        screen.blit(image,MOUSE_POSITION)
        
    def draw_str(screen,text,position=(122,600)):#Show words in screen
        # This function borrows the code from the link in https://jingyan.baidu.com/article/4f34706e0a0fa9e387b56dbf.html step 3
        FONT_TYPE="FONT1.TTF"# file name
        FONT_SIZE=33
        FONT_COLOR=pygame.Color(37,4,4)# Set font color, R.G.B format
        
        font  =  pygame.font.Font(FONT_TYPE,FONT_SIZE)
        text_set  =  font.render(text,True,FONT_COLOR)
        screen.blit(text_set, position)
        
    def draw_dialog(screen,text):
        DIALOG_POSTTION=(78,570)
        ICON_POSITION=(1105,585)
        ICON_HEIGHT=144
        DIA_IMAGE='pic/dialog.png'
        ICON_IMAGE='pic/icon.png'
        
        dialog_pic=pygame.image.load(DIA_IMAGE).convert_alpha()
        icon_pic=pygame.image.load(ICON_IMAGE).convert_alpha()
        screen.blit(dialog_pic,DIALOG_POSTTION)
        screen.blit(icon_pic, ICON_POSITION , (text[1]*ICON_HEIGHT, text[2]*ICON_HEIGHT, ICON_HEIGHT, ICON_HEIGHT))# Drawing icon
        Draw.draw_str(screen,text[0])
        if len(text)==4 and Music.now_dialog_music!=text[3]:#Determine whether this dialogue has music attributes,
            # Determine whether this dialogue is currently playing music
            Music.now_dialog_music=text[3]
            Music.play_music(text[3])
            
class Music:
    """Class Music controls all thing relate to music in the game"""
    pygame.mixer.init()
    now_dialog_music=''
    bgm=pygame.mixer.Sound("music/"+'start.wav')
    
    def play_music(musicinfo):# Play music
        
        if musicinfo[1]==0:#Determine whether it is short music
            music0=pygame.mixer.Sound("music/"+musicinfo[0])
            music0.set_volume(musicinfo[2])
            music0.play()
        else:#If it is not short music, it will play in loop
            Music.bgm=pygame.mixer.Sound("music/"+musicinfo[0])
            Music.bgm.set_volume(musicinfo[2])
            Music.bgm.stop()
            Music.bgm.play(loops=-1)# Loop

        