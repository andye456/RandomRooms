"""
P indicates that the race is generally preferred, and dealings with the members of the race will be reflected accordingly.
G means that considerable goodwill exists towards the race.
T indicates that the race is viewed with tolerance and generally acceptable, if not loved.
N shows that the race is thought of neutrally, although some suspicion will be evidenced.
A means that the race is greeted with antipathy.
H tokens a strong hatred for the race in question.
"""
races = {
    ('Dwarf', 'Dwarf'): 'P',
    ('Dwarf', 'Elf'): 'A',
    ('Dwarf', 'Gnome'): 'G',
    ('Dwarf', 'Half_Elf'): 'N',
    ('Dwarf', 'Halfling'): 'G',
    ('Dwarf', 'Half_Orc'): 'H',
    ('Dwarf', 'Human'): 'N',
    ('Elf', 'Dwarf'): 'A',
    ('Elf', 'Elf'): 'P',
    ('Elf', 'Gnome'): 'T',
    ('Elf', 'Half_Elf'): 'G',
    ('Elf', 'Halfling'): 'T',
    ('Elf', 'Half_Orc'): 'A',
    ('Elf', 'Human'): 'N',
    ('Gnome', 'Dwarf'): 'G',
    ('Gnome', 'Elf'): 'T',
    ('Gnome', 'Gnome'): 'P',
    ('Gnome', 'Half_Elf'): 'T',
    ('Gnome', 'Halfling'): 'G',
    ('Gnome', 'Half_Orc'): 'H',
    ('Gnome', 'Human'): 'N',
    ('Half_Elf', 'Dwarf'): 'N',
    ('Half_Elf', 'Elf'): 'P',
    ('Half_Elf', 'Gnome'): 'T',
    ('Half_Elf', 'Half_Elf'): 'P',
    ('Half_Elf', 'Halfling'): 'N',
    ('Half_Elf', 'Half_Orc'): 'A',
    ('Half_Elf', 'Human'): 'T',
    ('Halfling', 'Dwarf'): 'G',
    ('Halfling', 'Elf'): 'G',
    ('Halfling', 'Gnome'): 'T',
    ('Halfling', 'Half_Elf'): 'N',
    ('Halfling', 'Halfling'): 'P',
    ('Halfling', 'Half_Orc'): 'N',
    ('Halfling', 'Human'): 'N',
    ('Half_Orc', 'Dwarf'): 'H',
    ('Half_Orc', 'Elf'): 'A',
    ('Half_Orc', 'Gnome'): 'H',
    ('Half_Orc', 'Half_Elf'): 'A',
    ('Half_Orc', 'Halfling'): 'N',
    ('Half_Orc', 'Half_Orc'): 'P',
    ('Half_Orc', 'Human'): 'T',
    ('Human', 'Dwarf'): 'N',
    ('Human', 'Elf'): 'N',
    ('Human', 'Gnome'): 'N',
    ('Human', 'Half_Elf'): 'T',
    ('Human', 'Halfling'): 'N',
    ('Human', 'Half_Orc'): 'N',
    ('Human', 'Human'): 'P'
}


def getFriendStatus(race1, race2):
    return races[(race1,race2)]

if __name__ == "__main__":
    print(getFriendStatus("Dwarf","Half_Orc"))