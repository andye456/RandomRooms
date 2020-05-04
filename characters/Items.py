import random
'''
The items are added to the item matrix 
'''
Belt        = {"name":"Belt", "type":"item", "buy":"3sp", "sell":"1sp"}
Backpack    = {"name":"Backpack", "type":"item", "buy":"2gp", "sell":"1gp"}
Candle      = {"name":"Candle", "type":"item", "buy":"1sp", "sell":"1sp"}
Snake       = {"name":"Snake", "type":"item", "buy": "5gp", "sell":"4gp"}
Sack        = {"name":"Sack", "type":"item", "buy":"1sp", "sell":"1sp"}



healing1 = {"name":"healing1", "type":"potion", "power": 1, "experience": 1, "uses": 5, "who": [{"class": "all"}]}
healing2 = {"name":"healing2", "type":"potion", "power": 2, "experience": 2, "uses": 6, "who": [{"class": "all"}]}
healing3 = {"name":"healing3", "type":"potion", "power": 3, "experience": 5, "uses": 7, "who": [{"class": "all"}]}
healing4 = {"name":"healing4", "type":"potion", "power": 4, "experience": 10, "uses": 8, "who": [{"class": "all"}]}
healing5 = {"name":"healing5", "type":"potion", "power": 5, "experience": 20, "uses": 9, "who": [{"class": "all"}]}
# Boost is a one off potion to boost anything by 5 points
boost = {"name":"boost", "type":"potion", "power": 5, "experience": 8, "uses": 1, "who": [{"class": "all"}]}
# Invisibility potion
invisible = {"name":"invisible", "type":"potion", "power": 1, "experience": 10, "uses": 1, "who": [{"class": "illusionist"}, {"class": "monk"}]}

# For each item add it to this list so it can be selected at random
group_of_items=[Belt,Backpack,Candle,Sack,Snake]
# For each potion add it to this list so one can be chosen at random
group_of_potions=[healing1,healing2,healing3,healing4,healing5,boost,invisible]

# group_of_items=[Belt.copy(),Backpack.copy(),Candle.copy(),Sack.copy(),Snake.copy()]
# group_of_potions=[healing1.copy(),healing2.copy(),healing3.copy(),healing4.copy(),healing5.copy(),boost.copy(),invisible.copy()]


def getRandomItems():
    list_of_random_items = []
    num_to_select = random.randint(1, len(group_of_items))
    list_of_random_items = random.sample(group_of_items, num_to_select)
    return list_of_random_items

def getARandomPotion():
    return random.choice(group_of_potions)