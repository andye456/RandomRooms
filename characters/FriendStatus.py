"""
P P indicates that the race is generally preferred, and dealings with the members of the race will be reflected accordingly.
G means that considerable goodwill exists towards the race.
T indicates that the race is viewed with tolerance and generally acceptable, if not loved.
N shows that the race is thought of neutrally, although some suspicion will be evidenced.
A means that the race is greeted with antipathy.
H tokens a strong hatred for the race in question.
"""
races = {}
races[('Dwarf','Dwarf')]   = 'P'
races[('Dwarf','Elf')]     = 'A'
races[('Dwarf','Gnome')]   = 'G'
races[('Dwarf','Half_Elf')]= 'N'
races[('Dwarf','Halfling')]= 'G'
races[('Dwarf','Half_Orc')]= 'H'
races[('Dwarf','Human')]   = 'N'

races[('Elf','Dwarf')]   = 'A'
races[('Elf','Elf')]     = 'P'
races[('Elf','Gnome')]   = 'T'
races[('Elf','Half_Elf')]= 'G'
races[('Elf','Halfling')]= 'T'
races[('Elf','Half_Orc')]= 'A'
races[('Elf','Human')]   = 'N'

races[('Gnome','Dwarf')]   = 'G'
races[('Gnome','Elf')]     = 'T'
races[('Gnome','Gnome')]   = 'P'
races[('Gnome','Half_Elf')]= 'T'
races[('Gnome','Halfling')]= 'G'
races[('Gnome','Half_Orc')]= 'H'
races[('Gnome','Human')]   = 'N'

races[('Half_Elf','Dwarf')]   = 'N'
races[('Half_Elf','Elf')]     = 'P'
races[('Half_Elf','Gnome')]   = 'T'
races[('Half_Elf','Half_Elf')]= 'P'
races[('Half_Elf','Halfling')]= 'N'
races[('Half_Elf','Half_Orc')]= 'A'
races[('Half_Elf','Human')]   = 'T'

races[('Halfling','Dwarf')]   = 'G'
races[('Halfling','Elf')]     = 'G'
races[('Halfling','Gnome')]   = 'T'
races[('Halfling','Half_Elf')]= 'N'
races[('Halfling','Halfling')]= 'P'
races[('Halfling','Half_Orc')]= 'N'
races[('Halfling','Human')]   = 'N'

races[('Half_Orc','Dwarf')]   = 'H'
races[('Half_Orc','Elf')]     = 'A'
races[('Half_Orc','Gnome')]   = 'H'
races[('Half_Orc','Half_Elf')]= 'A'
races[('Half_Orc','Halfling')]= 'N'
races[('Half_Orc','Half_Orc')]= 'P'
races[('Half_Orc','Human')]   = 'T'

races[('Human','Dwarf')]   = 'N'
races[('Human','Elf')]     = 'N'
races[('Human','Gnome')]   = 'N'
races[('Human','Half_Elf')]= 'T'
races[('Human','Halfling')]= 'N'
races[('Human','Half_Orc')]= 'N'
races[('Human','Human')]   = 'P'
