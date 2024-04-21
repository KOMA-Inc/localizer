class StringsFileWriter:

    def __init__(self):
        pass

    def write(self, groups):
        for group in groups:
            self.__write(group)

    def __write(self, group):
        for entity in group.entities:
            self.__wtite_entity(entity)

    def __wtite_entity(self, entity):
        # Open the file for writing
        first = entity.string_elements[0]

        if first is None:
            return
        
        with open(entity.file.path, 'w') as file:
            for element in entity.string_elements:
                if element["type"] == "newline":
                    file.write("\n")
                elif element["type"] in ['line_comment', 'block_comment']:
                    file.write(f'{element["comment"]}\n')
                elif element["type"] == "string":
                    file.write(f'"{element["key"]}" = "{element["value"]}";\n')
