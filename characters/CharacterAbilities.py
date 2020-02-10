# This describes the character abilities


class CharacterAbilities:
    _name = ""
    _health = 0
    _level = 0

    _charisma = 10
    _constitution = 10
    _dexterity = 10
    _intelligence = 10
    _strength = 10
    _wisdom = 10

    _char_class=""
    _char_race=""

    def __init__(self, name):
        self._name=name
