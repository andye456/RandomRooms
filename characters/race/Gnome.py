from characters import Items
from characters.CharacterAbilities import CharacterAbilities
from characters import Weapons

# Race
class Gnome(CharacterAbilities):
    _spells=True
    _size="small"

    _weapon = Weapons.Club
    _money_gold="12"
    _money_silver="5"

    _items=[Items.Candle,Items.Backpack]