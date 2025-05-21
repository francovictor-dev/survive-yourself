# entity.py

class Entity:
    def __init__(self, life_point, attack_value, tag):
      self._life_point = life_point
      self._attack_value = attack_value
      self._tag = tag

    @property
    def life_point(self):
        return self._life_point

    @life_point.setter
    def life_point(self, value):
        if value < 0:
            value = 0  # Evita vida negativa
        self._life_point = value

    @property
    def attack_value(self):
        return self._attack_value

    @attack_value.setter
    def attack_value(self, value):
        if value < 0:
            raise ValueError("O valor de ataque não pode ser negativo.")
        self._attack_value = value

    @property
    def tag(self):
        return self._tag


    
