import dill as dill


class CharacterMatrix:
    x_ref = 0
    y_ref = 0
    character_ref={}

    def addCharacter(self, ref, character):
        self.character_ref[ref]=character

    def getCharacter(self, x, y):
        return self.character_ref[(x,y)]

    # returns the character object matrix
    def get_character_matrix(self):
        # Open the serialised data file in read/binary mode
        f = open("character.bin", "rb")

        # Load the saved data dictionary.
        character_ref = dill.load(f)

        return character_ref

    def dump_chars_to_binary(self):
        # dumps the matrix of room to a binary file
        with open("characters.bin","wb") as f:
            dill.dump(self.character_ref, f)
