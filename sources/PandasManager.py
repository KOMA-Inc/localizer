import pandas as pd
from ExportInput import ExportInput
from LProjName import LProjName
from StringsFileReader import Symbol
from LocalizationEntity import LocalizationEntity
from LocalizationGroup import LocalizationGroup
from hashlib import md5

class StringsColumn:

    def __init__(self, title, rows) -> None:
        self.title = title
        self.rows = rows

class PandasManager:

    _key = "key"

    def __init__(self):
        pass

    def create_export_inputs(self, groups):
        inputs = [self.__create_export_input(group) for group in groups]
        return inputs
    
    def create_import_groups(self, import_inputs, files):
        groups = [self.__create_import_groups(input, files) for input in import_inputs]
        return groups

    def __create_import_groups(self, import_input, files):
        if len(import_input.records) == 0:
            return [] 

        languages = [
            getattr(LProjName, self.__language(column)) 
            for column in import_input.records[0] if column != "key"
        ]

        string_elements_dict = {}
        for language in languages:
           string_elements_dict[language] = [] 

        for record in import_input.records:
            for key, value in record.items():
                if key == "key":
                    continue
                language_value = self.__language(key)
                language = getattr(LProjName, language_value)
                if value == "":
                    string_elements_dict[language].append({"type": "newline"})
                elif value.startswith(Symbol.lineComment.value):
                    if value.startswith(Symbol.unlocalizedComment.value):
                        continue
                    string_elements_dict[language].append({"type": "line_comment", "comment": value})
                elif value.startswith(Symbol.blockCommentStart.value):
                    string_elements_dict[language].append({"type": "block_comment", "comment": value})
                else:
                    string_elements_dict[language].append({"type": "string", "key": record["key"], "value": value})
        
        entities = []

        for key, string_elements in string_elements_dict.items():
            file = next((f for f in files if f.path.endswith(f"{key.value}.lproj/{import_input.name}.strings")), None)
            if file is not None:
                entities.append(LocalizationEntity(file, string_elements))
        
        return LocalizationGroup(import_input.name, entities[0].file.kind, entities, md5(entities[0].file.path.encode()).hexdigest())

    
    def __language(self, string):
        # Split the string by spaces and join without spaces
        camel_case_string = ''.join(string.split())

        # Convert the first character to lowercase
        camel_case_string = camel_case_string[0].lower() + camel_case_string[1:]
        
        return camel_case_string
    
    def __create_export_input(self, group):
        entities = sorted(group.entities, key=lambda e: e.language.title)
        key_index = next((i for i, entity in enumerate(entities) if entity.language == group.preferences.key_language), None)

        if key_index is not None:
            key_entity = entities.pop(key_index)
            entities.insert(0, key_entity)

        titles = [e.language.title for e in entities]
        titles.insert(0, self._key)

        key_language = entities[0].language
        
        columns = [StringsColumn(t, []) for t in titles]

        for entity in entities:
            for index, element in enumerate(entity.string_elements):
                if element["type"] == "string":
                    key, value = element["key"], element["value"]
                    key_index = next((i for i, row in enumerate(columns[0].rows) if row == key), None)
                    # If there is NO row with `key` text, then create one for every column
                    if key_index is None:
                        for index, title in enumerate(titles):
                            # if this is a key column, add key
                            if title == self._key:
                                columns[index].rows.append(key)
                            # if it is the current entity's language column, add value
                            elif title == entity.language.title:
                            # else add empty string
                                columns[index].rows.append(value)
                            else:
                                columns[index].rows.append("")
                    # else, update the row in column of current entity's language
                    else:
                        columns[titles.index(entity.language.title)].rows[key_index] = value

                elif element["type"] in ['line_comment', 'block_comment'] and entity.language == key_language:
                    comment = element["comment"]
                    for column in columns:
                        column.rows.append(comment)
                elif element["type"] == 'newline' and entity.language == key_language:
                    for column in columns:
                        column.rows.append("")
        
        data = { }
        for column in columns:
            data[column.title] = column.rows
        df = pd.DataFrame(data)
        return ExportInput(group.name, df)
