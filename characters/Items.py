import random
Belt        = {"name":"Belt", "buy":"3sp", "sell":"1sp"}
Backpack    = {"name":"Backpack", "buy":"2gp", "sell":"1gp"}
Candle      = {"name":"Candle", "buy":"1sp", "sell":"1sp"}
Sack        = {"name":"Sack", "buy":"1sp", "sell":"1sp"}

# For each item add it to this list so it can be selected at random
group_of_items=[Belt,Backpack,Candle,Sack]


def getRandomItems():
    list_of_random_items = []
    num_to_select = random.randint(1, len(group_of_items))
    list_of_random_items = random.sample(group_of_items, num_to_select)
    return list_of_random_items