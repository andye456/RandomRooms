from characters.CharacterAbilities import CharacterAbilities
from characters import  Items
from characters import Weapons

# Race
class Dwarf(CharacterAbilities):
    _spells=True
    _size="small"

    _weapon = Weapons.Cane
    _money_gold="2"
    _money_silver="2"

    _items=[Items.Candle,Items.Backpack]