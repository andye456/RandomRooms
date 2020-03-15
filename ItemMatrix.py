import dill as dill

class ItemMatrix:
    # x_ref = 0
    # y_ref = 0
    item_ref = {}
    item_collection = []

    def addItem(self, ref, item_array):
        self.item_ref[ref] = item_array

    def getItem(self, x, y):
        return self.item_ref[(x, y)]

    # returns the item object matrix
    def get_item_matrix(self):
        # Open the serialised data file in read/binary mode
        f = open("item.bin", "rb")

        # Load the saved data dictionary.
        item_ref = dill.load(f)

        return item_ref

    def dump_items_to_binary(self):
        print("Dumping items to binary file")
        # dumps the matrix of items to a binary file
        with open("items.bin", "wb") as f:
            dill.dump(self.item_ref, f)
