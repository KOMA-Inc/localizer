from enum import Enum
from LocalizationFile import LocalizationFile
from LocalizationEntity import LocalizationEntity

class Symbol(Enum):
    lineComment = "//"
    blockCommentStart = "/*"
    blockCommentEnd = "*/"
    newline = "\n"
    unlocalizedComment = "//<unlocalized>"

class StringsFileReader:
    
    def __init__(self):
        pass

    def localization_entities(self, files):
        entities = []
        for file in files:
            if file.kind == LocalizationFile.Kind.strings:
                entity = self.__read_strings(file)
                entities.append(entity)
                # TODO: - Add support for other types
        return entities

    def __read_strings(self, localization_file):
        path = localization_file.path
        with open(path, 'r') as file:
            lines = file.readlines()

        array = [line.rstrip() for line in lines]
        results = []

        while array:
            first = array.pop(0).strip()

            if first.startswith(Symbol.blockCommentStart.value):
                comment = first

                while array:
                    next_line = array.pop(0).strip()
                    comment += "\n" + next_line

                    if next_line.endswith(Symbol.blockCommentEnd.value):
                        break

                results.append({"type": "block_comment", "comment": comment})
                continue

            if first.startswith(Symbol.lineComment.value):
                if first.startswith(Symbol.unlocalizedComment.value):
                    continue
                results.append({"type": "line_comment", "comment": first})
                continue

            if not first:
                while array and not array[0].strip():
                    array.pop(0)
                results.append({"type": "newline"})
                continue

            if first.startswith('"'):
                parts = [part.strip() for part in first.split("=")]

                if len(parts) == 2:
                    key = parts[0].strip('"')
                    value, *comment = parts[1].split('";')
                    value = value.strip('"')

                    results.append({"type": "string", "key": key, "value": value})
                    continue

        return LocalizationEntity(localization_file, results)
