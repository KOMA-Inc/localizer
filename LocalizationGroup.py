from LProjName import LProjName

class LocalizationGroup:

    class Preferences:

        def __init__(self, sheet_name, key_language):
            self.sheet_name = sheet_name
            self.key_language = key_language

    def __init__(self, name, kind, entities, grouping_value):
        self.name = name
        self.kind = kind
        self.entities = entities
        self.grouping_value = grouping_value
        self.languages = sorted([entity.language() for entity in entities], key=lambda x: x.value)
        self.preferences = LocalizationGroup.Preferences(
            name, 
            LProjName.english if LProjName.english in self.languages else self.languages[0]
        )