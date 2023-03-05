import random
from enemy import Enemy
from bullet import Bullet
from player import Player
from power_up import Power_up
import pygame
import math
import asyncio
from entity import Entity
from websocks import WebsocketServer, MoveMessage, ShootMessage, NewPlayerMessage, KillPlayerMessage, UPDATING_LIFE, \
    StartMessage
from threading import Thread
import queue
from macron_explosion import Explosion

websocket_to_pygame = queue.Queue()
pygame_to_websocket = queue.Queue()

phone_input = True
display = None
last_message = None

levels = []
def load_levels():
    global levels
    for i in range(1,2):
        with open(f'level{i}.txt', 'r') as file:
            levels.append([])
            data = file.readlines()
            for line in data:
                line = line.split(':')
                levels[i-1].append(line)
wave = -1
wave_index = 0
wave_loader = -1
def summon_level(scr_size):
    if len(levels) == 0:
        return
    global wave
    global wave_loader
    global wave_index
    time = pygame.time.get_ticks()
    if time > wave_loader + 4500/(len(Player.entities)) or wave_loader == -1:
        print("[*] Spawning a new ship")
        wave_loader = time
        if wave_index == len(levels[wave]):
            wave += 1
            wave_index = 0
        else:
            line = levels[wave][wave_index]
            random_pos = random.randint(200,scr_size.current_w-200)
            x = eval(line[2])
            y = eval(line[3])
            create_ship(line[0], (random_pos,0),int(line[4]),y,x,line[1], int(line[5]), int(line[6]), None)
            wave_index += 1



def move(message):
    Player.entities[message.client_id].move_p(message.up, message.down, message.right, message.left)


def create_ship(sprite, position, damage, speed, bullet_speed, bullet_sprite, health, reload_time, type):
    Enemy(display, position, sprite, bullet_sprite, bullet_speed, speed, damage, health, reload_time, type)


def create_player(id, sprite, bullet_speed, damage):
    Player(id, display, [display.get_size()[0] // 2, display.get_size()[1] - 400], damage, sprite, bullet_speed)


def main():
    global display
    global last_message
    global wave
    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Audio/main.ogg")
    pygame.mixer.music.play(-1)
    # Initialisation de la fenêtre
    pygame.init()
    load_levels()
    scr_size = pygame.display.Info()

    display = pygame.display.set_mode((scr_size.current_w, scr_size.current_h))
    pygame.display.set_caption("Pilou-Pilou")

    # Setting up the background
    bg = pygame.transform.scale(pygame.image.load("Assets/Background/background.png").convert(),
                                (scr_size.current_w, scr_size.current_h))
    tiles = math.ceil(scr_size.current_w - 100 / bg.get_height()) + 1
    scroll = 0

    num_frames = 35
    frame_width = 64
    frame_height = 64
    tilesheet = pygame.image.load("Assets/Macron RXPLOSION/bk_explo_one.png").convert_alpha()
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = tilesheet.subsurface(rect)
        frames.append(frame)
    frame = frames[15]

    # Listes de sprites
    all_sprites_list = pygame.sprite.Group()
    clock = pygame.time.Clock()

    # Creating enemies

    """
    create_ship(sprite="Assets/Enemy Ships/BigShip1.png",
                position=[300, 200],
                damage=50,
                speed=[0, 0],
                bullet_speed=[[-10, 2], [10, 2]],
                bullet_sprite="Assets/Projectiles/Projectiles/b2_01.png",
                health=200,
                reload_time=3,
                type='none')
    """

    # Creating player
    if not phone_input:
        create_player(0, "Assets/Hero_ship.png", [0, -4], 10)

    created = False
    prev_time = 0
    randomval = 1

    while True:
        messages = []
        if websocket_to_pygame.empty():
            for player in Player.entities:
                messages.append(player.last_message)
        while not websocket_to_pygame.empty():
            messages.append(websocket_to_pygame.get())
        for player in Player.entities:
            player.has_moved = False
        for x in reversed(messages):
            try:
                if type(x) == MoveMessage and not Player.entities[x.client_id].has_moved:
                    move(x)
                    Player.entities[x.client_id].has_moved = True
                    Player.entities[x.client_id].last_message = x
                elif type(x) == ShootMessage:
                    Player.entities[x.client_id].shoot()
                elif type(x) == NewPlayerMessage:
                    create_player(len(Player.entities), "Assets/Hero_ship.png", [0, -4], 10)
                elif type(x) == KillPlayerMessage:
                    Player.entities[x.client_id].self_kill()
                elif type(x) == StartMessage:
                    wave = 0
            except IndexError:
                pass

        # Effective handling of input type
        if not phone_input:
            keys = pygame.key.get_pressed()
            Player.entities[0].move_k(keys)

        # Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_SPACE:
                for player in Player.entities:
                    player.shoot()

        # Out of screen
        for enemy_ship in Enemy.entities:
            if enemy_ship.rect.y > scr_size.current_h:
                enemy_ship.self_kill()

            # Enemy side collisions
            elif enemy_ship.rect.x < 0 or enemy_ship.rect.x > display.get_width() - enemy_ship.rect.width:
                enemy_ship.speed[0] = enemy_ship.speed[0] * -1

            # reload time is good
            elif int(enemy_ship.clock) == enemy_ship.reload_time:
                enemy_ship.clock = 0
                try:

                    for i in range(len(enemy_ship.bullet_speed)):
                        enemy_ship.shoot(enemy_ship.bullet_speed[i])



                except:
                    enemy_ship.shoot(enemy_ship.bullet_speed)

        # out of screen
        for projectile in Bullet.entities:
            if projectile.rect.y > scr_size.current_h or projectile.rect.y + projectile.rect.height < 0:
                projectile.self_kill()
        # hits
        for player in Player.entities:
            enemy_hit_list = pygame.sprite.spritecollide(player, Bullet.enemy_bullet_sprites, False)
            for hit in enemy_hit_list:
                player.get_hit(hit.damage)
                pygame_to_websocket.put([UPDATING_LIFE, Player.entities.index(player), player.lives])
                if player.lives <= 0:
                    player.self_kill()
        # hits
        for enemy_ship in Enemy.entities:
            player_hit_list = pygame.sprite.spritecollide(enemy_ship, Bullet.player_bullet_sprites, False)
            if player_hit_list != []:
                print('ENEMY got hit ', player_hit_list)
            for hit in player_hit_list:
                hit.self_kill()
                enemy_ship.get_hit(hit.damage)
                audio = pygame.mixer.Sound("./Assets/Audio/little-hit.wav")
                pygame.mixer.Sound.play(audio)
                hit.shooter.score += 10 + round(enemy_ship.health / 10)
                expl = Explosion(display,(hit.rect.x,hit.rect.y),frame)
                Explosion.entities.append(expl)


                pygame_to_websocket.put([1, Player.entities.index(hit.shooter), hit.shooter.score])
            if enemy_ship.health < 0:
                enemy_ship.self_kill()
                audio = pygame.mixer.Sound("./Assets/Audio/ennemy_dead.wav")
                pygame.mixer.Sound.play(audio)

        # this is for collision with ship

        for enemy_ship in Enemy.entities:
            player_hit_list = pygame.sprite.spritecollide(enemy_ship, Player.entities, False)
            if player_hit_list != []:
                print('CRASH got hit ', player_hit_list)
            for hit in player_hit_list:
                enemy_ship.self_kill()
                hit.self_kill()

        # Power up création

        if wave > -1:
            if not created and randomval == 400:
                big_cock_power = Power_up(display, (400, 400), random.randint(0, len(Power_up.power_up_sprites) - 1))
                created = True
                randomval = 0
            randomval += 1

        if created:
            big_cock_power.clock.tick(120)
            big_cock_power.move()

            players_bonus_list = pygame.sprite.spritecollide(big_cock_power, Player.entities, False)

            for gamer in players_bonus_list:
                big_cock_power.on_touch(gamer)
                big_cock_power.self_kill()
                prev_time = 0
                created = False

            prev_time += big_cock_power.clock.get_time()
            if prev_time > Power_up.up_timer:
                big_cock_power.self_kill()
                prev_time = 0
                created = False

        # =========================================
        # BACKGROUND
        # =========================================

        clock.tick(125)

        i = 0
        while i < tiles:
            display.blit(bg, (0, -(bg.get_height() * i) + scroll))
            i += 1
        if wave > -1:
            scroll += 6

        if abs(scroll) > bg.get_height():
            scroll = 0
        # =========================================
        if wave >= 0:
            summon_level(scr_size)
        Enemy.move_all()
        Entity.draw_all()
        for exl in Explosion.entities:
            exl.count+=0.1
            if int(exl.count) == 10:
                exl.kill()

        font = pygame.font.Font('./Assets/fonts/Retro.ttf', 40)
        font3 = pygame.font.Font('./Assets/fonts/Retro.ttf', 50)
        font2 = pygame.font.Font('./Assets/fonts/Retro.ttf', 20)
        text = font2.render(str(int(clock.get_fps())), 1, pygame.Color("LIGHTBLUE"))
        display.blit(text, (5,5))

        if len(Player.entities) == 0:
            text2 = font.render("Waiting for connections...", 1, pygame.Color("WHITE"))
            text3 = font3.render("Press start to launch the game", 1, pygame.Color("WHITE"))
            display.blit(text2, (scr_size.current_w/2-text2.get_width()/2, scr_size.current_h/2-text2.get_height()/2))
            display.blit(text3,(scr_size.current_w/2-text3.get_width()/2, scr_size.current_h/2-text3.get_height()/2+50))

        # Updating the display
        pygame.display.flip()
        if len(Player.entities) == 0 and wave > 0:
            exit()


def setupWSEverything():
    server = WebsocketServer()
    u = asyncio.run(server.run(websocket_to_pygame, phone_input, pygame_to_websocket))
    u.result()


async def setup():
    x = Thread(target=setupWSEverything)
    x.daemon = True
    y = Thread(target=main)
    y.daemon = True
    x.start()
    y.start()
    x.join()


if __name__ == "__main__":
    asyncio.run(setup())
