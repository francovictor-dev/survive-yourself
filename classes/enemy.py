import math
from .entity import Entity
import pygame

class Enemy(Entity):
  def __init__(self, life_point, attack_value, enemy, tag, moviment_value, frames,x, y, points):
    super().__init__(life_point, attack_value, tag)
    self._enemy = enemy
    self._moviment_value = moviment_value
    self._enemy.x = x
    self._enemy.y = y
    self._enemy.frames = frames
    self._enemy.current_frame = 0
    self._enemy.frame_counter = 0
    self._enemy.fps = 2
    self._points = points
  
  @property
  def frames(self):
    return self._enemy.frames
  
  @frames.setter
  def frames(self, value):
    self._enemy.frames = value

  def pos(self, x, y):
    self._enemy.x = x
    self._enemy.y = y

  @property
  def x(self):
    return self._enemy.x
  
  @property
  def y(self):
    return self._enemy.y
  
  @x.setter
  def x(self, value):
    self._enemy.x = value 

  @y.setter
  def y(self, value):
    self._enemy.y = value 

  def draw(self):
    self._enemy.draw()

  def move_to_hero(self, hero):
    dx = hero.original_x - self._enemy.x
    dy = hero.original_y - self._enemy.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        return 

    dx /= dist
    dy /= dist

    self._enemy.x += dx * self._moviment_value
    self._enemy.y += dy * self._moviment_value

  def update(self, hero):
    self.move_to_hero(hero)
    self._enemy.frame_counter += 1
    if self._enemy.frame_counter >= 60 // self._enemy.fps:  # assume 60 FPS padrão
      self._enemy.frame_counter = 0
      self._enemy.current_frame = (self._enemy.current_frame + 1) % len(self._enemy.frames)
      self._enemy.image = self._enemy.frames[self._enemy.current_frame]
  
  def collision_box(self):
    return  pygame.Rect(
        self._enemy.x - self._enemy.width // 2,
        self._enemy.y - self._enemy.height // 2,
        self._enemy.width,
        self._enemy.height
    )
    