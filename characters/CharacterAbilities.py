class CharacterAbilities:


    # abilities=[charisma,constitution,dexterity,intelligence,strength,wisdom]

    def __init__(self,race,char_class):
        self.charisma = {"id": "charisma", "value": 10}
        self.constitution = {"id": "constitution", "value": 10}
        self.dexterity = {"id": "dexterity", "value": 10}
        self.intelligence = {"id": "intelligence", "value": 10}
        self.strength = {"id": "strength", "value": 10}
        self.wisdom = {"id": "wisdom", "value": 10}
        # Sigh this is laboureous
        if race == 'Dwarf':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Elf':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Gnome':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Half_Elf':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8,intelligence=4)
            if char_class == "Illusionist":
                self.setAbilities(strength=8,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15,intelligence=4)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13,intelligence=4)

        if race == 'Halfling':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Half_Orc':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=6)
            if char_class == "Illusionist":
                self.setAbilities(strength=6,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

        if race == 'Human':
            if char_class == "Assassin":
                self.setAbilities(strength=12,intelligence=11)
            if char_class == "Druid":
                self.setAbilities(strength=8)
            if char_class == "Illusionist":
                self.setAbilities(strength=8,intelligence=15)
            if char_class == "Monk":
                self.setAbilities(strength=15)
            if char_class == "Paladin":
                self.setAbilities(strength=12,intelligence=9)
            if char_class == "Ranger":
                self.setAbilities(strength=13)

    def setAbilities(self,charisma=10,constitution=10,dexterity=10,intelligence=10,strength=10,wisdom=10):
        self.charisma['value']=charisma
        self.constitution['value']=constitution
        self.dexterity['value']=dexterity
        self.intelligence['value']=intelligence
        self.strength['value']=strength
        self.wisdom['value']=wisdom

    def getAbilities(self):
        abilities=[self.charisma,self.constitution,self.dexterity,self.intelligence,self.strength,self.wisdom]
        return abilities



if __name__ == "__main__":
    c = CharacterAbilities("Dwarf", "Monk")
    print(c.getAbilities())

