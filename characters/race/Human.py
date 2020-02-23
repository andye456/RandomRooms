from characters import Items
from characters.CharacterAbilities import CharacterAbilities
from characters import Weapons
# Race
class Human(CharacterAbilities):
    _spells=False
    _size="large"

    _weapon = Weapons.Cane
    _money_gold="2"
    _money_silver="2"

    _items=[Items.Candle,Items.Backpack]


