from characters import  Items
from characters.CharacterAbilities import CharacterAbilities
from characters import Weapons


# Race
class Elf(CharacterAbilities):
    _size = "small"


    _weapon = Weapons.Cane
    _money_gold="2"
    _money_silver="2"

    _items=[Items.Candle,Items.Backpack]

    def __init__(self):
        self._dexterity += 1
        self._constitution -= 1
