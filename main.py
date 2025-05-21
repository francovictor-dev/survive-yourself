import pygame
import random
import math
from classes.hero import Hero
from classes.enemy import Enemy
from classes.item import Item


################
# GAME CONFIGS #
################

WIDTH = 1200
HEIGHT = 800
TILE_SIZE = 16  # tamanho dos tiles (ex: 64x64)

knockback_obj = None
dx = 0 
dy = 0
frame = 0
force = 0
points = 0
record_points = 0
cols = WIDTH // TILE_SIZE
rows = HEIGHT // TILE_SIZE
tilemap = [
    [random.choices([0, 1, 2], weights=[85, 13, 2])[0] for _ in range(cols)]
    for _ in range(rows)
]
timer_seconds = 0
life_color = 'white'
pressed_keys = set()
is_start = False
sounds_list = ["sfx_coin", "sfx_improve", "sfx_recover", "sfx_select", "sfx_slash", "sfx_steps", "sfx_sword", "sfx_throw"]

menu_rect = Rect(((WIDTH // 2)-150, (HEIGHT // 2) - 50), (300, 200))
menu_rect_start_text = Rect((menu_rect.x, menu_rect.y + 20), (300, 40))
menu_rect_quit_text = Rect((menu_rect.x, menu_rect.y + menu_rect.height - 60), (300, 40))
switch_song = Rect((menu_rect.centerx + 70, menu_rect.centery - 18), (60, 40))
is_actived_songs = True

#############
# FUNCTIONS #
#############

def start_state():
  music.play('title')
  hero.refresh()

def start_game_scene():
  draw_game_objects()
  
  screen.draw.text("Pontos: {points}".format(points=points), color='white', topleft=(20, 20), shadow=(0.5,0.5),scolor='black', fontsize=30)
  screen.draw.text("Tempo: {time}".format(time=format_time(timer_seconds)), color='white', topleft=(20, 50), shadow=(0.5,0.5),scolor='black', fontsize=30)
  screen.draw.text("Vida: {life}%".format(life=math.floor(hero.life_point)), color=life_color, midtop=(WIDTH // 2, 10), shadow=(0.5,0.5),scolor='black', fontsize=46)

def title_scene():
   screen.draw.text("Survive Yourself!", color="white", midtop=(((WIDTH // 2), 200)), shadow=(0.5, 0.5), scolor='black', fontsize=60)
   screen.draw.filled_rect(menu_rect, (50,50,50))

   screen.draw.text("Record: {points} (pontos + tempo x2)".format(points=record_points), color='black', center=(menu_rect.centerx, menu_rect.y - 20), shadow=(0.5,0.5),scolor='black', fontsize=30)

   screen.draw.text("Comecar o jogo", color="white", center=(menu_rect_start_text.center), shadow=(0, 0), scolor='black', fontsize=36)
   screen.draw.text("Musicas/Sons", color="white", center=(menu_rect.centerx - 20, menu_rect.centery), shadow=(0, 0), scolor='black', fontsize=36)
   screen.draw.rect(switch_song, (0 if is_actived_songs else 255,200,0))
   screen.draw.text("ON" if is_actived_songs else "OFF", color="white", center=(switch_song.center), shadow=(0, 0), scolor='black', fontsize=36)
   screen.draw.text("Sair", color="white", center=(menu_rect_quit_text.center), shadow=(0, 0), scolor='black', fontsize=36)

def draw_game_objects():
   global all_game_objects
   
   for obj in sorted(
      all_game_objects, key=lambda o: o.original_y if o.tag == 'hero' else o.y
    ):
      if obj.tag == 'hero':
         screen.blit(obj.draw(), (obj.x, obj.y))
      else:
         obj.draw()
      
def stages():
  global frame, all_game_objects, all_enemies, timer_seconds, is_start

  if not is_start: return

  if timer_seconds < 10:
     index_enemy = [0]
  elif timer_seconds < 25:
     index_enemy = [0, 1]
  elif timer_seconds < 50:
     index_enemy = [0, 1, 2]
  else:
     index_enemy = [0, 1, 2, 3]

  if frame != 0 and frame % 180 == 0:

    if timer_seconds <= 30:
      enemies = [create_obj_clone(all_enemies[random.choice(index_enemy)]) for _ in range(2)]
    elif timer_seconds <= 90:
      enemies = [create_obj_clone(all_enemies[random.choice(index_enemy)]) for _ in range(3)]
    elif timer_seconds <= 150:
      enemies = [create_obj_clone(all_enemies[random.choice(index_enemy)]) for _ in range(6)]
    else:
      enemies = [create_obj_clone(all_enemies[random.choice(index_enemy)]) for _ in range(10)]
      
    all_game_objects = [
        *all_game_objects,
        *enemies
    ]

def create_obj_clone(obj):
   if obj.tag == 'item':
    return Item(
      item=Actor(obj._item.image),
      action=obj.handleAction,
      sound_name=obj.sound_name
    )

   if obj.tag == 'enemy':
    position = get_enemy_spawn_position()
    return Enemy(
        life_point=obj.life_point, 
        attack_value=obj.attack_value, 
        enemy=Actor(obj._enemy.image), 
        tag=obj.tag, 
        moviment_value=random.uniform(obj._moviment_value - 0.5, obj._moviment_value + 1), 
        frames=obj.frames, 
        x=position[0], 
        y=position[1],
        points=obj._points
      )

def get_enemy_spawn_position():
   screen_side = random.choice(['left', 'right', 'top', 'bottom'])
   if screen_side == 'left':
        x = 0
        y = random.randint(0, HEIGHT)
   elif screen_side == 'right':
       x = WIDTH
       y = random.randint(0, HEIGHT)
   elif screen_side == 'top':
       x = random.randint(0, WIDTH)
       y = 0
   else:  # baixo
       x = random.randint(0, WIDTH)
       y = HEIGHT

   return x, y

def on_mouse_down(pos):
   global is_start, is_actived_songs, timer_seconds, frame
   
   if switch_song.collidepoint(pos):
      is_actived_songs = not is_actived_songs

   if menu_rect_start_text.collidepoint(pos):
     is_start = True
     timer_seconds = 0
     music.play("battle")
     frame = 0

   if menu_rect_quit_text.collidepoint(pos):
      exit()

   if is_actived_songs:
      music.set_volume(1)
      for sound in sounds_list:
        getattr(sounds, sound).set_volume(1)
   else:
      music.set_volume(0)
      for sound in sounds_list:
        getattr(sounds, sound).set_volume(0)

def on_key_down(key):
   global frame_counter
   pressed_keys.add(key)
   
   if hero._is_attack:
      return

   if key == keys.RETURN:
      hero.start_attack()

def on_key_up(key):

  if key in pressed_keys:
    pressed_keys.remove(key)

  if (pressed_keys.__len__() > 0):
     return

  if key == keys.D or key == keys.A or key == keys.S or key == keys.W:
     hero.animation_idle()

def is_hero_collision(obj):
   return hero.collision_box().colliderect(obj.collision_box())

def is_hero_attack_collision(enemy):
   return hero.attack_collision().colliderect(enemy.collision_box())

def knockback_enemy(enemy):
    global knockback_obj, frame, dx, dy, force

    dx = enemy.x - hero.original_x
    dy = enemy.y - hero.original_y

    dist = math.hypot(dx, dy)
    if dist == 0:
        return 

    dx /= dist
    dy /= dist

    force = 0
    frame = 0
    knockback_obj = enemy

def increment_timer():
    global timer_seconds
    timer_seconds += 1

def format_time(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"

def drop_items():
   global all_items
   
   rate_drop = 50

   chance = random.randint(0, 100)

   if chance > rate_drop: 
    return None

   item = random.choice(all_items)

   return create_obj_clone(item)

def game_over():
    global all_game_objects, is_start, record_points, points, timer_seconds
    is_start = False
    hero.x = WIDTH // 2
    hero.y = HEIGHT // 2
    hero._moviment_value = 1.5
    hero._animation_speed = 8
    hero.attack_value = 10
    hero.life_point = 100
    all_game_objects = [hero]
    total_points = timer_seconds * 2 + points
    record_points = total_points if record_points < total_points else record_points
    points = 0
    music.play("title")

def colission_update():
  global life_color, all_game_objects, points, is_start, record_points, points
  
  for obj in all_game_objects:

    # SOM DO ATAQUE
    if hero.attack_collision().x > 0:
      if obj.tag == "enemy" and is_hero_attack_collision(obj):  
       sounds.sfx_sword.play()
      else:
       sounds.sfx_slash.play()

    # COLISAO DO INIMIGO COM HEROI
    if obj.tag == "enemy" and is_hero_collision(obj):
      life_color = 'red'
      hero.life_point -= obj.attack_value / 100
      if (hero.life_point == 0):
        game_over()

    # COLISAO DO HEROI COM INIMIGOS
    if obj.tag == "enemy" and is_hero_attack_collision(obj):
      
      obj.life_point -= hero.attack_value
  
      if (obj.life_point == 0):
        points += obj._points
        new_item = drop_items()

        if new_item:
          new_item.x = obj.x
          new_item.y = obj.y
          update_game_objects = [e for e in all_game_objects if e != obj]
          all_game_objects = [*update_game_objects, new_item]   
        else:
          all_game_objects = [e for e in all_game_objects if e != obj]
        
      else: 
        knockback_enemy(obj)
      
    if obj.tag == "item" and is_hero_collision(obj):
       obj.handleAction()
       sound = getattr(sounds, obj.sound_name)
       sound.play()
       all_game_objects = [e for e in all_game_objects if e != obj]
       

  enemies_list = [obj for obj in all_game_objects if obj.tag == 'enemy']

  if all(not is_hero_collision(enemy) for enemy in enemies_list):
    life_color = 'white'

def keyboard_update():
   global frame

   is_step_time = frame % (9 + hero._animation_speed + hero._animation_speed) == 0

   if keyboard.d:
      if hero.x >= WIDTH - (hero._FRAME_HEIGHT * 0.75): return 
      hero.move_right()   
      if is_step_time:
        sounds.sfx_steps.play()
      
   if keyboard.a:
      if hero.x <= 0 - (hero._FRAME_HEIGHT * 0.25): return 
      hero.move_left()   
      if is_step_time:
        sounds.sfx_steps.play()

   if keyboard.w:
      if hero.y <= 0 - (hero._FRAME_HEIGHT * 0.25): return 
      hero.move_up()   
      if is_step_time:
        sounds.sfx_steps.play()

   if keyboard.s:
      if hero.y >= HEIGHT - (hero._FRAME_HEIGHT * 0.75): return 
      hero.move_down()
      if is_step_time:
        sounds.sfx_steps.play()

def improve_attack():
   hero.attack_value += 5

def improve_speed():
   if hero._animation_speed > 3:
    hero._animation_speed -= 1  
   hero._moviment_value += 0.25

def get_point():
   global points
   points += 100

def recover_life():
   hero.life_point += 10
   if hero.life_point >= 100:
      hero.life_point = 100

################
# GAME OBJECTS #
################

hero = Hero(life_point=100,attack_value=10, hero=Actor("blank"), sprite_hero=Actor("warrior"), tag="hero")
hero.y = HEIGHT // 2
hero.x = WIDTH // 2

start_state()

clock.schedule_interval(increment_timer, 1.0) 

all_items = [
   Item(item=Actor('axe'), action=improve_attack, sound_name='sfx_improve'), 
   Item(item=Actor('water'), action=improve_speed, sound_name='sfx_improve'),
   Item(item=Actor('coin'), action=get_point, sound_name='sfx_coin'),
   Item(item=Actor('mushroom'), action=recover_life, sound_name='sfx_recover')
]

all_enemies = [
   Enemy(
      life_point=20, 
      attack_value=10, 
      enemy=Actor("slime_1"), 
      tag="enemy", 
      moviment_value=1, 
      frames=["slime_1", "slime_2"], 
      x=random.choice([0, WIDTH]), 
      y=random.choice([0, HEIGHT]),
      points=100
    ),
  Enemy(
      life_point=40, 
      attack_value=15, 
      enemy=Actor("worm_1"), 
      tag="enemy", 
      moviment_value=1.5, 
      frames=["worm_1", "worm_2"], 
      x=random.choice([0, WIDTH]), 
      y=random.choice([0, HEIGHT]),
      points=200
    ),
  Enemy(
      life_point=80, 
      attack_value=20, 
      enemy=Actor("block_1"), 
      tag="enemy", 
      moviment_value=1, 
      frames=["block_1", "block_2"], 
      x=random.choice([0, WIDTH]), 
      y=random.choice([0, HEIGHT]),
      points=500
    ),
  Enemy(
      life_point=120, 
      attack_value=25, 
      enemy=Actor("saw_1"), 
      tag="enemy", 
      moviment_value=1, 
      frames=["saw_1", "saw_2"], 
      x=random.choice([0, WIDTH]), 
      y=random.choice([0, HEIGHT]),
      points=1000
    )
]

all_game_objects = [
   hero,
]


def draw():
    screen.clear()
    
    for row_index, row in enumerate(tilemap):
      for col_index, tile_id in enumerate(row):
          tile_name = f"tile_{tile_id}"
          x = col_index * TILE_SIZE
          y = row_index * TILE_SIZE
          screen.blit(tile_name, (x, y))

    if is_start:   
     start_game_scene()
    else:
     title_scene()

def update():
    global knockback_obj, frame, dx, dy, force, all_game_objects, all_enemies, timer_seconds

    frame += 1

    if knockback_obj:
      if frame % 1 == 0: 
        knockback_obj.x += dx * 10
        knockback_obj.y += dy * 10
        force += 1
      if force == 10:
         force = 0
         knockback_obj = None

    enemies_obj = [obj for obj in all_game_objects if obj.tag == 'enemy']
    for enemy in enemies_obj:
      enemy.update(hero)

    stages()

    colission_update()

    keyboard_update()

    hero.update()
   
    