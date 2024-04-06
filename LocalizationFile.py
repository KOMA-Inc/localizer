from FileExtension import FileExtension
from enum import Enum
import hashlib
import os

class LocalizationFile:

    class Kind(Enum):
        strings = "strings"
        stringsDictionary = "stringsDictionary"

        @staticmethod
        def create(path):
            file_extension = os.path.splitext(path)[1][1:]
            if file_extension == FileExtension.strings.value:
                return LocalizationFile.Kind.strings
            elif file_extension == FileExtension.stringsDictionary.value:
                return LocalizationFile.Kind.stringsDictionary
            else:
                return None
            
    def __init__(self, language_folder, name, kind, path):
        self.identifier = hashlib.md5(path.encode()).hexdigest()
        self.language_folder = language_folder
        self.name = name
        self.kind = kind
        self.path = path
    
    @staticmethod
    def create(path, language):
        kind = LocalizationFile.Kind.create(path)
        if kind:
            name = os.path.basename(path)
            return LocalizationFile(language_folder=language, name=name, kind=kind, path=path)
        return None