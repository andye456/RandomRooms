from characters.CharacterAbilities import CharacterAbilities
from characters import  Items
from characters import Weapons

# Race
class Half_Orc(CharacterAbilities):
    _spells=True
    _size="large"

    _weapon = Weapons.Club
    _money_gold="12"
    _money_silver="5"

    _items=[Items.Candle,Items.Backpack]