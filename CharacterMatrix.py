import dill as dill


class CharacterMatrix:
    # x_ref = 0
    # y_ref = 0
    def __init__(self):
        self.character_ref = {}

    def addCharacter(self, ref, character):
        self.character_ref[ref] = character

    def getCharacter(self, x, y):
        return self.character_ref[(x, y)]

    def attack(self, char_ref):
        return self.character_ref[char_ref]

    # returns the character object matrix
    def get_character_matrix(self):
        # Open the serialised data file in read/binary mode
        f = open("character.bin", "rb")

        # Load the saved data dictionary.
        character_ref = dill.load(f)

        return character_ref

    def dump_chars_to_binary(self):
        print("Dumping characters to binary file")
        # dumps the matrix of characters to a binary file
        with open("characters.bin", "wb") as f:
            dill.dump(self.character_ref, f)
