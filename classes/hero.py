from .entity import Entity
import pygame

class Hero(Entity):

  def __init__(self, life_point, attack_value, hero, sprite_hero, tag):
    super().__init__(life_point, attack_value, tag)
    # SPRITE
    self._idle_frames=[]
    self._frame_index = 0
    self._frame_counter = 0
    self._sprite_hero = sprite_hero
    self._FRAME_WIDTH = 192
    self._FRAME_HEIGHT = 192
    self._IDLE_FRAMES = 6  # Total de quadros na animação idle (linha 0)
    self._animation_index = 0
    self._hero = hero
    self._moviment_value = 1.5
    self._sprite_surface = sprite_hero._surf  # acesso ao pygame.Surface
    self._side="right"
    self._animation_speed = 8 
    self._is_attack = False


  # Atualiza sprite na tela
  def refresh(self):
    self._idle_frames = [
        self._sprite_surface.subsurface(pygame.Rect(i * self._FRAME_WIDTH, self._animation_index * self._FRAME_HEIGHT, self._FRAME_WIDTH, self._FRAME_HEIGHT))
        for i in range(self._IDLE_FRAMES)
    ]

  def draw(self):
    return self._idle_frames[self._frame_index]
  
  @property
  def x(self):
    return self._hero.x - self._FRAME_WIDTH // 2
  
  @property
  def y(self):
    return self._hero.y - self._FRAME_HEIGHT // 2
  
  @property
  def original_x(self):
    return self._hero.x 
  
  @property
  def original_y(self):
    return self._hero.y 

  @x.setter
  def x(self, value):
    self._hero.x = value 

  @y.setter
  def y(self, value):
    self._hero.y = value 
  
  @property
  def is_attack(self):
    return self._is_attack
  
  # Cria o retângulo de colisao a partir do Hero
  def collision_box(self):
    return pygame.Rect(
      self._hero.x - self._FRAME_WIDTH // 4, 
      self._hero.y - self._FRAME_HEIGHT // 4 - 6, 
      self._FRAME_WIDTH // 2, 
      self._FRAME_HEIGHT // 2
    )

  def move_up(self):
    if self._is_attack: return

    if self._side == "right":
      self._animation_index = 1
    else:
      self._animation_index = 9
    self._hero.y -= self._moviment_value
    self.refresh()

  def move_right(self):
    if self._is_attack: return

    self._side="right"
    self._animation_index = 1
    self._hero.x += self._moviment_value
    self.refresh()

  def move_left(self):
    if self._is_attack: return

    self._side="left"
    self._animation_index = 9
    self._hero.x -= self._moviment_value
    self.refresh()

  def move_down(self):
    if self._is_attack: return

    if self._side == "right":
      self._animation_index = 1
    else:
      self._animation_index = 9
    self._hero.y += self._moviment_value
    self.refresh()

  def start_attack(self):
    self._is_attack = True
    if self._side == "right":
        self._animation_index = 3
        self._frame_index=0
        self._frame_counter=0
    else:
       self._frame_index=5
       self._frame_counter=0
       self._animation_index = 11 
    self.refresh()

  def animation_attack(self):
    if self._side == "right":
      self._frame_counter += 1
      if self._frame_counter >= self._animation_speed:
        if self._frame_index == 5:         
          self._is_attack = False
          self._animation_index = 0  
          self.refresh()
          return 

        self._frame_counter = 0
        self._frame_index += 1
    else:
      if self._frame_index == 0:
        self._is_attack = False
        self._animation_index = 8  
        self.refresh()
        return
    
      self._frame_counter += 1     
      if self._frame_counter >= self._animation_speed:
        self._frame_counter = 0
        self._frame_index -= 1
    return

  def animation_idle(self):
    if self._side == "right":
      self._animation_index = 0   
    else:
      self._animation_index = 8  
    self.refresh()

  def attack_collision(self):
    if not self._is_attack:
      return pygame.Rect(
        0,0,0,0
      )

    if self._side == 'right':
      if self._frame_index == 3 and self._frame_counter == 0:
        return pygame.Rect(
          self._hero.x, 
          self._hero.y - self._FRAME_HEIGHT // 2, 
          self._FRAME_WIDTH // 2, 
          self._FRAME_HEIGHT
        )
      else:
        return pygame.Rect(0,0,0,0)
    else:
      if self._frame_index == 2 and self._frame_counter == 0:
        return pygame.Rect(
          self._hero.x - self._FRAME_WIDTH // 2, 
          self._hero.y - self._FRAME_HEIGHT // 2 , 
          self._FRAME_WIDTH // 2, 
          self._FRAME_HEIGHT
        )
      else:
        return pygame.Rect(0,0,0,0)

  def update(self):

    if self._is_attack:
      return self.animation_attack()

    self._frame_counter += 1
    if self._frame_counter >= self._animation_speed:
        self._frame_counter = 0
        self._frame_index = (self._frame_index + 1) % self._IDLE_FRAMES