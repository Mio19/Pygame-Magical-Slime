from Actor import Monster
import Global_var as gv

class Monster_list:
    """This class is used to get the list of monsters"""
    def __init__(self):
        self.list=[]
    
    def put_monster(self,number):# Put monsters into the map
        MONSTER_IMG=[['monster.png','boom.png'],34,34]
        player1=gv.get_dict('player')
        monster_position=gv.get_dict('monster_position')# Get the monster position coordinates stored in Global_var
        
        monster_position_list=monster_position[str(number)]
        for i in monster_position_list:
            new_monster=Monster(i[0],i[1],player1,MONSTER_IMG[0],MONSTER_IMG[1],MONSTER_IMG[2])
            self.list.append(new_monster) 
            
    def check_monster_list(self):
        for i in self.list:
            i.actor_check()
            
    def fresh_monster(self,number):
        self.list=[]
        self.put_monster(number)
        
    def check_alive(self):
        for i in self.list:
            if i.show_flag==True:
                return True
        return False