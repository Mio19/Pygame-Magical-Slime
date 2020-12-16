import Global_var as gv
from Draw import Draw

class Dialog:
    """This class is used to set up and run dialogs"""
    def __init__(self,text=''):
        self.text=text# text is initially set to empty
        self.flag=False # False means the dialog is not displayed
        self.index=0# Index used when drawing the dialog
                
    def show(self):
        game_main=gv.get_dict('game_main')
        Draw.draw_dialog(game_main.screen,self.text[self.index])
        
    def show_next(self):
        if self.index < len(self.text)-1:
            self.index +=1
        else:
            self.flag=False
            self.index=0
            
    def dialog_check(self):
        if self.flag:
            self.show()
    
    def set_dialog(self,textinfo):#Setting the content of the dialog and make it invisiable
        self.text=textinfo
        self.flag= not self.flag