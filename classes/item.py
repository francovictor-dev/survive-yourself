import pygame

class Item:
  def __init__(self, item, action, sound_name):
    self._item = item
    self._action = action
    self._tag = "item"
    self._sound_name = sound_name
  
  @property
  def x(self):
    return self._item.x
  
  @property
  def y(self):
    return self._item.y
  
  @x.setter
  def x(self, value):
    self._item.x = value 

  @y.setter
  def y(self, value):
    self._item.y = value 

  @property
  def tag(self):
    return self._tag
  
  @property
  def sound_name(self):
    return self._sound_name

  @tag.setter
  def tag(self, value):
    self._tag = value 

  def draw(self):
    return self._item.draw()
  
  def handleAction(self):
    return self._action()

  def collision_box(self):
    return pygame.Rect(
        self._item.x - self._item.width // 2,
        self._item.y - self._item.height // 2,
        self._item.width,
        self._item.height
    )
