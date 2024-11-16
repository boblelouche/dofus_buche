from config import constants



def unhash_cell(raw_cell):
    return [constants["ZKARRAY"].index(i) for i in raw_cell]


print()