class SheetsNamesCreator:

    def __init__(self):
        pass

    def create_names(self, files):
        names = [file.name.split('.')[0] for file in files]
        return list(set(names))