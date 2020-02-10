from characters.CharacterAbilities import CharacterAbilities


# Race
class Elf(CharacterAbilities):
    _size = "small"


    def __init__(self):
        self._dexterity += 1
        self._constitution -= 1
