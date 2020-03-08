import characters.CharacterAbilities
class Character:

    name=""
    age=0
    skill=0
    race=""
    char_class=""
    inventory={}
    x_pos=0
    y_pos=0
    weapon=""
    abilities=[]
    hit_points=5

    def __init__(self, name, age, skill, race, char_class, items, x_pos, y_pos, weapon, abilities):
        self.name=name
        self.age=age
        self.skill=skill
        self.race=race
        self.char_class=char_class
        self.inventory=items
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.weapon=weapon
        self.abilities=abilities
