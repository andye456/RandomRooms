class CharacterAbilities:

    # abilities={charisma,constitution,dexterity,intelligence,strength,wisdom}

    def __init__(self, race, char_class):
        self.charisma = 10
        self.constitution = 10
        self.dexterity = 10
        self.intelligence = 10
        self.strength = 10
        self.wisdom = 10
        # Sigh this is laboreous
        if race == 'Dwarf':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Elf':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Gnome':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Half_Elf':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8, intelligence=4)
            if char_class == "Illusionist":
                self.setAbilities(strength=8, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15, intelligence=4)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13, intelligence=4)

        if race == 'Halfling':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Half_Orc':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Human':
            if char_class == "Assassin":
                self.setAbilities(strength=12, intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8, intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12, intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

    def setAbilities(self, charisma=10, constitution=10, dexterity=10, intelligence=10, strength=10, wisdom=10):

        self.charisma = charisma
        self.constitution = constitution
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.strength = strength
        self.wisdom = wisdom

    def getAbilities(self):
        abilities = {"charisma":self.charisma, "constitution": self.constitution, "dexterity":self.dexterity,
                     "intelligence":  self.intelligence, "strength": self.strength, "wisdom": self.wisdom}
        return abilities


if __name__ == "__main__":
    c = CharacterAbilities("Dwarf", "Monk")
    print(c.getAbilities())
