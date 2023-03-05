from enemy import Enemy
import random
import time
import main

class Level:
    def __init__(self,display,number):
        self.display = display
        self.number = number
    def iteration(self,enemies):
        for i in range(self.len_):
            step = random.randint(0,10)
            position = random.randint(100,main.scr_size.current_w-100)
            time.sleep(step)
            new_enemy = Enemy(self.display,(position,0),enemies[0],enemies[1],enemies[2],enemies[3],enemies[4],enemies[5])
            Enemy.entities.append()
            Entity.all_sprite_list.add(new_enemy)

for i in range(10):
    with open(f'Levels/level{i}.txt','r') as file:
        data = file.readlines()
        level = Level(main.display,i)
        for line in data:
            line = line.split(':')
            level.iteration(line)

