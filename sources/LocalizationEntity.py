class LocalizationEntity:

    def __init__(self, file, string_elements) -> None:
        self.file = file
        self.string_elements = string_elements

    @property
    def language(self):
        return self.file.language_folder