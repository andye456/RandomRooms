import characters.CharacterAbilities


class Character:
    name = ""
    age = 0
    hit_points = 0
    race = ""
    char_class = ""
    inventory = {}
    x_pos = 0
    y_pos = 0
    weapon = ""
    abilities = []

    def __init__(self, name, age, hit_points, race, char_class, items, x_pos, y_pos, weapon, abilities):
        print("hit_points = "+str(hit_points))
        self.name = name
        self.age = age
        self.hit_points = hit_points
        self.race = race
        self.char_class = char_class
        self.inventory = items
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.weapon = weapon
        self.abilities = abilities
