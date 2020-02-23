from characters.CharacterAbilities import CharacterAbilities
from characters import Weapons


import characters.Items as Items
# Race
class Halfling(CharacterAbilities):
    _spells=False
    _size="small"

    _weapon = Weapons.Club
    _money_gold="12"
    _money_silver="5"

    _items=[Items.Candle,Items.Backpack]