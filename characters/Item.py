# If the item is created at a location where there is a monster then the item belongs to that monster
# If it is created in a room  with no monster then it a loose and can be picked up

class Item:

    def __init__(self, item_object, owner):
        self.item_object = item_object
        self.owner = owner